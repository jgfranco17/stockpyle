import argparse


def get_args():
    parser = argparse.ArgumentParser("Capytal Trader")
    parser.add_argument("symbol",
                        type=str,
                        help="Stock ticker symbol to monitor")
    args = parser.parse_args()
    return args