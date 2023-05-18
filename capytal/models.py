import datetime as dt
import yfinance as yf
from typing import List
from dataclasses import dataclass, field


@dataclass
class Asset:
    symbol: str
    holding: bool = False
    ticker: yf.Ticker = field(init=False)

    def __post_init__(self):
        self.symbol = self.symbol.upper()
        self.ticker = yf.Ticker(self.symbol)


@dataclass
class Transaction:
    date: dt.datetime
    ticker: str
    side: str
    price: float

    def __post_init__(self):
        self.ticker = self.ticker.upper()
        self.side = self.side.lower()
        self.price = round(self.price, 2)


class AssetCollection:
    def __init__(self, symbols: List[str]):
        self.__symbols = symbols
        self.__assets = [Asset(symbol=symbol) for symbol in self.__symbols]

    def add(self, symbol: str):
        new_asset = Asset(symbol=symbol.upper())
        self.__assets.append(new_asset)


class TradeLog:
    def __init__(self) -> None:
        self.__buy_log = []
        self.__sell_log = []

    @property
    def buy_count(self) -> int:
        return len(self.__log)

    def update(self, transaction: Transaction):
        if transaction.side == "buy":
            self.__buy_log.append(transaction)
        if transaction.side == "sell":
            self.__sell_log.append(transaction)
        else:
            raise ValueError(f'Expecting \"buy\" or \"sell\", got \"{transaction.side}\"')