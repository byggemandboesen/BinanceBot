import numpy as np
from ta import momentum, trend

class Analyser:

    def __init__(self, df):
        self.closes = df["Close"]
        