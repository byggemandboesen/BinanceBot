import ccxt

class Account:

    def __init__(self, APIKEY, SECRETKEY, SYMBOL):
        self.client = ccxt.binance({"apiKey": APIKEY, "secret": SECRETKEY}) # Change to bybit!!
        self.SYMBOL = SYMBOL

    # Returns historic klines
    def getKlines(self, symbol, interval, limit = 180):
        klines = self.client.fetch_ohlcv(
            symbol = self.SYMBOL,
            timeframe = interval,
            limit = limit, # Number of candles to retrieve
        )
        return klines

    # Returns balance of chosen coin
    def getBalance(self, coin):
        balance = self.client.fetch_balance()
        free_balance = balance["free"][coin]
        return free_balance

    # Places order on coin in chosen symbol
    def placeOrder(self, symbol, type, price):
        response = self.client.create_order(self.SYMBOL, "limit", type, 1, price, params = {"test": True})
        print(response)
        print(f"Order placed on {symbol}, type: {type}")
        # TODO If order is succesful return XXXX else return ERROR

# NOTE! Place limit orders if possible. Otherwise 0.5% fees instead of 0.1%
# NOTE! Keep BNB funds available for lower fees