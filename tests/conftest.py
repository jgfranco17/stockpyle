import pytest
import datetime as dt
from unittest.mock import MagicMock
from projects.stockpyle.stockpyle.assets import Transaction


@pytest.fixture
def mock_yfinance_ticker(monkeypatch):
    mock_ticker = MagicMock()
    monkeypatch.setattr("yfinance.Ticker", MagicMock(return_value=mock_ticker))
    return mock_ticker


@pytest.fixture
def sample_assets():
    return ["AAPL", "GOOGL", "MSFT"]


@pytest.fixture
def sample_transactions():
    return [
        Transaction(dt.datetime(2022, 1, 1), "AAPL", "buy", 100.0),
        Transaction(dt.datetime(2022, 1, 2), "GOOGL", "sell", 200.0),
        Transaction(dt.datetime(2022, 1, 3), "MSFT", "buy", 150.0),
    ]
