import datetime as dt
from stockpyle.models import Transaction


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