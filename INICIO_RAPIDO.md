# 🎯 Início Rápido - Robo Trade + Quotex

## ⚡ Em 5 Minutos

### 1. **Preparar Credenciais** (2 min)
```
Acesse: https://quotex.io/
- Crie sua conta ou faça login
- Use o mesmo email e senha no .env
```

### 2. **Configurar .env** (1 min)
Abra `c:\Users\46\Desktop\ROBO TRADE\.env` e edite:
```ini
QUOTEX_EMAIL=seu_email
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
```

### 3. **Iniciar Sistema** (1 min)
```bash
# Opção A: Duplo clique em start_robo.bat
# Opção B: No terminal
python -m robo_trade.dashboard
```

### 4. **Acessar Painel** (1 min)
- Abra: http://127.0.0.1:5000
- Selecione modo: **"Simulação (Paper)"**
- Clique: **▶ Iniciar**

## 📋 Checklist

- [ ] Conta Quotex criada e verificada
- [ ] Email e senha preenchidos no .env
- [ ] .env preenchido
- [ ] Teste executado: `python test_quotex_connection.py`
- [ ] Painel iniciado: `python -m robo_trade.dashboard`
- [ ] Acesso ao painel: http://127.0.0.1:5000

## 🎮 Usando o Painel

### Modo Simulação (Paper)
- ✅ Teste sem risco
- ✅ Não usa créditos
- ✅ Ideal para aprender

Passos:
1. Selecione: **"Simulação (Paper)"**
2. Configure o par: ADA/USDT
3. Configure timeframe: 5m
4. Clique: **▶ Iniciar**

### Modo Real (Live)
- ⚠️ Coloca ordens REAIS
- 💰 Usa saldo da sua conta
- 🎯 Use APÓS testar Paper

Passos:
1. **PRIMEIRO**: Teste em Paper!
2. Selecione: **"Real (Live)"**
3. Clique: **▶ Iniciar**
4. Monitore operações

## 🐛 Problemas Comuns

### Painel não abre
```
Verifique: http://127.0.0.1:5000 está acessível?
Se não, execute: python -m robo_trade.dashboard
```

### Credentials não funcionam
```
Execute: python test_quotex_connection.py
Verifique se QUOTEX_EMAIL e QUOTEX_PASSWORD estão corretos
```

### Ordens não saem
```
1. Verifique se está em modo "Real" (não Paper)
2. Verifique se o par existe na Quotex (ADA/USDT existe?)
3. Monitore: data/robo_trade.log
```

## 📁 Estrutura de Arquivos

```
ROBO TRADE/
├── .env                          ← EDITE AQUI com suas credenciais
├── start_robo.bat                ← Duplo clique para iniciar
├── requirements.txt              ← Dependências Python
├── test_quotex_connection.py     ← Teste a integração
├── GUIA_QUOTEX.md               ← Guia completo (português)
├── QUOTEX_SETUP.md              ← Setup detalhado
├── robo_trade/
│   ├── dashboard.py             ← Painel web
│   ├── quotex.py                ← Cliente Quotex (API)
│   ├── broker.py                ← Abstração de broker
│   ├── config.py                ← Configurações
│   └── __main__.py
└── data/
    ├── martingale_operations.csv ← Histórico de operações
    └── robo_trade.log           ← Arquivo de logs
```

## 🔗 Links Úteis

- 📱 Quotex: https://quotex.io/
- 🐍 Python: https://www.python.org/
- 📚 CCXT (mercados): https://github.com/ccxt/ccxt
- 🧪 Teste integração: `python test_quotex_connection.py`

## 💡 Dicas

### Ganho Rápido (5-10 min)
```
Modo: Paper (Simulação)
Par: ADA/USDT
Timeframe: 1m
Operações por hora: 60
```

### Teste Completo (30-60 min)
```
Modo: Paper
Par: BTC/USDT
Timeframe: 5m
Operações por hora: 12
```

### Produção (Cuidado!)
```
Modo: Live
Par: EUR/USD
Timeframe: 15m
Operações por hora: 4
```

## ⚠️ Aviso Legal

- Trading envolve riscos significativos
- Use SEMPRE Paper antes de Live
- Monitore suas operações regularmente
- Nunca deixe rodando sem supervisão
- Mantenha cópia de segurança dos .env

---

**Pronto para começar?**
1. Execute: `python test_quotex_connection.py`
2. Abra: `start_robo.bat`
3. Acesse: http://127.0.0.1:5000

Boa sorte! 🚀
