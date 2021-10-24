import ccxt, websocket, json, os, datetime
import pandas as pd

# File imports
from client_events import Account
from analysis import Analyzer
import logger

SOCKET_PREFIX = "wss://stream.binance.com:9443/ws/"

class Bot:
    # Initialize the bot with certain parameters
    def __init__(self, config):
        self.COIN = config["Coin"]
        self.FUND = config["Fund"]
        self.PARAMETERS = config["Parameters"]
        self.SYMBOL_CCXT = f'{self.COIN}/{self.FUND}'
        self.SYMBOL_WEBSOCKET = (self.COIN + self.FUND).lower()

        self.KLINE_INTERVAL = config["Parameters"]["KLineInterval"]

        self.APIKEY = config["Secrets"]["APIKey"]
        self.SECRETKEY = config["Secrets"]["SecretKey"]
    
    # Main bot loop
    def runBot(self):
        
        # Initiate an account from API- and secret key
        self.account = Account(self.APIKEY, self.SECRETKEY, self.SYMBOL_CCXT)
        # Checks for available funds        
        free_funds, already_owned = self.checkFunds()
        
        # Get historical klines
        historic_klines = self.getKlines()

        # Initiate analyzing class
        self.analyzer = Analyzer(self.PARAMETERS)

        # Start websocket
        websocket = self.openSocket()

    # Checks for available funds in account
    def checkFunds(self):
        print("Checking for available funds...")
        free_funds = self.account.getBalance(self.FUND)
        already_owned = self.account.getBalance(self.COIN)
        print(f"Free funds available = {free_funds}{self.FUND}")
        print(f"Coins already owned = {already_owned}{self.COIN}")
        
        # Free funds available?
        # TODO Uncomment this!
        # if free_funds == 0:
        #     print("Not any available funds to buy coin...")
        #     quit()
        
        return free_funds, already_owned

    # Gets historical klines two hours back in time
    def getKlines(self):
        klines = self.account.getKlines(self.SYMBOL_CCXT, self.KLINE_INTERVAL)
        
        # Create pandas dataframe for ease of use
        df = pd.DataFrame(klines, columns = [
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"])

        # Convert unix to datetime
        df["Open time"] = pd.to_datetime(df["Open time"], unit = "ms")

        # Add dataframe to bot
        self.df = df

    # Opens a websocket for klines stream
    def openSocket(self):
        print("Establishing connection to websocket...")
        socket = f"{SOCKET_PREFIX}{self.SYMBOL_WEBSOCKET}@kline_{self.KLINE_INTERVAL}"
        webSocket = websocket.WebSocketApp(socket, on_open = self.onOpen, on_close = self.onClose, on_message = self.onMessage)
        webSocket.run_forever()
        return webSocket

    # Callback function for websocket, when it's opened
    def onOpen(self, ws):
        print("Connection established!")
    
    # Callback function for websocket, when it's closed
    def onClose(self, ws):
        print("Connection closed!")
    
    # Callback function for websocket, when message is received
    def onMessage(self, ws, message):
        # self.clear()
        print("Receiving data...")
        message = json.loads(message)["k"]
        
        data = [
            pd.to_datetime(message["t"], unit = "ms"),
            message["o"],
            message["h"],
            message["l"],
            message["c"],
            message["v"],
            ]

        # Check if candle is already in dataframe then update data, otherwise add it and remove old row
        if data[0] in self.df["Open time"].values:
            self.df.iloc[[-1]] = data
            
            response = self.analyzer.doAnalysis(self.df)
        else:
            self.df.drop(self.df.head(1).index, inplace = True)
            df_length = len(self.df)
            self.df.loc[df_length + 1] = data
            self.df.reset_index(drop = True, inplace = True)

            response = self.analyzer.doAnalysis(self.df)

        try:
        # If bot should buy or sell, do so
            print(response)
            if response == "BUY":
                order = self.account.placeOrder(self.SYMBOL_CCXT, "buy", self.df["Close"].iloc[-1])
                #Add order to logger
                logger.addOrder(order)
            elif response == "SELL":
                order = self.account.placeOrder(self.SYMBOL_CCXT, "sell", self.df["Close"].iloc[-1])
                logger.addOrder(order)
            
        except Exception as e:
            print(e)

        # Drop calculated columns. Yes I know, stupid but fixes errors when updating df with new data
        self.df = self.df.dropna(axis = 1)

    # Clear console for new dataframe printout update
    def clear(self):
        os.system('cls' if os.name =='nt' else 'clear')
        

# Reads user parameters
def readParams():
    path = 'Parameters.json'
    config = open(path, 'r')
    parsed_config = json.load(config)
    return parsed_config

if __name__ == "__main__":
    config = readParams()
    BinanceBot = Bot(config)
    BinanceBot.runBot()
    