import pytest
import datetime as dt
from stockpyle.transactions import Transaction, TradeLog


def test_trade_log_init():
    trade_log = TradeLog()
    assert len(trade_log) == 0
    assert trade_log.buy_count == 0
    assert trade_log.sell_count == 0


def test_trade_log_attributes(sample_transactions):
    trade_log = TradeLog()
    for transaction in sample_transactions:
        trade_log.update(transaction)
    assert len(trade_log) == len(sample_transactions)
    assert len(trade_log) == trade_log.buy_count + trade_log.sell_count


def test_trade_log_update_buy(sample_buy_transaction):
    trade_log = TradeLog()
    trade_log.update(sample_buy_transaction)
    assert len(trade_log) == 1
    assert trade_log.buy_count == 1
    assert trade_log.sell_count == 0


def test_trade_log_update_sell(sample_sell_transaction):
    trade_log = TradeLog()
    trade_log.update(sample_sell_transaction)
    assert len(trade_log) == 1
    assert trade_log.buy_count == 0
    assert trade_log.sell_count == 1


def test_trade_log_update_invalid_side():
    trade_log = TradeLog()
    transaction = Transaction(dt.datetime(2022, 1, 1), "AAPL", "invalid", 100.0)
    with pytest.raises(ValueError):
        trade_log.update(transaction)