import numpy as np
from ta import momentum, trend

class Analyzer:

    def __init__(self, parameters):
        self.TakeProfit = parameters["TakeProfit"]
        self.MaxLoss = parameters["MaxLoss"]
        self.StopLoss = parameters["StopLoss"]
        self.Oversolf = parameters["Oversold"]
        self.Overbought = parameters["Overbought"]
    
    # Returns Exponential moving average of price
    def ema(self, closes, windows):
        ema = trend.EMAIndicator(closes, windows)
        return ema.ema_indicator()

    # Returns RSI
    def rsi(self, closes, windows = 14):
        rsi = momentum.RSIIndicator(closes, windows)
        return rsi.rsi()

    # Returns MACD histogram (difference between MACD and signal line)
    def macd(self, closes, slow = 26, fast = 12, signal = 9):
        macd = trend.MACD(closes, slow, fast, signal)
        return macd.macd_diff()

    # Gets indicators
    def doAnalysis(self, df):
        # Get closes as floats
        closes = df["Close"].astype("float")
        
        # Calculate indicators
        df["EMA25"] = self.ema(closes, 25)
        df["EMA50"] = self.ema(closes, 50)
        df["RSI"] = self.rsi(closes)
        df["MACD"] = self.macd(closes)

        # Finally, drop NaN rows
        df = df.dropna()

        print(df)
