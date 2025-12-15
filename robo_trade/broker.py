from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Optional, Dict, Any


class BrokerClient(Protocol):
    def place_order(self, symbol: str, side: str, amount_brl: float, expiration_time: int = 60) -> Dict[str, Any]:
        ...

    def get_balance(self) -> Dict[str, Any]:
        ...


@dataclass
class BrokerConfig:
    platform: str
    email: Optional[str] = None
    password: Optional[str] = None
    lang: str = "pt"
    environment: str = "demo"


def create_broker_from_settings(settings) -> Optional[BrokerClient]:
    """Factory to create a broker client from settings."""
    try:
        from .quotex import QuotexClient, QuotexConfig
        if settings.quotex_email and settings.quotex_password:
            cfg = QuotexConfig(
                email=settings.quotex_email,
                password=settings.quotex_password,
                lang=settings.quotex_lang or "pt"
            )
            return QuotexClient(cfg)
    except Exception:
        return None
    return None
