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
        self.__full_history: List[Transaction] = []
        self.__buy_history: List[Transaction] = []
        self.__sell_history: List[Transaction] = []

    def __len__(self) -> int:
        return len(self.__full_history)

    def __getitem__(self, key: str) -> List[Transaction]:
        output = []
        if key == "buy":
            output = self.__buy_history
        elif key == "sell":
            output = self.__sell_history
        else:
            raise ValueError(f'Expecting \"buy\" or \"sell\", got \"{key}\".')

        return output

    def __iter__(self) -> Transaction:
        for item in self.__full_history:
            yield item

    @property
    def buy_count(self) -> int:
        return len(self.__buy_history)

    @property
    def sell_count(self) -> int:
        return len(self.__sell_history)

    @property
    def history(self) -> list:
        return self.__full_history

    def update(self, transaction: Transaction) -> None:
        """
        Add a transaction to the log history.

        Args:
            transaction (Transaction): New transaction

        Raises:
            ValueError: if transaction is invalid
        """
        if transaction.side == "buy":
            self.__buy_history.append(transaction)
        elif transaction.side == "sell":
            self.__sell_history.append(transaction)
        else:
            raise ValueError(f'Expecting \"buy\" or \"sell\", got \"{transaction.side}\".')

        self.__full_history.append(transaction)

    def export(self) -> None:
        buy_data = [item.to_dict() for item in self.__buy_history]
        sell_data = [item.to_dict() for item in self.__sell_history]
        json_data = {"buy": buy_data, "sell": sell_data}
        timestamp = dt.datetime.now().strftime("%d-%b-%Y_%H%M")
        export_directory = os.path.join(os.getcwd(), "trades")
        os.makedirs(export_directory, exist_ok=True)
        export_path = os.path.join(export_directory, f'tradelogs_{timestamp}.json')

        with open(export_path, "w") as file:
            json.dump(json_data, file)

        print(f'Wrote {len(self.__full_history)} transactions ({self.buy_count} buys, {self.sell_count} sells) to JSON file.')
