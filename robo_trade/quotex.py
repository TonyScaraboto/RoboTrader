from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
import asyncio
import logging
import sys
from datetime import datetime

# Suppress noisy asyncio event loop warnings on Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.getLogger('asyncio').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

@dataclass
class QuotexConfig:
    email: str
    password: str
    lang: str = "pt"


class QuotexClient:
    """Cliente Quotex usando a biblioteca pyquotex oficial."""
    
    def __init__(self, config: QuotexConfig) -> None:
        self.config = config
        self.client = None
        self.connected = False
        self._loop = None
        
        if not self.config.email:
            raise ValueError("Quotex email is required")
        if not self.config.password:
            raise ValueError("Quotex password is required")
    
    def _get_loop(self):
        """Obtém ou cria um event loop."""
        if self._loop is None or self._loop.is_closed():
            try:
                self._loop = asyncio.get_event_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop
    
    def _run_async(self, coro):
        """Executa uma corrotina de forma síncrona."""
        loop = self._get_loop()
        if loop.is_running():
            # Se o loop já está rodando, cria uma task
            return asyncio.create_task(coro)
        else:
            # Se o loop não está rodando, executa até completar
            return loop.run_until_complete(coro)
    
    async def _connect_async(self):
        """Conecta ao Quotex de forma assíncrona."""
        try:
            from pyquotex.stable_api import Quotex
            
            self.client = Quotex(
                email=self.config.email,
                password=self.config.password,
                lang=self.config.lang
            )
            
            # Conectar com retry
            check_connect, message = await self.client.connect()
            
            if not check_connect:
                logger.error(f"Failed to connect to Quotex: {message}")
                return False
            
            self.connected = True
            logger.info("Successfully connected to Quotex")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to Quotex: {str(e)}")
            self.connected = False
            return False
    
    def connect(self):
        """Conecta ao Quotex (versão síncrona)."""
        return self._run_async(self._connect_async())
    
    async def _place_order_async(self, symbol: str, side: str, amount_brl: float, expiration_time: int = 60):
        """Coloca ordem de forma assíncrona."""
        try:
            if not self.connected:
                await self._connect_async()
            
            # Normalizar símbolo (pyquotex usa formato como "EURUSD_otc")
            quotex_symbol = symbol.replace('/', '').replace('-', '') + "_otc"
            
            # Converter side para direction (call/put)
            direction = "call" if side.upper() in ("BUY", "CALL") else "put"
            
            # Verificar se asset está disponível
            asset_name, asset_data = await self.client.get_available_asset(quotex_symbol, force_open=True)
            
            if not asset_data or len(asset_data) < 3 or not asset_data[2]:
                logger.error(f"Asset {quotex_symbol} is closed or invalid")
                return {
                    "status": "error",
                    "error": f"Asset {quotex_symbol} is closed",
                    "symbol": symbol
                }
            
            # Executar compra
            buy_info = await self.client.buy(
                amount=amount_brl,
                asset=quotex_symbol,
                direction=direction,
                duration=expiration_time
            )
            
            if buy_info:
                logger.info(f"Order placed: {symbol} {direction} {amount_brl} BRL")
                return {
                    "status": "success",
                    "platform": "quotex",
                    "order_id": buy_info.get('id', 'N/A'),
                    "symbol": symbol,
                    "side": side,
                    "amount_brl": amount_brl,
                    "expiration_time": expiration_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                logger.error(f"Buy failed for {symbol}")
                return {
                    "status": "error",
                    "error": "Buy operation failed",
                    "symbol": symbol
                }
                
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            return {
                "status": "error",
                "platform": "quotex",
                "symbol": symbol,
                "side": side,
                "amount_brl": amount_brl,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def place_order(self, symbol: str, side: str, amount_brl: float, expiration_time: int = 60) -> dict:
        """
        Place a binary option order on Quotex.
        
        Args:
            symbol: Trading pair (e.g., 'ADA/USDT', 'EURUSD')
            side: 'CALL' (buy) or 'PUT' (sell)
            amount_brl: Amount in BRL
            expiration_time: Expiration time in seconds (default 60)
        
        Returns:
            Order response dict
        """
        return self._run_async(self._place_order_async(symbol, side, amount_brl, expiration_time))
    
    async def _get_balance_async(self):
        """Obtém saldo de forma assíncrona."""
        try:
            if not self.connected:
                await self._connect_async()
            
            balance = await self.client.get_balance()
            
            return {
                "status": "success",
                "balance": float(balance),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "balance": 0.0
            }
    
    def get_balance(self) -> Dict[str, Any]:
        """Get account balance."""
        return self._run_async(self._get_balance_async())
    
    async def _get_asset_info_async(self, symbol: str):
        """Obtém informações do asset de forma assíncrona."""
        try:
            if not self.connected:
                await self._connect_async()
            
            quotex_symbol = symbol.replace('/', '').replace('-', '') + "_otc"
            asset_name, asset_data = await self.client.get_available_asset(quotex_symbol)
            
            if asset_data and len(asset_data) >= 3:
                return {
                    "symbol": symbol,
                    "is_open": bool(asset_data[2]),
                    "payout": float(asset_data[1]) if len(asset_data) > 1 else 85.0
                }
            else:
                return {
                    "symbol": symbol,
                    "is_open": False,
                    "payout": 0.0
                }
        except Exception as e:
            logger.error(f"Failed to get asset info: {str(e)}")
            return {
                "symbol": symbol,
                "is_open": False,
                "error": str(e)
            }
    
    def get_asset_info(self, symbol: str) -> dict:
        """Get asset trading information."""
        return self._run_async(self._get_asset_info_async(symbol))
    
    def close(self):
        """Fecha conexão com Quotex."""
        if self.client:
            try:
                self._run_async(self.client.close())
            except Exception:
                pass
        self.connected = False
    
    def __del__(self):
        """Destrutor para garantir fechamento da conexão."""
        self.close()

