"""
Script para descobrir e testar URLs da API Avalon Broker
Execute: python discover_api.py
"""
# -*- coding: utf-8 -*-
import asyncio
import sys
import aiohttp
import websockets

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# URLs candidatas para testar
POSSIBLE_DOMAINS = [
    "avalonbroker.com",
    "www.avalonbroker.com",
    "trade.avalonbroker.com",
    "api.avalonbroker.com",
    "ws.avalonbroker.com",
    "app.avalonbroker.com",
    "quotex.io",  # Quotex como referência
    "qxbroker.com",
]

POSSIBLE_WS_PATHS = [
    "/socket.io/?EIO=3&transport=websocket",
    "/echo/websocket",
    "/realtime",
    "/ws",
    "/websocket",
    "/api/ws",
]

POSSIBLE_API_PATHS = [
    "/api/login",
    "/api/auth",
    "/api/v1/login",
    "/auth/login",
    "/login",
    "/signin",
]


async def test_websocket(url):
    """Testa conexão WebSocket"""
    try:
        async with websockets.connect(url, timeout=5) as ws:
            print(f"✅ WebSocket OK: {url}")
            
            # Tentar receber mensagem de boas-vindas
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2)
                print(f"   Recebido: {msg[:100]}...")
            except:
                pass
            
            return True
    except Exception as e:
        print(f"❌ WebSocket FALHOU: {url}")
        print(f"   Erro: {str(e)[:80]}")
        return False


async def test_api_endpoint(url):
    """Testa endpoint API REST"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                print(f"✅ API OK ({response.status}): {url}")
                return True
    except Exception as e:
        print(f"❌ API FALHOU: {url}")
        print(f"   Erro: {str(e)[:80]}")
        return False


async def discover_api():
    """Tenta descobrir URLs da API"""
    print("=" * 70)
    print("🔍 DESCOBRINDO API DO AVALON BROKER")
    print("=" * 70)
    
    # Teste 1: WebSocket URLs
    print("\n📡 Testando URLs WebSocket...\n")
    ws_found = []
    
    for domain in POSSIBLE_DOMAINS:
        for path in POSSIBLE_WS_PATHS:
            url = f"wss://{domain}{path}"
            if await test_websocket(url):
                ws_found.append(url)
            await asyncio.sleep(0.5)
    
    # Teste 2: API REST URLs
    print("\n🌐 Testando URLs API REST...\n")
    api_found = []
    
    for domain in POSSIBLE_DOMAINS:
        for path in POSSIBLE_API_PATHS:
            url = f"https://{domain}{path}"
            if await test_api_endpoint(url):
                api_found.append(url)
            await asyncio.sleep(0.5)
    
    # Resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)
    
    if ws_found:
        print(f"\n✅ WebSocket URLs encontradas ({len(ws_found)}):")
        for url in ws_found:
            print(f"   • {url}")
    else:
        print("\n❌ Nenhuma URL WebSocket funcionando")
    
    if api_found:
        print(f"\n✅ API REST URLs encontradas ({len(api_found)}):")
        for url in api_found:
            print(f"   • {url}")
    else:
        print("\n❌ Nenhuma URL API REST funcionando")
    
    # Instruções
    print("\n" + "=" * 70)
    print("📝 PRÓXIMOS PASSOS")
    print("=" * 70)
    
    if ws_found or api_found:
        print("\n1. Copie as URLs encontradas acima")
        print("2. Atualize robo_trade/avalon.py:")
        print("   AVALON_WS_URL = 'URL_WEBSOCKET'")
        print("   AVALON_API_URL = 'URL_API_REST'")
        print("\n3. Execute: python test_avalon_connection.py")
    else:
        print("\n⚠️  Nenhuma URL automática encontrada!")
        print("\nUSE O MÉTODO MANUAL:")
        print("1. Abra https://avalonbroker.com no navegador")
        print("2. Pressione F12 (DevTools)")
        print("3. Vá em Network → WS")
        print("4. Faça login no site")
        print("5. Copie a URL do WebSocket que aparecer")
        print("6. Atualize robo_trade/avalon.py com a URL correta")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("\n🚀 Iniciando descoberta da API...\n")
    asyncio.run(discover_api())
    print("\n✅ Descoberta concluída!\n")
