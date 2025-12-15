"""Legacy placeholder for old HomeBroker API.

This module is intentionally kept minimal to avoid using the deprecated
token/account-id flow. Use `robo_trade.quotex.QuotexClient` with
email/senha instead.
"""

from __future__ import annotations

class QuotexClient:
    def __init__(self, *_, **__):
        raise RuntimeError(
            "homebroker.py está obsoleto. Use robo_trade.quotex.QuotexClient com email/senha."
        )

