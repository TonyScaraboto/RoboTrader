# -*- coding: utf-8 -*-
"""
Sniffer de WebSocket para capturar protocolo do Avalon Broker
IMPORTANTE: Execute este script ENQUANTO faz login manualmente no site
"""
import asyncio
import websockets
import json
from datetime import datetime

WS_URL = "wss://ws.trade.avalonbroker.com/echo/websocket"

async def sniff_websocket():
    print("=" * 70)
    print("🔍 SNIFFER DE WEBSOCKET - AVALON BROKER")
    print("=" * 70)
    print(f"\nConectando a: {WS_URL}\n")
    
    try:
        async with websockets.connect(WS_URL, open_timeout=10) as ws:
            print("✅ Conectado ao WebSocket!\n")
            print("📡 Aguardando mensagens (Ctrl+C para parar)...\n")
            print("-" * 70)
            
            msg_count = 0
            
            while True:
                try:
                    # Receber mensagem
                    msg = await asyncio.wait_for(ws.recv(), timeout=60)
                    msg_count += 1
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    print(f"\n[{timestamp}] Mensagem #{msg_count}")
                    print(f"Tipo: {type(msg)}")
                    print(f"Tamanho: {len(msg)} bytes")
                    
                    # Tentar parsear como JSON
                    try:
                        data = json.loads(msg)
                        print("Formato: JSON")
                        print(json.dumps(data, indent=2, ensure_ascii=False))
                    except:
                        # Não é JSON, mostrar raw
                        print("Formato: Texto/Binário")
                        print(msg[:500])  # Primeiros 500 chars
                    
                    print("-" * 70)
                    
                except asyncio.TimeoutError:
                    print("\n⏱️  Nenhuma mensagem nos últimos 60 segundos...")
                    print("💡 Dica: Faça login no site trade.avalonbroker.com")
                    print("         para gerar mensagens no WebSocket\n")
                    
    except KeyboardInterrupt:
        print("\n\n⚠️  Captura interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print(f"\n💡 O WebSocket pode precisar de autenticação prévia")
        print("   ou estar em um caminho diferente.")
    
    print("\n" + "=" * 70)
    print("✅ Sniffer finalizado")
    print("=" * 70)

if __name__ == "__main__":
    print("\n🚀 Iniciando sniffer...\n")
    print("INSTRUÇÕES:")
    print("1. Execute este script")
    print("2. Abra https://trade.avalonbroker.com no navegador")
    print("3. Faça login")
    print("4. Observe as mensagens capturadas aqui")
    print("5. Pressione Ctrl+C quando terminar\n")
    
    asyncio.run(sniff_websocket())
