# 🚀 Guia Completo: Integração Quotex com Robo Trade

## 1️⃣ Criar Conta Demo Quotex

### Passo 1: Registrar-se
1. Acesse https://quotex.io/
2. Clique em "Registar-se" / "Sign Up"
3. Preencha com email e crie senha
4. Confirme o email

### Passo 2: Acessar Configurações
1. Faça login na sua conta
2. Clique no ícone de **Perfil** (canto superior direito)
3. Selecione **Configurações**

## 2️⃣ Confirmar Credenciais de Login

Você usará o mesmo email e senha que já utiliza para entrar na Quotex.

### Checklist
1. Tem acesso ao email cadastrado? (verifique caixa de entrada)
2. Sabe a senha atual? (faça login em https://quotex.io/ para confirmar)
3. (Opcional) Defina o idioma padrão no `.env` via `QUOTEX_LANG=pt|en|es`

## 3️⃣ Configurar Robo Trade

### Editar .env
Na raiz do projeto (c:\Users\46\Desktop\ROBO TRADE\.env):

```ini
# Substituir pelos seus valores (login por email/senha)
QUOTEX_EMAIL=seu_email
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
QUOTEX_ENVIRONMENT=demo

# Outras configurações
SYMBOL=ADA/USDT
EXPIRATION_TIME=60
PAYOUT_RATIO=85
INITIAL_BALANCE_BRL=1000
```

⚠️ **NÃO COMPARTILHE SUA SENHA!**

## 4️⃣ Testando a Integração

### Verificar Configuração
```bash
python test_quotex_connection.py
```

Resultado esperado:
```
✓ QUOTEX_EMAIL: ✓ Configurado
✓ QUOTEX_PASSWORD: ✓ Configurado
✓ Cliente QuotexClient instanciado com sucesso
✓ Broker criado com sucesso
```

## 5️⃣ Iniciar o Robô

### Modo Paper (Recomendado para teste)
```bash
python -m robo_trade.dashboard
```

Abra: http://127.0.0.1:5000

No painel:
1. Selecione modo: **"Simulação (Paper)"**
2. Configure: Par, Timeframe, Payout
3. Clique: **▶ Iniciar**

### Modo Live (Real)
⚠️ **Use SOMENTE após testar no Paper!**

1. Selecione modo: **"Real (Live)"**
2. Clique: **▶ Iniciar**
3. O robô colocará ordens reais na sua conta demo

## 🎯 Ativos Suportados

Quotex oferece trading em:
- **Criptomoedas**: BTC, ETH, ADA, XRP, etc.
- **Forex**: EUR/USD, GBP/USD, USD/JPY, etc.
- **Commodities**: Ouro, Petróleo, etc.
- **Índices**: SP500, CRYPTO_INDEX, etc.

Use o formato: `BTC/USDT`, `EUR/USD`, etc.

## 📊 Configuração Recomendada

### Para Iniciantes (Paper)
```
Par: ADA/USDT
Timeframe: 5m
Payout: 85%
Modo: Simulação
```

### Para Testes (Paper com mais estresse)
```
Par: BTC/USDT
Timeframe: 1m
Payout: 80%
Modo: Simulação
```

### Para Produção (Live - CUIDADO!)
```
Par: EUR/USD
Timeframe: 15m
Payout: 85%
Modo: Real
```

## 🐛 Troubleshooting

### Erro: "Email is required"
```
❌ QUOTEX_EMAIL não está no .env
✅ Edite .env e adicione: QUOTEX_EMAIL=seu_email
```

### Erro: "Password is required"
```
❌ QUOTEX_PASSWORD não está no .env
✅ Edite .env e adicione: QUOTEX_PASSWORD=sua_senha
```

### Erro: "Failed to resolve 'api.quotex.io'"
```
❌ Sem conexão com a internet
✅ Verifique sua conexão e tente novamente
```

### Ordens não são colocadas
```
❌ Modo pode estar em "Simulação" em vez de "Real"
✅ Verifique o selector de modo no painel
✅ Verifique email/senha estão corretos no .env
✅ Verifique se o par é negociado (está aberto)
```

### Saldo mostra como 0 BRL
```
⚠️ Isso é normal se a API não responder
✅ Em modo Paper, o saldo é simulado
✅ Em modo Live, verifique sua conta Quotex
```

## 🔒 Segurança

### Boas Práticas
- ✅ Guarde .env apenas localmente
- ✅ Nunca comite .env no git
- ✅ Use conta DEMO para testes
- ✅ Monitore suas operações
- ✅ Teste Paper antes de Live

### Em Produção
- ✅ Use variáveis de ambiente do sistema
- ✅ Troque a senha periodicamente
- ✅ Implemente 2FA na conta Quotex
- ✅ Tenha um mecanismo de parada de emergência
- ✅ Mantenha logs detalhados

## 📈 Monitorar Operações

### Painel Web
- Equidade: Gráfico em tempo real
- Ganhos/Perdas: Estatísticas ao vivo
- Histórico: CSV em `data/martingale_operations.csv`

### Arquivo de Log
```
data/robo_trade.log
```

Contém todos os eventos e erros.

## 🛑 Parar o Robô

### No Painel
Clique em **⏹ Parar**

### Via Terminal
```
Ctrl+C
```

## 📞 Suporte

Se tiver problemas:

1. Verifique `data/robo_trade.log`
2. Execute o teste: `python test_quotex_connection.py`
3. Verifique documentação: `QUOTEX_SETUP.md`
4. Abra issue no repositório

---

**Lembre-se**: Trading envolve riscos. Use a função de "Paper" para praticar!
