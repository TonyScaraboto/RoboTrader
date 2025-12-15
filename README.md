# 🚀 ROBO TRADE - Sistema de Trading Automático com Quotex

Trading bot com estratégia Martingale para a plataforma Quotex de opções binárias.

## ⚡ Início Rápido (5 min)

### 1. Configurar Credenciais
Edite `.env`:
```ini
QUOTEX_EMAIL=seu@email.com
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
```

### 2. Testar Integração
```bash
python test_quotex_connection.py
```

### 3. Iniciar Painel
```bash
python -m robo_trade.dashboard
# ou duplo clique: start_robo.bat
```

### 4. Acessar
```
http://127.0.0.1:5000
```

---

## 📚 Documentação

- **[PASSO_A_PASSO.md](PASSO_A_PASSO.md)** - Guia passo a passo (10 min)
- **[GUIA_QUOTEX.md](GUIA_QUOTEX.md)** - Documentação completa em pt-BR
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Quick start
- **[QUOTEX_SETUP.md](QUOTEX_SETUP.md)** - Setup detalhado

---

## 🎯 Funcionalidades

- ✅ **Integração Real com Quotex** - Usando biblioteca PyQuotex oficial
- ✅ **Paper & Live Modes** - Teste sem risco ou com real
- ✅ **Estratégia Martingale** - Sequência automática de apostas
- ✅ **Dashboard Web** - Painel interativo em tempo real
- ✅ **Gráficos Avançados** - Candlestick + Equity Curve
- ✅ **Histórico CSV** - Todas as operações registradas
- ✅ **Validação em Tempo Real** - Entrada segura
- ✅ **Logs Detalhados** - Rastreamento completo
- ✅ **Configuração Web** - Altere credenciais pela interface

---

## 📋 Pré-requisitos

- Python 3.8+
- Conta Quotex (demo ou real)
- Email e senha da sua conta Quotex
- Conexão com internet

---

## 🔧 Instalação

### 1. Clonar ou Baixar Projeto
```bash
cd c:\Users\46\Desktop\ROBO TRADE
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar .env
```bash
# Edite com suas credenciais Quotex
QUOTEX_EMAIL=seu@email.com
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
```

---

## 🚀 Uso

### Mode 1: Painel Web (Recomendado)
```bash
python -m robo_trade.dashboard
# Acesse: http://127.0.0.1:5000
# Configure suas credenciais em ⚙️ Configurações
```

### Mode 2: Linha de Comando
```bash
python test_quotex_connection.py  # Testar
```

---

## 🎮 Painel Web

### Funcionalidades
- 📊 Gráficos em tempo real (Candlestick + Equity)
- 🎛️ Seletor de Modo (Paper/Live)
- ⚙️ Configuração de Parâmetros
- 📈 Estatísticas ao vivo
- 🔄 Histórico de operações

### Controls
- **▶ Iniciar** - Começa o bot
- **⏹ Parar** - Para o bot
- **Par** - Ativo a negociar (ADA/USDT, BTC/USDT, etc)
- **Timeframe** - Intervalo de candle (1m, 5m, 15m, 1h, etc)
- **Payout** - Taxa de retorno (1-100%)

---

## 🏗️ Arquitetura

```
Dashboard (Web)
    ↓
Flask App
    ↓
BotRunner (Backtesting + Ordening)
    ↓
Broker Abstraction
    ↓
QuotexClient (HTTP API)
    ↓
Quotex Platform API
```

---

## 📁 Estrutura do Projeto

```
robo_trade/
├── dashboard.py      # Painel Flask + HTML
├── quotex.py         # Cliente Quotex
├── broker.py         # Abstração de Broker
├── config.py         # Configurações
└── __main__.py

data/
├── martingale_operations.csv  # Histórico
└── robo_trade.log            # Logs

.env                 # Credenciais (não comitar)
requirements.txt     # Dependências
start_robo.bat      # Script inicialização
```

---

## 🔐 Segurança

- Credenciais (email/senha) somente no `.env` local
- Nunca expostas em logs ou código
- `.env` no `.gitignore`
- Validação de entrada robusta

---

## 🐛 Troubleshooting

### Erro: "Email é obrigatório"
```
→ Verifique QUOTEX_EMAIL em .env
→ Execute: python test_quotex_connection.py
```

### Erro: "Senha é obrigatória"
```
→ Verifique QUOTEX_PASSWORD em .env
→ Tente login manual no site Quotex para validar senha
```

### Ordens não saem em Live
```
→ Verifique modo (deve ser "Real", não "Simulação")
→ Verifique internet e credenciais corretas
→ Consulte: data/robo_trade.log
```

### Painel não abre
```
→ Verifique porta 5000: netstat -ano | findstr :5000
→ Use outra porta: PORT=8000 python -m robo_trade.dashboard
```

---

## 📊 Operações

Cada operação é registrada em `data/martingale_operations.csv`:

```csv
timestamp,symbol,timeframe,direction,stake,side,win,profit_brl
2024-01-15 14:23:45,ADA/USDT,5m,UP,2.0,CALL,TRUE,1.7
2024-01-15 14:28:50,ADA/USDT,5m,DOWN,4.0,PUT,FALSE,-4.0
```

---

## 🎯 Estratégia Martingale

Sequência de apostas crescentes após perdas:
```
Stake 1: 2 BRL   (1ª tentativa)
Stake 2: 4 BRL   (se perder)
Stake 3: 10 BRL  (se perder 2x)
...até
Stake 8: 400 BRL (se perder 7x)
```

Reinicia ao ganhar (ciclo completo).

---

## ⚖️ Riscos

⚠️ **IMPORTANTE**:
- Trading envolve perda de capital
- Use apenas saldo que possa perder
- Teste em Paper antes de Live
- Monitore operações constantemente
- Implementar stop-loss é recomendado

---

## 📝 Logs

Consulte `data/robo_trade.log` para:
- Erros de API
- Detalhes de operações
- Status de conexão
- Warnings e alerts

---

## 🤝 Contribuições

Melhorias e correções são bem-vindas!

---

## 📜 Licença

Projeto open-source para fins educacionais.

---

## 📞 Suporte

Para dúvidas:
1. Consulte: [GUIA_QUOTEX.md](GUIA_QUOTEX.md)
2. Execute: `python test_quotex_connection.py`
3. Verifique: `data/robo_trade.log`

---

**Desenvolvido com ❤️ para Quotex Trading** 🚀

Leia [PASSO_A_PASSO.md](PASSO_A_PASSO.md) para começar AGORA!

⚠️ **WARNING: This uses REAL money!**

```bash
python -m robo_trade.trader live
```

### Dashboard

Launch the web dashboard at http://127.0.0.1:5000:

```bash
python -m robo_trade.dashboard
```

Or use the script:

```bash
scripts\run_dashboard.cmd
```

- Outputs: saves CSV of martingale operations to `data/martingale_operations.csv`.

```

```

Change mode via `.env` `MODE=paper|live` or CLI arg.

## Notes
- This is a scaffold; paper/live are stubs.
- Uses `ccxt` for exchange access.
- Default symbol: `BTC/USDT`.
- Martingale sequence per user rules: stakes BRL [2,4,10,20,50,100,200,400]; resets on victory.
