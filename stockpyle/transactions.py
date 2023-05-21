import os
import json
import datetime as dt
from typing import List, Tuple
from dataclasses import dataclass



@dataclass(repr=True)
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


class TradeLog:
    def __init__(self) -> None:
        self.__logs: List[Transaction] = []
        self.__buy_count: int = 0
        self.__sell_count: int = 0

    def __getitem__(self, key: str) -> Tuple[Transaction]:
        if key not in ("buy", "sell"):
            raise KeyError(f'Invalid key \"{key}\" provided.')

        return (item for item in self.__logs if item.side == key.lower())

    def __iter__(self) -> Transaction:
        for item in self.__logs:
            yield item

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
        now = dt.datetime.now()
        timestamp = now.strftime("%d-%b-%Y_%H%M")
        export_directory = os.path.join(os.getcwd(), "trades")
        os.makedirs(export_directory, exist_ok=True)
        export_path = os.path.join(export_directory, f'tradelogs_{timestamp}.json')

        with open(export_path, "w") as file:
            json.dump(raw_data, file)

        print(f'Wrote {len(self.__logs)} transactions ({self.buy_count} buys, {self.sell_count} sells) to JSON file.')
