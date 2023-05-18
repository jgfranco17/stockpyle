import io
import os
import argparse
from .trader import SingleAssetTrader


def get_args():
    parser = argparse.ArgumentParser("Capytal Trader")
    parser.add_argument("symbol",
                        type=str,
                        help="Stock ticker symbol to monitor")
    args = parser.parse_args()
    return args


def main():
    header = r"""
  _________ __                 __                  .__          
 /   _____//  |_  ____   ____ |  | ________ ___.__.|  |   ____  
 \_____  \\   __\/  _ \_/ ___\|  |/ /\____ <   |  ||  | _/ __ \ 
 /        \|  | (  <_> )  \___|    < |  |_> >___  ||  |_\  ___/ 
/_______  /|__|  \____/ \___  >__|_ \|   __// ____||____/\_____>
        \/                  \/     \/|__|   \/
    """
    args = get_args()
    print(header)
    traderbot = SingleAssetTrader(symbol=args.symbol)
    traderbot.run()
