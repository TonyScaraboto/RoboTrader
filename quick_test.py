# -*- coding: utf-8 -*-
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from robo_trade.avalon import AvalonClient, AvalonConfig

async def quick_test():
    config = AvalonConfig(
        email="salaodainformatica@gmail.com",
        password="sua_senhabrandnew2022",
        environment="demo"
    )
    
    client = AvalonClient(config)
    
    print("Conectando ao Avalon Broker...")
    connected = await client.connect()
    
    if connected:
        print(f"Status: Conectado = {client.is_connected()}")
        
        balance = await client.get_balance()
        print(f"Saldo: R$ {balance.get('balance', 0):.2f}")
        print(f"Status Conexao: {balance.get('status', 'unknown')}")
        
        await client.disconnect()
    else:
        print("Falha na conexao")

if __name__ == "__main__":
    asyncio.run(quick_test())
