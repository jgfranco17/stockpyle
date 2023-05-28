import datetime as dt
import pandas as pd
import pandas_ta as ta
from typing import Tuple
from .assets import Asset


class AlgorithmComputer:
    def __init__(self, symbol: str, interval_fast: int = 10, interval_slow: int = 30) -> None:
        self.__symbol = symbol.upper()
        self.__asset = Asset(symbol=self.__symbol, holding=False)
        self.__interval = {"slow": interval_slow, "fast": interval_fast}

    @property
    def asset(self) -> Asset:
        return self.__asset

    def _get_ticker_data(self, span: int) -> pd.DataFrame:
        """
        Retrieve ticker historical data.

        Args:
            span (int): Number of days prior to look into

        Returns:
            pd.DataFrame: Historical data
        """
        # Retrieve yfinance data
        start_date = (dt.datetime.now() - dt.timedelta(days=span)).strftime('%Y-%m-%d')
        dataframe = self.__asset.ticker.history(start=start_date, interval='1m')

        # Postprocessing
        del dataframe['Dividends'], dataframe['Stock Splits'], dataframe['Volume']
        dataframe['SMA_fast'] = ta.sma(dataframe['Close'], self.__interval["fast"])
        dataframe['SMA_slow'] = ta.sma(dataframe['Close'], self.__interval["slow"])
        return dataframe

    @staticmethod
    def _get_metrics(dataframe: pd.DataFrame) -> Tuple[float, float, float]:
        metrics = ("Close", "SMA_fast", "SMA_slow")
        return (dataframe.iloc[-1][key] for key in metrics)

    def compute(self) -> Tuple[bool, str, float]:
        """
        Run the algorithm using the retrieved dataframe.

        Returns:
            bool: True if the algorithm creates a new recommendation
            str: Transaction side
            float: Price of recommended transaction
        """
        new_recommendation_created: bool = False
        side: str = "none"
        df = self._get_ticker_data(span=2)
        price, df_fast, df_slow = self._get_metrics(df)

        # Determine course of action
        if df_fast > df_slow and not self.__asset.holding:
            print(f'Buy {self.__symbol} @ ${price:.2f}')
            side = "buy"
            new_recommendation_created = True
            self.__asset.update_holding(status=True)

        elif df_fast < df_slow and self.__asset.holding:
            print(f'Sell {self.__symbol} @ ${price:.2f}')
            side = "sell"
            new_recommendation_created = True
            self.__asset.update_holding(status=False)

        else:
            print(f'Currently no recommendations for {self.__symbol} stocks.')

        return new_recommendation_created, side, price
