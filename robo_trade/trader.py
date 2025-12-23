from __future__ import annotations
import argparse
import sys
from typing import List

from .config import settings
from .exchange import ExchangeClient
from .backtest import Backtester
from .martingale import MartingaleManager, MartingaleConfig
from .logger import CSVLogger
from .avalon import AvalonClient, AvalonConfig
from strategies.ema_cross import EMACross


def get_closes_from_ohlcv(ohlcv: List[List[float]]) -> List[float]:
    return [c[4] for c in ohlcv]


def run_backtest() -> None:
    ex = ExchangeClient()
    ohlcv = ex.fetch_ohlcv(settings.symbol, timeframe="1h", limit=300)
    closes = get_closes_from_ohlcv(ohlcv)
    strat = EMACross()
    signals = strat.generate_signals(closes)
    bt = Backtester()
    result = bt.run(closes, signals)
    print(f"Final equity: {result['final_equity']:.2f}")


def run_martingale_backtest() -> None:
    ex = ExchangeClient()
    # Use ADA/USDT hourly as proxy for candle directions (until broker API is integrated)
    ohlcv = ex.fetch_ohlcv("ADA/USDT", timeframe="1h", limit=500)
    opens = [c[1] for c in ohlcv]
    closes = [c[4] for c in ohlcv]
    mgr = MartingaleManager(MartingaleConfig())
    res = mgr.run(opens, closes)
    print(f"Martingale total profit (BRL, payout {settings.payout_ratio}%): {res.total_profit_brl:.2f}")
    print(f"Operations simulated: {len(res.sequence_results)}")
    # Persist operations
    logger = CSVLogger("data/martingale_operations.csv")
    logger.write_rows(res.sequence_results)
    print("Saved operations to data/martingale_operations.csv")


def run_paper() -> None:
    """Paper trading mode with Avalon Broker platform simulation."""
    print("=== Paper Trading Mode (Avalon Broker) ===")
    
    if not settings.avalon_email or not settings.avalon_password:
        print("WARNING: AVALON_EMAIL or AVALON_PASSWORD not configured.")
        print("Running in simulation mode only.")
    
    config = AvalonConfig(
        email=settings.avalon_email,
        password=settings.avalon_password,
        lang=settings.avalon_lang,
        environment="demo"
    )
    
    try:
        client = AvalonClient(config)
        
        # Get account info
        balance = client.get_balance()
        if balance.get("status") == "success":
            print(f"Balance: R$ {balance['balance']:.2f}")
        else:
            print("Balance unavailable (not connected).")
        
        # Get asset info
        asset_info = client.get_asset_info(settings.symbol)
        print(f"\nAsset: {asset_info['symbol']}")
        print(f"Payout: {asset_info.get('payout', 0)}%")
        if asset_info.get("enabled"):
            print("Ativo aberto para operações")
        else:
            print("Ativo fechado ou indisponível")
        
        print("\nPaper trading mode ready. TODO: implement live order simulation loop.")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set AVALON_EMAIL and AVALON_PASSWORD in .env file")


def run_live() -> None:
    """Live trading mode with Avalon Broker platform."""
    print("=== Live Trading Mode (Avalon Broker) ===")
    print("WARNING: This will place REAL orders with REAL money!")
    
    if not settings.avalon_email or not settings.avalon_password:
        print("ERROR: AVALON_EMAIL and AVALON_PASSWORD must be configured for live trading.")
        return
    
    confirmation = input("Type 'YES' to confirm live trading: ")
    if confirmation != 'YES':
        print("Live trading cancelled.")
        return
    
    config = QuotexConfig(
        email=settings.quotex_email,
        password=settings.quotex_password,
        lang=settings.quotex_lang
    )
    
    try:
        client = QuotexClient(config)
        print("Connected to Quotex using email/password")
        print("Live trading mode ready. TODO: implement martingale strategy execution loop.")
        
    except ValueError as e:
        print(f"Configuration error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Robo Trade")
    parser.add_argument("mode", choices=["backtest", "paper", "live", "martingale_backtest", "martingale_demo"], nargs="?", default=settings.mode)
    args = parser.parse_args()

    if args.mode == "backtest":
        run_backtest()
    elif args.mode == "paper":
        run_paper()
    elif args.mode == "live":
        run_live()
    elif args.mode == "martingale_backtest":
        run_martingale_backtest()
    elif args.mode == "martingale_demo":
        # Offline demo without network: synthetic candles alternating colors
        opens = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        closes = [11, 9, 11, 9, 11, 9, 11, 9, 11, 9]
        mgr = MartingaleManager(MartingaleConfig())
        res = mgr.run(opens, closes)
        print(f"[DEMO] Martingale total profit (BRL, 1:1 payout): {res.total_profit_brl:.2f}")
        logger = CSVLogger("data/martingale_demo.csv")
        logger.write_rows(res.sequence_results)
        print("Saved demo operations to data/martingale_demo.csv")
    else:
        print("Unknown mode.")
        sys.exit(1)


if __name__ == "__main__":
    main()
