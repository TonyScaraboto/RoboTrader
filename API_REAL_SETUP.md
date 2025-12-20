# 🔌 Configuração da API Real do Avalon Broker

## ⚠️ IMPORTANTE

O sistema agora está configurado para **tentar** se conectar à API real do Avalon Broker via WebSocket. Se a conexão falhar, ele automaticamente usa **modo simulado** como fallback.

## 🌐 URLs da API

Atualmente configuradas em `robo_trade/avalon.py`:

```python
AVALON_WS_URL = "wss://ws.avalonbroker.com/socket.io/?EIO=3&transport=websocket"
AVALON_API_URL = "https://api.avalonbroker.com"
```

### ⚙️ Como Descobrir as URLs Reais

1. **Abra o site do Avalon Broker** (https://avalonbroker.com)
2. **Abra DevTools** (F12)
3. **Vá para a aba Network**
4. **Filtre por WS** (WebSocket)
5. **Faça login no site**
6. **Copie a URL do WebSocket** que aparece

### Exemplo do que procurar:
```
wss://quotex.io/socket.io/?EIO=3&transport=websocket&sid=xxxxx
wss://qxbroker.com/websocket
wss://api.avalonbroker.com/realtime
```

## 📡 Estrutura de Mensagens WebSocket

### Autenticação
```json
{
  "type": "auth",
  "token": "seu_token_jwt",
  "demo": true
}
```

### Obter Saldo
```json
{
  "type": "get_balance",
  "demo": true
}
```

### Executar Ordem
```json
{
  "type": "place_order",
  "id": "AVL1234567890",
  "symbol": "EURUSD",
  "side": "call",
  "amount": 10.00,
  "expiration": 60,
  "demo": true
}
```

## 🔧 Como Atualizar as URLs

Edite o arquivo `robo_trade/avalon.py`:

```python
# Linha ~23-24
AVALON_WS_URL = "wss://SUA_URL_WEBSOCKET_AQUI"
AVALON_API_URL = "https://SUA_URL_API_AQUI"
```

## 🧪 Testando Conexão Real

1. **Configure as URLs corretas**
2. **Execute o teste**:

```python
from robo_trade.avalon import AvalonClient, AvalonConfig
import asyncio

async def test():
    config = AvalonConfig(
        email="seu@email.com",
        password="sua_senha",
        environment="demo"
    )
    
    client = AvalonClient(config)
    connected = await client.connect()
    
    if connected:
        print("✅ Conectado!")
        balance = await client.get_balance()
        print(f"Saldo: R$ {balance['balance']}")
        
        # Testar ordem
        result = await client.place_order(
            symbol="EURUSD",
            side="call",
            amount_brl=10.0,
            expiration_time=60
        )
        print(f"Ordem: {result}")
        
        await client.disconnect()
    else:
        print("❌ Falha na conexão")

asyncio.run(test())
```

## 📊 Monitoramento de Mensagens

Para ver as mensagens WebSocket em tempo real, aumente o nível de log:

```python
# No início do avalon.py
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Autenticação

### Opção 1: Token JWT
Se o Avalon usar tokens JWT, atualize o método `_authenticate()`:

```python
async def _authenticate(self) -> bool:
    async with aiohttp.ClientSession() as session:
        payload = {
            "email": self.config.email,
            "password": self.config.password
        }
        
        async with session.post(
            f"{AVALON_API_URL}/auth/login",
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                self._session_token = data["token"]
                return True
    return False
```

### Opção 2: Cookie/Session
Se usar cookies, modifique para guardar cookies:

```python
self._session_cookies = response.cookies
```

## 🚀 Modo de Operação Atual

### 1️⃣ Tentativa de Conexão Real
- Tenta autenticar via API REST
- Tenta conectar WebSocket
- Tenta fazer handshake

### 2️⃣ Fallback Automático
Se qualquer etapa falhar:
- ✅ Continua funcionando em **modo simulado**
- ✅ Mantém todas as funcionalidades
- ⚠️ Resultados são aleatórios (não reais)

### 3️⃣ Como Saber se Está em Modo Real

Verifique os logs do servidor:

```
✅ Conectado ao Avalon com sucesso   ← Modo REAL
ℹ️ Usando modo simulado (fallback)    ← Modo SIMULADO
```

Ou verifique o resultado da ordem:

```python
result = await client.place_order(...)
if result.get("simulated"):
    print("⚠️ Operação simulada")
else:
    print("✅ Operação real")
```

## 📱 Opções de Plataforma

### Se Avalon não tiver API pública:

#### Opção A: Usar PyQuotex
```python
# Já está instalado!
from quotex import Quotex

client = Quotex(email="...", password="...")
await client.connect()
await client.buy(10, "EURUSD", "call", 60)
```

#### Opção B: Usar Navegador Automatizado
```python
# Via Playwright (já instalado)
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto("https://avalonbroker.com")
    # Automatizar clicks...
```

#### Opção C: Engenharia Reversa
1. Usar Playwright em modo headless=False
2. Capturar todas as requisições WebSocket
3. Replicar o protocolo em Python

## 🛠️ Ferramentas de Debug

### 1. Wireshark
Para capturar tráfego WebSocket real

### 2. Chrome DevTools
- Network → WS
- Ver frames enviados/recebidos

### 3. Postman
Para testar endpoints REST

## 📝 Próximos Passos

1. ✅ **Descobrir URLs reais** do Avalon Broker
2. ✅ **Capturar formato das mensagens** WebSocket
3. ✅ **Atualizar `avalon.py`** com protocolo correto
4. ✅ **Testar em Demo** antes de usar real
5. ✅ **Validar resultados** comparando com plataforma web

## ⚠️ ATENÇÃO - Modo Real

Quando conectar à API real:

- 🚨 **SEMPRE teste em DEMO primeiro**
- 🚨 **NUNCA use quantias grandes inicialmente**
- 🚨 **Monitore os logs constantemente**
- 🚨 **Tenha stop-loss configurado**
- 🚨 **Verifique resultados manualmente**

---

**Status Atual**: ✅ Sistema pronto para integração, aguardando URLs corretas da API
