import os
import json
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

    def to_dict(self) -> dict:
        return {
            "date": str(self.date),
            "ticker": self.ticker,
            "side": self.side,
            "price": self.price
        }


class AssetCollection:
    def __init__(self, symbols: List[str]):
        self.__symbols = symbols
        self.__assets = [Asset(symbol=symbol) for symbol in self.__symbols]

    def add(self, symbol: str):
        new_asset = Asset(symbol=symbol.upper())
        self.__assets.append(new_asset)


class TradeLog:
    def __init__(self) -> None:
        self.__logs: List[Transaction] = []
        self.__buy_count = 0
        self.__sell_count = 0

    @property
    def buy_count(self) -> int:
        return self.__buy_count

    @property
    def sell_count(self) -> int:
        return self.__sell_count

    def update(self, transaction: Transaction) -> None:
        if transaction.side == "buy":
            self.__buy_count += 1
        elif transaction.side == "sell":
            self.__sell_count += 1
        else:
            raise ValueError(f'Expecting \"buy\" or \"sell\", got \"{transaction.side}\".')

        self.__logs.append(transaction)

    def export(self) -> None:
        raw_data = [item.to_dict() for item in self.__logs]
        export_path = os.path.join(os.getcwd(), "tradelogs.json")

        with open(export_path, "w") as file:
            json.dump(raw_data, file)

        print(f'Wrote {len(self.__logs)} transactions to JSON file.')
