import time
import datetime as dt
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from tqdm import tqdm
from .models import Asset, TradeLog, Transaction
from .utils import get_pause


class SingleAssetTrader:
    def __init__(self, symbol: str, interval_fast: int = 10, interval_slow: int = 30) -> None:
        self.__symbol = symbol.upper()
        self.__asset = Asset(symbol=self.__symbol, holding=False)
        self.__interval_fast = interval_fast
        self.__interval_slow = interval_slow
        self.__tradelog = TradeLog()
        self.__currently_holding = False
        self.__is_running = False

    @property
    def ticker(self) -> yf.Ticker:
        return self.__asset.ticker

    def _get_ticker_data(self, span: int) -> pd.DataFrame:
        """
        Retrieve ticker historical data.

        Args:
            span (int): Number of days prior to look into

        Returns:
            pd.DataFrame: Historical data
        """
        start_date = (dt.datetime.now() - dt.timedelta(days=span)).strftime('%Y-%m-%d')
        return self.ticker.history(start=start_date, interval='1m')

    def _log_transaction(self, details: dict) -> None:
        """
        Log a transaction to the TradeLog.

        Args:
            details (dict): Transaction details
        """
        transaction = Transaction(**details)
        self.__tradelog.update(transaction)

    def run(self) -> None:
        """
        Run the algorithmic trader continuously.
        """
        self.__is_running = True
        print("Running algo trading...")
        while self.__is_running:
            try:
                df = self._get_ticker_data(span=2)
                del df['Dividends']
                del df['Stock Splits']
                del df['Volume']

                df['SMA_fast'] = ta.sma(df['Close'], self.__interval_fast)
                df['SMA_slow'] = ta.sma(df['Close'], self.__interval_slow)
                new_recommendation_created = False
                side = None
                price = df.iloc[-1]['Close']
                df_fast = df.iloc[-1]['SMA_fast']
                df_slow = df.iloc[-1]['SMA_slow']

                if df_fast > df_slow and not self.__currently_holding:
                    print(f'Buy {self.__symbol} @ ${price:.2f}')
                    self.__currently_holding = True
                    side = "buy"
                    new_recommendation_created = True

                elif df_fast < df_slow and self.__currently_holding:
                    print(f'Sell {self.__symbol} @ ${price:.2f}')
                    self.__currently_holding = False
                    side = "sell"
                    new_recommendation_created = True

                else:
                    print(f'Currently no recommendations for {self.__symbol} stocks.')

                if new_recommendation_created:
                    self._log_transaction({
                        "date": dt.datetime.now(),
                        "ticker": self.__symbol,
                        "side": side,
                        "price": price
                    })

                wait_interval = get_pause()
                if wait_interval:
                    for _ in tqdm(range(wait_interval), desc=f'Waiting {wait_interval}s'):
                        time.sleep(1)
                else:
                    continue

            except KeyboardInterrupt:
                self.__is_running = False
                print("\nShutting down trading bot!")
                self.__tradelog.export()
                break
