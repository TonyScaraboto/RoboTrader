#!/usr/bin/env python3
"""Script para testar todas as funcionalidades do dashboard"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_main_page():
    """Testa se a página principal carrega corretamente"""
    print("🧪 Testando página principal...")
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200 and "Robo Trade" in r.text:
            print("✅ Página principal carregada com sucesso")
            return True
        else:
            print(f"❌ Erro ao carregar página: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_summary_route():
    """Testa a rota /summary"""
    print("\n🧪 Testando rota /summary...")
    try:
        r = requests.get(f"{BASE_URL}/summary")
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Summary recebido:")
            print(f"  - Operações: {data.get('ops_count', 0)}")
            print(f"  - Ganhos: {data.get('wins', 0)}")
            print(f"  - Perdas: {data.get('losses', 0)}")
            print(f"  - Lucro Total: {data.get('total_profit', 0)}")
            print(f"  - Status do Bot: {data.get('bot', {}).get('status', 'desconhecido')}")
            print(f"  - Saldo: {data.get('account', {}).get('balance_brl', 0)}")
            print(f"  - Candles: {len(data.get('candles', []))} candles")
            print(f"  - Equity Curve: {len(data.get('equity_curve', []))} pontos")
            return True
        else:
            print(f"❌ Erro: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_start_bot():
    """Testa iniciar o robô"""
    print("\n🧪 Testando inicialização do robô...")
    try:
        payload = {
            "symbol": "ADA/USDT",
            "timeframe": "5m",
            "payout": 80.0
        }
        r = requests.post(f"{BASE_URL}/start", json=payload)
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Robô iniciado com sucesso")
            print(f"  - Status: {data.get('status')}")
            print(f"  - Symbol: {data.get('symbol')}")
            print(f"  - Timeframe: {data.get('timeframe')}")
            print(f"  - Payout: {data.get('payout')}")
            return True
        else:
            print(f"❌ Erro: {r.status_code}")
            print(f"Resposta: {r.text}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_stop_bot():
    """Testa parar o robô"""
    print("\n🧪 Testando parada do robô...")
    try:
        r = requests.post(f"{BASE_URL}/stop")
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Robô parado com sucesso")
            print(f"  - Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Erro: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_validation():
    """Testa validação de inputs"""
    print("\n🧪 Testando validação de inputs...")
    
    # Testar symbol inválido (será aceito pelo servidor, validação é cliente-side)
    print("\n  - Testando symbol inválido...")
    try:
        payload = {"symbol": "INVALID", "timeframe": "5m", "payout": 50}
        r = requests.post(f"{BASE_URL}/start", json=payload)
        print(f"    ℹ️ Servidor respondeu com {r.status_code} (validação é cliente-side)")
    except Exception as e:
        print(f"    ⚠️ {e}")
    
    # Testar timeframe válido
    print("\n  - Testando timeframes válidos...")
    for tf in ["1m", "5m", "15m", "1h", "4h", "1d"]:
        try:
            payload = {"symbol": "ADA/USDT", "timeframe": tf, "payout": 50}
            r = requests.post(f"{BASE_URL}/start", json=payload, timeout=2)
            print(f"    ✅ Timeframe {tf}: OK")
            time.sleep(0.5)
        except Exception as e:
            print(f"    ❌ Timeframe {tf}: {e}")
    
    # Testar payout válido
    print("\n  - Testando payout válido...")
    try:
        payload = {"symbol": "ADA/USDT", "timeframe": "5m", "payout": 75.5}
        r = requests.post(f"{BASE_URL}/start", json=payload)
        print(f"    ✅ Payout 75.5%: OK ({r.status_code})")
    except Exception as e:
        print(f"    ❌ {e}")

def main():
    print("=" * 60)
    print("🤖 TESTE COMPLETO DO DASHBOARD - ROBO TRADE")
    print("=" * 60)
    
    results = []
    
    # Testes básicos
    results.append(("Página Principal", test_main_page()))
    time.sleep(1)
    
    results.append(("Summary Route", test_summary_route()))
    time.sleep(1)
    
    # Testes de funcionalidade
    results.append(("Iniciar Bot", test_start_bot()))
    time.sleep(2)
    
    results.append(("Validação", test_validation()))
    time.sleep(1)
    
    results.append(("Parar Bot", test_stop_bot()))
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam")

if __name__ == "__main__":
    main()
