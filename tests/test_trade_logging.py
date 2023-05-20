import pytest
import datetime as dt
from stockpyle.models import Transaction, TradeLog


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