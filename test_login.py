"""
Script de teste para validar login no Avalon Broker
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_login():
    """Testa endpoint de login"""
    print("🧪 Testando login no Avalon Broker...")
    
    # Dados de teste
    data = {
        'email': 'teste@avalon.com',
        'password': 'senha123',
        'environment': 'demo'
    }
    
    # Fazer login
    response = requests.post(f"{BASE_URL}/login", data=data)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200 and response.json().get('success'):
        print("\n✅ Login bem-sucedido!")
        
        # Testar acesso a rota protegida
        cookies = response.cookies
        protected_response = requests.get(f"{BASE_URL}/check-auth", cookies=cookies)
        print(f"\nStatus de autenticação: {json.dumps(protected_response.json(), indent=2)}")
        
        return True
    else:
        print("\n❌ Login falhou!")
        return False

def test_protected_route_without_login():
    """Testa acesso a rota protegida sem login"""
    print("\n🧪 Testando acesso sem login...")
    
    response = requests.get(f"{BASE_URL}/summary")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Proteção funcionando - acesso negado sem login")
    else:
        print("❌ Proteção falhou - rota acessível sem login")

def test_check_auth():
    """Testa endpoint de verificação de autenticação"""
    print("\n🧪 Testando /check-auth sem sessão...")
    
    response = requests.get(f"{BASE_URL}/check-auth")
    
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if not response.json().get('logged_in'):
        print("✅ Sessão não autenticada corretamente detectada")
    else:
        print("❌ Erro: usuário aparece como logado sem fazer login")

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 TESTE DO SISTEMA DE LOGIN - AVALON BROKER")
    print("=" * 60)
    
    # Teste 1: Verificar autenticação inicial
    test_check_auth()
    
    # Teste 2: Tentar acessar rota protegida sem login
    test_protected_route_without_login()
    
    # Teste 3: Fazer login
    test_login()
    
    print("\n" + "=" * 60)
    print("✅ Todos os testes concluídos!")
    print("=" * 60)
