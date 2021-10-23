import ccxt

class Account:

    def __init__(self, client):
        self.client = client

    # Returns balance of chosen coin
    def getBalance(self, coin):
        balance = self.client.fetch_balance()
        free_balance = balance["free"][coin]
        return free_balance

    # Places order on coin in chosen symbol
    def placeOrder(self, symbol, type):
        print(f"Order placed on {symbol}, type: {type}")
        # TODO If order is succesful return XXXX else return ERROR

# NOTE! Place limit orders if possible. Otherwise 0.5% fees instead of 0.1%
# NOTE! Keep BNB funds available for lower fees