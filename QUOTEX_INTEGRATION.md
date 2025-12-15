# Integração com Quotex

Este documento descreve a integração do Robo Trade com a plataforma Quotex de opções binárias.

## Configuração

### 1. Obter Credenciais Quotex

Você precisará das credenciais de login da sua conta Quotex:

- **QUOTEX_EMAIL**: Email que você usa para acessar a Quotex
- **QUOTEX_PASSWORD**: Senha que você usa para acessar a Quotex
- (Opcional) **QUOTEX_LANG**: Idioma (`pt`, `en`, `es`)

### 2. Configurar .env

Crie ou edite o arquivo `.env` na raiz do projeto:

```env
# Quotex Platform Configuration (login por email/senha)
QUOTEX_EMAIL=seu_email
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
QUOTEX_ENVIRONMENT=demo

# Trading Settings
INITIAL_BALANCE_BRL=1000
PAYOUT_RATIO=85.0
EXPIRATION_TIME=60

# Exchange (for candle data)
EXCHANGE=binance
SYMBOL=ADA/USDT
```

## Arquitetura

### Arquivo: `robo_trade/quotex.py`

Contém a implementação do cliente Quotex:

- **QuotexConfig**: Configuração da plataforma (URL, credenciais)
- **QuotexClient**: Cliente para interagir com a API Quotex

### Métodos Disponíveis

#### `place_order(symbol, side, amount_brl, expiration_time)`

Coloca uma ordem de opção binária.

**Parâmetros:**
- `symbol`: Par de trading (ex: 'ADA/USDT')
- `side`: 'CALL' (compra/sobe) ou 'PUT' (venda/desce)
- `amount_brl`: Valor em BRL da operação
- `expiration_time`: Tempo de expiração em segundos (padrão: 60)

**Retorna:**
```python
{
    "status": "simulated",
    "platform": "quotex",
    "symbol": "ADA/USDT",
    "side": "CALL",
    "amount_brl": 2.0,
   "expiration_time": 60,
   "email": "..."
}
```

#### `get_asset_info(symbol)`

Obtém informações sobre um ativo.

**Retorna:**
```python
{
    "symbol": "ADA/USDT",
    "is_open": True,
    "min_amount": 1.0,
    "max_amount": 10000.0,
    "payout": 85.0
}
```

#### `get_balance()`

Obtém o saldo da conta.

**Retorna:**
```python
{
    "balance": 1000.0,
    "currency": "BRL",
   "email": "..."
}
```

## Estratégia Martingale

A estratégia implementada segue a lógica:

1. **Sequência de Stakes**: [2, 4, 10, 20, 50, 100, 200, 400] BRL
2. **Direção**: Baseada na cor do candle anterior
   - Verde (close > open): CALL (aposta na alta)
   - Vermelho (close < open): PUT (aposta na baixa)
3. **Vitória**: Reseta para o stake inicial (2 BRL)
4. **Derrota**: Avança para o próximo stake da sequência
5. **Payout**: Configurável (padrão 85%)

## Modos de Operação

### Backtest

Testa a estratégia com dados históricos:

```bash
python -m robo_trade.trader martingale_backtest
```

### Paper Trading

Simula operações sem dinheiro real:

```bash
python -m robo_trade.trader paper
```

### Live Trading

**⚠️ ATENÇÃO: Usa dinheiro real!**

```bash
python -m robo_trade.trader live
```

Requer confirmação digitando 'YES'.

## Dashboard

O dashboard Flask permite visualizar:

- Saldo atual
- Total de operações
- Ganhos/Perdas
- Lucro total
- Gráfico de Equity
- Gráfico de Candlestick
- Tabela de operações

Acesse em: http://127.0.0.1:5000

## Diferenças da HomeBroker

### Mudanças Principais

1. **Arquivo renomeado**: `homebroker.py` → `quotex.py`
2. **Classes renomeadas**: 
   - `HomeBrokerConfig` → `QuotexConfig`
   - `HomeBrokerClient` → `QuotexClient`
3. **Configurações novas**:
   - `QUOTEX_EMAIL` / `QUOTEX_PASSWORD` (login)
   - `QUOTEX_LANG` (idioma)
   - `QUOTEX_ENVIRONMENT` (demo/live)
   - `EXPIRATION_TIME` (novo)
4. **Payout**: Mudou de 1.0 (100%) para 85.0 (85% padrão da Quotex)
5. **Parâmetros novos**: `expiration_time` em `place_order()`

## Implementação Futura

Atualmente os métodos estão em modo **simulação**. Para integração real:

1. Obter documentação oficial da API Quotex
2. Validar autenticação via login (email/senha) ou fluxo oficial da Quotex
3. Implementar endpoints reais:
   - POST `/api/v1/options/open` - Abrir posição
   - GET `/api/v1/account/balance` - Consultar saldo
   - GET `/api/v1/assets/{symbol}` - Informações do ativo
   - WebSocket para dados em tempo real
4. Adicionar tratamento de erros
5. Implementar rate limiting
6. Adicionar logs detalhados

## Segurança

- ✅ Credenciais em arquivo `.env` (não commitado)
- ✅ Validação de entrada no dashboard
- ✅ Confirmação obrigatória para modo live
- ⚠️ TODO: Implementar SSL/TLS para API
- ⚠️ TODO: Criptografar credenciais sensíveis
- ⚠️ TODO: Implementar 2FA

## Suporte

Para dúvidas sobre a integração, consulte:
- Documentação oficial da Quotex API
- README.md do projeto
- Código em `robo_trade/quotex.py`
