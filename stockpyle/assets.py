import yfinance as yf
from typing import List
from dataclasses import dataclass, field


@dataclass
class Asset:
    symbol: str = field(compare=True)
    holding: bool = field(compare=True, default=False)
    ticker: yf.Ticker = field(init=False, repr=False)

    def __post_init__(self):
        self.symbol = self.symbol.upper()
        self.ticker = yf.Ticker(self.symbol)


class AssetCollection:
    def __init__(self, symbols: List[str]):
        self.__symbols = symbols
        self.__assets = [Asset(symbol=symbol) for symbol in self.__symbols]

    def add(self, symbol: str) -> None:
        new_asset = Asset(symbol=symbol.upper())
        self.__assets.append(new_asset)
