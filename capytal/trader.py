import time
import datetime as dt
import pandas_ta as ta
from .models import Asset, AssetCollection


class SingleAssetTrader:
    def __init__(self, symbol: str, interval_fast: int = 10, interval_slow: int = 30) -> None:
        self.__asset = Asset(symbol=symbol, holding=False)
        self.__interval_fast = interval_fast
        self.__interval_slow = interval_slow
        self.__tradelog = []
        self.__currently_holding = False
        self.__is_running = False

    @property
    def ticker(self):
        return self.__asset.ticker

    def run(self):
        self.__is_running = True
        while self.__is_running:
            start_date = (dt.datetime.now() - dt.timedelta(days=2)).strftime('%Y-%m-%d')
            df = self.ticker.history(start=start_date, interval='1m')
            del df['Dividends']
            del df['Stock Splits']
            del df['Volume']
            
            df['SMA_fast'] = ta.sma(df['Close'], self.__interval_fast)
            df['SMA_slow'] = ta.sma(df['Close'], self.__interval_slow)
            
            price = df.iloc[-1]['Close']
            if df.iloc[-1]['SMA_fast'] > df.iloc[-1]['SMA_slow'] and not self.__currently_holding:
                print(f"Buy {self.ticker} @ ${price}")
                self.__tradelog.append({
                    'date':dt.datetime.now(),
                    'ticker': self.ticker,
                    'side': 'buy',
                    'price': price
                })
                self.__currently_holding = True
            
            elif df.iloc[-1]['SMA_fast'] < df.iloc[-1]['SMA_slow'] and self.__currently_holding:
                print(f"Sell {self.ticker} @ ${price}")
                self.__tradelog.append({
                    'date':dt.datetime.now(),
                    'ticker': self.ticker,
                    'side': 'sell',
                    'price': price
                })
                self.__currently_holding = False
            
            time.sleep(60)
