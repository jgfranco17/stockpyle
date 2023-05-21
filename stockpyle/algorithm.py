import datetime as dt
import numba
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from typing import Tuple
from .assets import Asset


class AlgorithmComputer:
    def __init__(self, symbol: str, interval_fast: int = 10, interval_slow: int = 30) -> None:
        self.__asset = Asset(symbol=symbol, holding=False)
        self.__interval_fast = interval_fast
        self.__interval_slow = interval_slow

    def _get_ticker_data(self, span: int) -> pd.DataFrame:
        """
        Retrieve ticker historical data.

        Args:
            span (int): Number of days prior to look into

        Returns:
            pd.DataFrame: Historical data
        """
        start_date = (dt.datetime.now() - dt.timedelta(days=span)).strftime('%Y-%m-%d')
        return self.__asset.ticker.history(start=start_date, interval='1m')

    def compute(self) -> Tuple[bool, str, float]:
        df = self._get_ticker_data(span=2)
        new_recommendation_created = False
        side = None
        del df['Dividends'], df['Stock Splits'], df['Volume']

        df['SMA_fast'] = ta.sma(df['Close'], self.__interval_fast)
        df['SMA_slow'] = ta.sma(df['Close'], self.__interval_slow)
        price = df.iloc[-1]['Close']
        df_fast = df.iloc[-1]['SMA_fast']
        df_slow = df.iloc[-1]['SMA_slow']

        if df_fast > df_slow and not self.__asset.holding:
            print(f'Buy {self.__symbol} @ ${price:.2f}')
            self.__asset.holding = True
            side = "buy"
            new_recommendation_created = True

        elif df_fast < df_slow and self.__asset.holding:
            print(f'Sell {self.__symbol} @ ${price:.2f}')
            self.__asset.holding = False
            side = "sell"
            new_recommendation_created = True

        else:
            print(f'Currently no recommendations for {self.__symbol} stocks.')

        return new_recommendation_created, side, price