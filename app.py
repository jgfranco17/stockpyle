from stockpyle.trader import SingleAssetTrader


def main():
    traderbot = SingleAssetTrader("MSFT")
    traderbot.run()


if __name__ == "__main__":
    main()