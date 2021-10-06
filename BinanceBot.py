import websocket, json, pprint
from binance import Client, ThreadedWebsocketManager

SOCKET_PREFIX = "wss://stream.binance.com:9443/ws/"


class Bot:
    # Initialize the bot with certain parameters
    def __init__(self, config):
        self.SYMBOL = config["Symbol"].lower()
        self.TAKEPROFIT = config["Parameters"]["TakeProfit"]
        self.MAXLOSS = config["Parameters"]["MaxLoss"]
        self.STOPLOSS = config["Parameters"]["StopLoss"]
        self.OVERSOLD = config["Parameters"]["Oversold"]
        self.OVERBOUGHT = config["Parameters"]["Overbought"]
        self.KLINE_INTERVAL = config["Parameters"]["KLineInterval"]

        self.APIKEY = config["Secrets"]["APIKey"]
        self.SECRETKEY = config["Secrets"]["SecretKey"]
        self.client = Client(api_key = self.APIKEY, api_secret = self.SECRETKEY, testnet = True)
    
    # Opens websocket and starts streaming k-lines
    def RunBot(self):
        print("Bot is running...")
        print("Establishing connection to websocket...")
        
        SOCKET = f"{SOCKET_PREFIX}{self.SYMBOL}@kline_{self.KLINE_INTERVAL}"
        WebSocket = websocket.WebSocketApp(SOCKET, on_open = self.OnOpen, on_close = self.OnClose, on_message = self.OnMessage)
        WebSocket.run_forever()

    # Callback function for websocket, when it's opened
    def OnOpen(self, ws):
        print("Connection established!")
        print("Streaming data...")
    
    # Callback function for websocket, when it's closed
    def OnClose(self, ws):
        print("Connection closed!")
    
    # Callback function for websocket, when message is received
    def OnMessage(self, ws, message):
        json_message = json.loads(message)
        pprint.pprint(json_message)


# Reads user parameters
def ReadParams():
    path = 'Parameters.json'
    config = open(path, 'r')
    parsed_config = json.load(config)
    return parsed_config

if __name__ == "__main__":
    config = ReadParams()
    symbol = config['Symbol']
    BinanceBot = Bot(config)
    BinanceBot.RunBot()
    