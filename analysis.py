import numpy as np
from ta import momentum, trend

class Analyzer:

    def __init__(self, parameters):
        self.TakeProfit = parameters["TakeProfit"]
        self.MaxLoss = parameters["MaxLoss"]
        self.StopLoss = parameters["StopLoss"]
        self.Oversold = parameters["Oversold"]
        self.Overbought = parameters["Overbought"]
    
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
        try:
            bullish = self.checkBuy(df)
        except Exception as e:
            print(e)
        print(bullish)

        if all(bullish):
            print(f"Order placed at price = {closes[-1]}")
        # Check if position is already held in coin and create buy conditions with less bullish indicators.

        # print(df)


    def checkBuy(self, df):
        ema = True if (df["EMA25"].iloc[-1] > df["EMA50"].iloc[-1] > df["EMA100"].iloc[-1]) else False
        rsi = True if (df["RSI"].iloc[-1] < self.Oversold) else False
        macd = True if all([(df["MACD"].iloc[-1] > df["SIGNAL"].iloc[-1]), (df["MACD"].iloc[-1] < 0)]) else False

        bullish = [ema, rsi, macd]
        return bullish