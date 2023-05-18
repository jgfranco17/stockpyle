import os
import json
import pytest
import datetime as dt
from unittest.mock import MagicMock, patch
from typing import List
from dataclasses import asdict
from tempfile import TemporaryDirectory
from stockpyle.models import Asset, Transaction, AssetCollection, TradeLog

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


def test_asset_initialization():
    asset = Asset("AAPL")
    assert asset.symbol == "AAPL"
    assert not asset.holding
    assert isinstance(asset.ticker, MagicMock)


def test_asset_post_init():
    asset = Asset("AAPL")
    assert asset.symbol == "AAPL"
    assert not asset.holding
    assert isinstance(asset.ticker, MagicMock)


def test_transaction_initialization():
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "buy", 100.0)
    assert transaction.date == dt.datetime(2022, 1, 1)
    assert transaction.ticker == "AAPL"
    assert transaction.side == "buy"
    assert transaction.price == 100.0


def test_transaction_post_init():
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "buy", 100.015)
    assert transaction.date == dt.datetime(2022, 1, 1)
    assert transaction.ticker == "AAPL"
    assert transaction.side == "buy"
    assert transaction.price == 100.02


def test_transaction_to_dict():
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "buy", 100.0)
    expected_dict = {
        "date": str(dt.datetime(2022, 1, 1)),
        "ticker": "AAPL",
        "side": "buy",
        "price": 100.0,
    }
    assert transaction.to_dict() == expected_dict


def test_asset_collection_initialization(sample_assets):
    asset_collection = AssetCollection(sample_assets)
    assert len(asset_collection._AssetCollection__assets) == 3


def test_asset_collection_add():
    asset_collection = AssetCollection([])
    asset_collection.add("AAPL")
    assert len(asset_collection._AssetCollection__assets) == 1


def test_trade_log_initialization():
    trade_log = TradeLog()
    assert len(trade_log._TradeLog__logs) == 0
    assert trade_log.buy_count == 0
    assert trade_log.sell_count == 0


def test_trade_log_update_buy():
    trade_log = TradeLog()
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "buy", 100.0)
    trade_log.update(transaction)
    assert len(trade_log._TradeLog__logs) == 1
    assert trade_log.buy_count == 1
    assert trade_log.sell_count == 0


def test_trade_log_update_sell():
    trade_log = TradeLog()
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "sell", 100.0)
    trade_log.update(transaction)
    assert len(trade_log._TradeLog__logs) == 1
    assert trade_log.buy_count == 0
    assert trade_log.sell_count == 1


def test_trade_log_update_invalid_side():
    trade_log = TradeLog()
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "invalid", 100.0)
    with pytest.raises(ValueError):
        trade_log.update(transaction)


def test_trade_log_export_json(sample_transactions):
    trade_log = TradeLog()
    trade_log._TradeLog__logs = sample_transactions
    with TemporaryDirectory() as temp_dir:
        export_path = os.path.join(temp_dir, "tradelogs.json")
        with patch("builtins.print") as mock_print:
            trade_log.export("json")
            mock_print.assert_called_with("Wrote 3 transactions to JSON file.")
        assert os.path.isfile(export_path)
        with open(export_path, "r") as file:
            data = json.load(file)
        assert len(data) == 3
        for index, transaction in enumerate(sample_transactions):
            assert data[index] == asdict(transaction)


def test_trade_log_export_invalid_format():
    trade_log = TradeLog()
    with pytest.raises(ValueError):
        trade_log.export("txt")
