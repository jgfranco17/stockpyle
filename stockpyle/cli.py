import argparse
from .trader import SingleAssetTrader


def get_args():
    parser = argparse.ArgumentParser("Stockpyle Trader")
    parser.add_argument("symbol",
                        type=str,
                        help="Stock ticker symbol to monitor")
    parser.add_argument("--export-data",
                        default=False, action="store_true",
                        help="Export the transaction history as JSON")
    args = parser.parse_args()
    return args


def main():
    header = r"""
  _________ __                 __                  .__.
 /   _____//  |_  ____   ____ |  | ________ ___.__.|  |   ____
 \_____  \\   __\/  _ \_/ ___\|  |/ /\____ <   |  ||  | _/ __ \
 /        \|  | (  <_> )  \___|    < |  |_> >___  ||  |_\  ___/
/_________/|__|  \____/ \_____>__|__\|   __//_____||____/\_____>
                                     |__|
    """
    args = get_args()
    print(header)
    traderbot = SingleAssetTrader(symbol=args.symbol)
    traderbot.run(save=args.export_data)
