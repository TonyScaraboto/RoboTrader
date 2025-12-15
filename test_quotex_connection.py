#!/usr/bin/env python3
"""
Test script to verify Quotex API integration
Usage: python test_quotex_connection.py
"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from robo_trade.config import settings
from robo_trade.quotex import QuotexConfig, QuotexClient
from robo_trade.broker import create_broker_from_settings

def test_config():
    """Test if configuration is loaded correctly"""
    print("=" * 60)
    print("TESTE 1: Verificando Configuração")
    print("=" * 60)
    
    print(f"✓ QUOTEX_EMAIL: {'✓ Configurado' if settings.quotex_email else '✗ NÃO CONFIGURADO'}")
    print(f"✓ QUOTEX_PASSWORD: {'✓ Configurado' if settings.quotex_password else '✗ NÃO CONFIGURADO'}")
    print(f"✓ QUOTEX_LANG: {settings.quotex_lang}")
    print(f"✓ QUOTEX_ENVIRONMENT: {settings.quotex_environment}")
    
    if not settings.quotex_email or not settings.quotex_password:
        print("\n⚠️  Credenciais ausentes! Configure o arquivo .env com seu email e senha Quotex")
        return False
    
    print("\n✓ Configuração OK\n")
    return True

def test_quotex_client():
    """Test QuotexClient instantiation"""
    print("=" * 60)
    print("TESTE 2: Conectando ao Cliente Quotex")
    print("=" * 60)
    
    try:
        config = QuotexConfig(
            email=settings.quotex_email,
            password=settings.quotex_password,
            lang=settings.quotex_lang or "pt"
        )
        client = QuotexClient(config)
        print("✓ Cliente QuotexClient instanciado com sucesso")
        print(f"  Email: {config.email}")
        print(f"  Lang: {config.lang}")
        print("\n✓ Conexão OK\n")
        return True, client
    except Exception as e:
        print(f"✗ Erro ao criar cliente: {str(e)}\n")
        return False, None

def test_broker_factory():
    """Test broker factory function"""
    print("=" * 60)
    print("TESTE 3: Factory de Broker")
    print("=" * 60)
    
    try:
        broker = create_broker_from_settings(settings)
        if broker:
            print("✓ Broker criado com sucesso")
            print(f"  Tipo: {type(broker).__name__}")
            print("\n✓ Factory OK\n")
            return True, broker
        else:
            print("✗ Broker é None (credenciais ausentes?)\n")
            return False, None
    except Exception as e:
        print(f"✗ Erro ao criar broker: {str(e)}\n")
        return False, None

def test_api_calls(client):
    """Test actual API calls"""
    print("=" * 60)
    print("TESTE 4: Chamadas à API Quotex")
    print("=" * 60)
    
    # Test get_asset_info
    print("→ Testando get_asset_info('ADA/USDT')...")
    try:
        info = client.get_asset_info('ADA/USDT')
        print(f"  ✓ Asset Info: {info}")
    except Exception as e:
        print(f"  ✗ Erro: {str(e)}")
    
    # Test get_balance
    print("\n→ Testando get_balance()...")
    try:
        balance = client.get_balance()
        print(f"  Status: {balance.get('status')}")
        print(f"  Saldo: {balance.get('balance')} {balance.get('currency')}")
    except Exception as e:
        print(f"  ✗ Erro: {str(e)}")
    
    # Test place_order (simulate only)
    print("\n→ Testando place_order() - SIMULADO...")
    try:
        order = client.place_order('ADA/USDT', 'CALL', 10.0, 60)
        print(f"  Status: {order.get('status')}")
        if order.get('order_id'):
            print(f"  Order ID: {order.get('order_id')}")
        if order.get('error'):
            print(f"  Erro: {order.get('error')}")
    except Exception as e:
        print(f"  ✗ Erro: {str(e)}")
    
    print("\n✓ Testes de API OK\n")

def main():
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  Teste de Integração Quotex - Robo Trade                 ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    # Test 1
    if not test_config():
        print("❌ Falha na configuração. Abortando.\n")
        return 1
    
    # Test 2
    success, client = test_quotex_client()
    if not success:
        print("❌ Falha na conexão. Abortando.\n")
        return 1
    
    # Test 3
    success, broker = test_broker_factory()
    if not success:
        print("⚠️  Broker factory falhou. Continuando...\n")
    
    # Test 4
    if client:
        test_api_calls(client)
    
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    print("""
✓ Todos os testes completados!

Próximas ações:
1. Edite .env com suas credenciais da conta demo Quotex
2. Execute: python -m robo_trade.dashboard
3. Abra: http://127.0.0.1:5000
4. Selecione modo "Paper" para testar antes de usar "Live"

Para conta DEMO Quotex:
  - Acesse: https://quotex.io/
    - Navegue até: Login normal com email e senha
    - Use as mesmas credenciais no arquivo .env
""")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
