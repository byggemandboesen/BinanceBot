# BinanceBot
Crypto trading bot using the python-binance API <br>
***NOTE!!! I'M NOT RESPONSIBLE FOR ANY MONEY THAT MAY BE LOST USING THIS BOT!*** <br>
Also note, that the bot is still under development and will actually not perform any trades yet.

## Installing
As usual, the required packages are installed with:
~~~bash
pip install -r requirements.txt
~~~
However, you may need to install websocket-client with pip3.
~~~bash
pip3 install websocket-client
~~~

## Modifying parameters
One can modify the parameters that determine if the bot should sell at a certain loss or how/if a trailing stop-loss should be added when the profit of a trade increases above a certain threashold.<br>

This could be useful if you want to trade on longer/shorter timeframes for less overall trades pr. time. <br>
Below is an example of what a config file might look like at this current moment, however, this will likely change once the bot will be improved with defult parameters. <br>
~~~json
{
    "Symbol": "BNBBUSD",
    "Parameters":{
        "TakeProfit": 0.3,
        "MaxLoss": 15.0,
        "StopLoss": 0.5,
        "Oversold": 30,
        "Overbought": 70,
        "KLineInterval": "1m"
    },
    "Secrets":{
        "APIKey": "<Insert-Key-Here>",
        "SecretKey": "<Insert-Secret-Key>"
    }
}
~~~
What everything means <br>
* Symbol = Coins you wish to trade. NOTE! Keep BNB in your wallet for [lower fees](https://www.binance.us/en/fee/schedule).
* Parameters
    * TakeProfit = The increase at which you want you to sell above.
    * MaxLoss = The maximum percentage you are willing to loose before selling.
    * StopLoss = How far below current price should trailing stop-loss be?
    * OverSold = The RSI value at which the symbol is considered oversold.
    * OverBought = The RSI value at which the symbol is considered overbought.
    * KLineInterval = The interval of each candlestick. NOTE! String, as from [this list](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams).
* Secrets
    * APIKey = Your API key.
    * SecretKey = Your secret key.


