from __future__ import annotations
import ccxt
from .config import settings

class ExchangeClient:
    def __init__(self) -> None:
        exchange_id = settings.exchange
        if not hasattr(ccxt, exchange_id):
            raise ValueError(f"Unsupported exchange: {exchange_id}")
        cls = getattr(ccxt, exchange_id)
        kwargs = {"enableRateLimit": True}
        if settings.api_key and settings.api_secret:
            kwargs["apiKey"] = settings.api_key
            kwargs["secret"] = settings.api_secret
        if settings.api_password:
            kwargs["password"] = settings.api_password
        self.client = cls(kwargs)

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 200):
        return self.client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    def fetch_balance(self):
        return self.client.fetch_balance()

    def create_order(self, symbol: str, side: str, type_: str, amount: float, price: float | None = None):
        if type_ == "market":
            return self.client.create_order(symbol, type_, side, amount)
        return self.client.create_order(symbol, type_, side, amount, price)
