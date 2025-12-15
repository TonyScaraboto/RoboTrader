# Robo Trade - Integração Quotex Demo

Sistema de trading automático martingale para plataforma Quotex com painel web.

## 🚀 Início Rápido

### 1. Obter Credenciais (Email/Senha) da Conta Quotex

Para usar este robô com sua conta demo da Quotex:

1. **Acesse sua conta** em https://quotex.io/
2. **Use o mesmo email e senha** que você usa para login
3. (Opcional) Ajuste o idioma: `QUOTEX_LANG` (pt/en/es)

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto:

```bash
# Quotex Demo Account Credentials (email/senha)
QUOTEX_EMAIL=seu_email
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
QUOTEX_ENVIRONMENT=demo

# Trading Configuration
SYMBOL=ADA/USDT
EXPIRATION_TIME=60
PAYOUT_RATIO=85
INITIAL_BALANCE_BRL=1000
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar o Sistema

```bash
python -m robo_trade.dashboard
```

O painel estará disponível em: **http://127.0.0.1:5000**

## 📊 Funcionalidades

- **Estratégia Martingale**: Sequência automática de apostas 2, 4, 10, 20, 50, 100, 200, 400 BRL
- **Paper Trading**: Teste sem risco (modo simulação)
- **Live Trading**: Operar na conta demo Quotex em tempo real
- **Gráficos Avançados**: Candlestick + Equity Curve
- **Validação em Tempo Real**: Padrão XXX/YYY, timeframes, payout
- **Histórico CSV**: Todas as operações salvas em `data/martingale_operations.csv`

## 🎯 Modos de Operação

### Paper (Simulação)
- Ideal para testes
- Não coloca ordens reais
- Usa dados do histórico CCXT

### Live (Real)
- Coloca ordens reais na conta demo Quotex
- Use com cuidado em produção
- Requer login válido (email/senha)

## 📈 Configuração da Estratégia

No painel, configure:

- **Par**: ADA/USDT, BTC/USDT, EUR/USD, etc.
- **Timeframe**: 1m, 5m, 15m, 1h, 4h, 1d
- **Payout**: Taxa de retorno esperada (1-100%)

## 🔒 Segurança

⚠️ **IMPORTANTE**: 
- Nunca compartilhe sua senha da Quotex
- Guarde-a apenas no `.env` local
- Para ambientes de produção, use variáveis de ambiente seguras

## 📝 Troubleshooting

### "Quotex email is required"
Verifique se `QUOTEX_EMAIL` está configurado no `.env`

### "Quotex password is required"
Verifique se `QUOTEX_PASSWORD` está configurado no `.env`

### Conexão recusada em http://127.0.0.1:5000
Verifique se a porta 5000 não está em uso:
```bash
netstat -ano | findstr :5000
```

### Ordens não estão sendo colocadas
1. Verifique se o modo está em "Live" (não Paper)
2. Confirme email/senha no dashboard ou `.env`
3. Verifique logs: `data/robo_trade.log`

## 📚 Estrutura do Projeto

```
robo_trade/
├── dashboard.py      # Painel web + Flask
├── quotex.py         # Cliente da API Quotex
├── broker.py         # Abstração de broker
├── config.py         # Configurações
├── __init__.py
└── __main__.py
data/
├── martingale_operations.csv  # Histórico de operações
└── robo_trade.log            # Logs da aplicação
.env                  # Credenciais (não comitar)
```

## 🤝 Contribuições

Melhorias e correções são bem-vindas!

---

**Aviso Legal**: Este é um robô experimental. Use por sua conta e risco. Trading com alavancagem envolve riscos significativos.
