import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    exchange: str = os.getenv("EXCHANGE", "binance")
    api_key: str | None = os.getenv("API_KEY")
    api_secret: str | None = os.getenv("API_SECRET")
    api_password: str | None = os.getenv("API_PASSWORD")
    mode: str = os.getenv("MODE", "paper")  # backtest | paper | live
    symbol: str = os.getenv("SYMBOL", "BTC/USDT")
    base_currency: str = os.getenv("BASE_CURRENCY", "USDT")
    quote_currency: str = os.getenv("QUOTE_CURRENCY", "BTC")
    
    # Quotex platform configuration
    quotex_email: str | None = os.getenv("QUOTEX_EMAIL")
    quotex_password: str | None = os.getenv("QUOTEX_PASSWORD")
    quotex_lang: str = os.getenv("QUOTEX_LANG", "pt")  # pt | en | es
    quotex_environment: str = os.getenv("QUOTEX_ENVIRONMENT", "demo")  # demo | live
    
    initial_balance_brl: float = float(os.getenv("INITIAL_BALANCE_BRL", "1000"))
    payout_ratio: float = float(os.getenv("PAYOUT_RATIO", "85.0"))
    
    # Trading configuration
    expiration_time: int = int(os.getenv("EXPIRATION_TIME", "60"))  # seconds

    # Database (PostgreSQL) configuration
    database_url: str | None = os.getenv("DATABASE_URL")
    postgres_host: str | None = os.getenv("POSTGRES_HOST")
    postgres_port: str | None = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str | None = os.getenv("POSTGRES_DB")
    postgres_user: str | None = os.getenv("POSTGRES_USER")
    postgres_password: str | None = os.getenv("POSTGRES_PASSWORD")
    postgres_sslmode: str | None = os.getenv("PGSSLMODE")
    
    def reload(self):
        """Recarrega as configurações do arquivo .env"""
        load_dotenv(override=True)
        self.exchange = os.getenv("EXCHANGE", "binance")
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.api_password = os.getenv("API_PASSWORD")
        self.mode = os.getenv("MODE", "paper")
        self.symbol = os.getenv("SYMBOL", "BTC/USDT")
        self.base_currency = os.getenv("BASE_CURRENCY", "USDT")
        self.quote_currency = os.getenv("QUOTE_CURRENCY", "BTC")
        self.quotex_email = os.getenv("QUOTEX_EMAIL")
        self.quotex_password = os.getenv("QUOTEX_PASSWORD")
        self.quotex_lang = os.getenv("QUOTEX_LANG", "pt")
        self.quotex_environment = os.getenv("QUOTEX_ENVIRONMENT", "demo")
        self.initial_balance_brl = float(os.getenv("INITIAL_BALANCE_BRL", "1000"))
        self.payout_ratio = float(os.getenv("PAYOUT_RATIO", "85.0"))
        self.expiration_time = int(os.getenv("EXPIRATION_TIME", "60"))
        self.database_url = os.getenv("DATABASE_URL")
        self.postgres_host = os.getenv("POSTGRES_HOST")
        self.postgres_port = os.getenv("POSTGRES_PORT", "5432")
        self.postgres_db = os.getenv("POSTGRES_DB")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_sslmode = os.getenv("PGSSLMODE")

settings = Settings()
