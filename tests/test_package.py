import os
import json
import pytest
import datetime as dt
from stockpyle.models import Asset, Transaction, AssetCollection, TradeLog


def test_asset_init():
    asset = Asset("AAPL")
    assert asset.symbol == "AAPL"
    assert not asset.holding


def test_transaction_init():
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "buy", 100.0)
    assert transaction.date == dt.datetime(2022, 1, 1)
    assert transaction.ticker == "AAPL"
    assert transaction.side == "buy"
    assert transaction.price == 100.0


def test_transaction_post_init():
    transaction = Transaction(dt.datetime(2022, 1, 1), "aapl", "Buy", 100.015)
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


def test_asset_collection_init(sample_assets):
    asset_collection = AssetCollection(sample_assets)
    assert len(asset_collection._AssetCollection__assets) == 3


def test_asset_collection_add():
    asset_collection = AssetCollection([])
    asset_collection.add("AAPL")
    assert len(asset_collection._AssetCollection__assets) == 1


def test_trade_log_init():
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
