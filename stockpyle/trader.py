import time
import datetime as dt
import matplotlib.pyplot as plt
from typing import Optional
from tqdm import tqdm
from .transactions import TradeLog, Transaction
from .utils import get_pause
from .algorithm import AlgorithmComputer


class SingleAssetTrader:
    def __init__(self, symbol: str, interval_fast: int = 10, interval_slow: int = 30) -> None:
        self.__symbol = symbol.upper()
        self.tradelog = TradeLog()
        self.__is_running = False
        self.algorithm = AlgorithmComputer(
            symbol=self.__symbol,
            interval_fast=interval_fast,
            interval_slow=interval_slow
        )

    def __str__(self) -> str:
        return f'SingleAssetTrader(symbol={self.__symbol})'

    def _log_transaction(self, details: dict) -> None:
        """
        Log a transaction to the TradeLog.

        Args:
            details (dict): Transaction details
        """
        transaction = Transaction(**details)
        self.tradelog.update(transaction)

    def run(self, save: Optional[bool] = False) -> None:
        """
        Run the algorithmic trader continuously.
        """
        self.__is_running = True
        print(f'Running algo trading for {self.__symbol} stock...')
        while self.__is_running:
            try:
                new_recommendation_created, side, price = self.algorithm.compute()
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

            except KeyboardInterrupt:
                self.__is_running = False
                print("*" * 20)
                print("Shutting down trading bot!")
                if save:
                    self.tradelog.export()
                break

    def plot(self, side: str) -> None:
        dates = [transaction.date for transaction in self.tradelog if transaction.side == side.lower()]
        prices = [transaction.price for transaction in self.tradelog if transaction.side == side.lower()]
        print(f'PRICE TREND FOR {side.upper()} SIDE')
        plt.plot(dates, prices, color="limegreen")
        plt.show()
