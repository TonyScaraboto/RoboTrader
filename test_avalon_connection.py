"""
Script de teste para validar conexão com Avalon Broker
Execute: python test_avalon_connection.py
"""
# -*- coding: utf-8 -*-
import asyncio
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from robo_trade.avalon import AvalonClient, AvalonConfig
from robo_trade.config import settings


async def test_connection():
    """Testa conexão básica com Avalon"""
    print("=" * 60)
    print("🧪 TESTE DE CONEXÃO - AVALON BROKER")
    print("=" * 60)
    
    # Configuração
    config = AvalonConfig(
        email=settings.quotex_email or "teste@email.com",
        password=settings.quotex_password or "senha123",
        lang="pt",
        environment=settings.quotex_environment or "demo"
    )
    
    print(f"\n📧 Email: {config.email}")
    print(f"🌍 Ambiente: {config.environment.upper()}")
    print(f"🔤 Idioma: {config.lang}\n")
    
    # Criar cliente
    client = AvalonClient(config)
    
    try:
        # Teste 1: Conexão
        print("🔌 Teste 1: Conectando ao Avalon...")
        connected = await client.connect()
        
        if connected:
            print("✅ Conexão estabelecida\n")
        else:
            print("❌ Falha na conexão\n")
            return
        
        # Teste 2: Obter saldo
        print("💰 Teste 2: Obtendo saldo...")
        balance_info = await client.get_balance()
        
        if balance_info["success"]:
            print(f"✅ Saldo: R$ {balance_info['balance']:.2f}")
            print(f"   Status: {balance_info.get('status', 'unknown')}")
            
            if balance_info.get("balance") == 10000.0 and config.environment == "demo":
                print("   ⚠️  Usando saldo simulado (fallback)")
            print()
        else:
            print(f"❌ Erro: {balance_info.get('error')}\n")
        
        # Teste 3: Informações de ativo
        print("📊 Teste 3: Informações do ativo EURUSD...")
        asset_info = await client.get_asset_info("EURUSD")
        
        if asset_info["success"]:
            print(f"✅ Ativo: {asset_info['symbol']}")
            print(f"   Habilitado: {asset_info['enabled']}")
            print(f"   Payout: {asset_info['payout']}%")
            print(f"   Min: R$ {asset_info['min_amount']:.2f}")
            print(f"   Max: R$ {asset_info['max_amount']:.2f}\n")
        else:
            print(f"❌ Erro: {asset_info.get('error')}\n")
        
        # Teste 4: Ordem de teste (apenas em demo)
        if config.environment == "demo":
            print("🎯 Teste 4: Executando ordem de teste...")
            print("   Aguarde 60 segundos para resultado...\n")
            
            order_result = await client.place_order(
                symbol="EURUSD",
                side="call",
                amount_brl=10.0,
                expiration_time=60
            )
            
            if order_result["success"]:
                print(f"✅ Ordem executada!")
                print(f"   ID: {order_result['order_id']}")
                print(f"   Símbolo: {order_result['symbol']}")
                print(f"   Direção: {order_result['side'].upper()}")
                print(f"   Valor: R$ {order_result['amount']:.2f}")
                print(f"   Expiração: {order_result['expiration']}s")
                print(f"   Resultado: {'✅ WIN' if order_result['win'] else '❌ LOSS'}")
                print(f"   Lucro/Perda: R$ {order_result['profit']:+.2f}")
                print(f"   Saldo Final: R$ {order_result['balance']:.2f}")
                
                if order_result.get("simulated"):
                    print(f"   ⚠️  Modo SIMULADO (API real não disponível)")
                else:
                    print(f"   ✅ Modo REAL")
                print()
            else:
                print(f"❌ Erro na ordem: {order_result.get('error')}\n")
        else:
            print("⚠️  Teste 4 pulado (ambiente REAL - não executar ordens de teste)\n")
        
        # Teste 5: Verificar estado da conexão
        print("🔍 Teste 5: Estado da conexão...")
        is_conn = client.is_connected()
        print(f"{'✅' if is_conn else '❌'} Conectado: {is_conn}\n")
        
    except Exception as e:
        print(f"❌ Erro durante testes: {e}\n")
        import traceback
        traceback.print_exc()
        
    finally:
        # Desconectar
        print("🔌 Desconectando...")
        await client.disconnect()
        print("✅ Desconectado com sucesso\n")
    
    print("=" * 60)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 60)


async def test_multiple_orders():
    """Testa múltiplas ordens em sequência"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE MÚLTIPLAS ORDENS")
    print("=" * 60 + "\n")
    
    config = AvalonConfig(
        email=settings.quotex_email or "teste@email.com",
        password=settings.quotex_password or "senha123",
        environment="demo"
    )
    
    client = AvalonClient(config)
    
    try:
        await client.connect()
        
        orders = [
            ("EURUSD", "call", 10.0),
            ("GBPUSD", "put", 15.0),
            ("BTCUSD", "call", 20.0),
        ]
        
        wins = 0
        losses = 0
        total_profit = 0.0
        
        for symbol, side, amount in orders:
            print(f"📈 Executando: {symbol} {side.upper()} R${amount:.2f}")
            
            result = await client.place_order(symbol, side, amount, 60)
            
            if result["success"]:
                if result["win"]:
                    wins += 1
                    print(f"   ✅ WIN +R${result['profit']:.2f}")
                else:
                    losses += 1
                    print(f"   ❌ LOSS R${result['profit']:.2f}")
                
                total_profit += result["profit"]
            else:
                print(f"   ❌ Erro: {result.get('error')}")
            
            print()
        
        print("=" * 60)
        print(f"📊 RESULTADOS FINAIS:")
        print(f"   Vitórias: {wins}")
        print(f"   Derrotas: {losses}")
        print(f"   Taxa de acerto: {(wins / (wins + losses) * 100) if (wins + losses) > 0 else 0:.1f}%")
        print(f"   Lucro Total: R$ {total_profit:+.2f}")
        
        balance = await client.get_balance()
        print(f"   Saldo Final: R$ {balance['balance']:.2f}")
        print("=" * 60 + "\n")
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    print("\n🚀 Iniciando testes do Avalon Broker...\n")
    
    # Executar teste básico
    asyncio.run(test_connection())
    
    # Perguntar se quer testar múltiplas ordens
    try:
        response = input("\n❓ Deseja testar múltiplas ordens? (s/n): ").strip().lower()
        if response == 's':
            asyncio.run(test_multiple_orders())
        else:
            print("\n✅ Testes finalizados!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
    
    print("\n👋 Até logo!\n")
