from capytal.cli import get_args
from capytal.trader import SingleAssetTrader


def main():
    args = get_args()
    traderbot = SingleAssetTrader("MSFT")
    traderbot.run()


if __name__ == "__main__":
    main()