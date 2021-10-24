from os import access
import numpy as np
from ta import momentum, trend

class Analyzer:

    def __init__(self, parameters):
        self.TakeProfit = parameters["TakeProfit"] / 100
        self.StopLoss = parameters["StopLoss"] / 100
        self.TrailingStop = parameters["TrailingStop"] / 100
        self.Oversold = parameters["Oversold"]
        self.Overbought = parameters["Overbought"]
        
        self.OpenPosition = False
        self.BuyPrice = 0
        self.Target = 0
        self.Stop = 0
    
    # Returns Exponential moving average of price
    def ema(self, closes, windows):
        ema = trend.EMAIndicator(closes, windows)
        return ema.ema_indicator()

    # Returns RSI
    def rsi(self, closes, windows = 14):
        rsi = momentum.RSIIndicator(closes, windows)
        return rsi.rsi()

    # Returns MACD and signal line (difference between MACD and signal line)
    def macd(self, closes, slow = 26, fast = 12, signal = 9):
        macd = trend.MACD(closes, slow, fast, signal)
        return macd.macd(), macd.macd_signal()

    # Gets indicators
    def doAnalysis(self, df):
        # Get closes as floats
        closes = df["Close"].astype("float")
        # Calculate indicators
        df["EMA25"] = self.ema(closes, 25)
        df["EMA50"] = self.ema(closes, 50)
        df["EMA100"] = self.ema(closes, 100)
        df["RSI"] = self.rsi(closes)
        df["MACD"], df["SIGNAL"] = self.macd(closes)
        # Finally, drop NaN rows
        df = df.dropna()

        # Check for bullish indicators
        # bullish = self.checkBullish(df)
        
        # Check if position already open, otherwise check if bot should buy
        try:
            if self.OpenPosition:
                message = self.checkSell(closes.iloc[-1])
            elif (df["RSI"].iloc[-1] < self.Oversold):
                self.BuyPrice = closes.iloc[-1]
                self.Target = (1 + self.TakeProfit) * self.BuyPrice
                self.Stop = (1 - self.StopLoss) * self.BuyPrice
                
                print(f"In at price: {self.BuyPrice}")
                print(f"Target price is {self.Target}")
                print(f"Stoploss set to {self.Stop}")

                self.OpenPosition = True
                message = "BUY"
            else:
                message = "No buy-opportunity available"
        except Exception as e:
            print(e)
        
        return message

    # Check for indicators showing bullish movement
    def checkBullish(self, df):
        ema = True if (df["EMA25"].iloc[-1] > df["EMA50"].iloc[-1] > df["EMA100"].iloc[-1]) else False
        rsi = True if (df["RSI"].iloc[-1] < self.Oversold) else False
        macd = True if (df["MACD"].iloc[-1] - df["SIGNAL"].iloc[-1] < 0) else False

        bullish = [ema, rsi, macd]
        return bullish
    
    # Check if stoploss/limit is reached or if trailing stop should be added
    def checkSell(self, price):
        if price <= self.Stop:
            self.OpenPosition = False
            profit = (price - self.BuyPrice) / self.BuyPrice
            return f"SELL"
        elif price > self.Target:
            self.Stop = price # if price < self.TakeProfit * (1 + self.TrailingStop) else price * (1 - self.TrailingStop)
            return f"Trailing stoploss set to = {self.Stop}"
        return "Awaiting sell signal..."
