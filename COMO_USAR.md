# 📖 Como Usar o ROBO TRADE com Quotex

## 🎯 Visão Geral

O **ROBO TRADE** é um robô de trading automatizado que opera em tempo real na plataforma **Quotex** (opções binárias). Ele pode executar operações em **modo simulação (Paper)** ou **modo ao vivo (Live)**.

---

## 🚀 INÍCIO RÁPIDO (5 minutos)

### 1️⃣ Iniciar o Sistema

**Opção A: Duplo clique (Recomendado para Windows)**
```
c:\Users\46\Desktop\ROBO TRADE\start_robo.bat
```

**Opção B: Terminal PowerShell**
```powershell
cd "c:\Users\46\Desktop\ROBO TRADE"
python -m robo_trade.dashboard
```

**Resultado esperado:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

### 2️⃣ Acessar o Painel (Dashboard)

Após iniciar, abra seu navegador e acesse:

```
http://127.0.0.1:5000
```

Você verá a interface como na imagem em anexo com:
- **Controle do Robô** (esquerda)
- **Conta/Saldo** (direita)
- **Gráficos** em tempo real
- **Histórico de Operações** (tabela)

---

## 🎮 Usando o Painel

### Seção: Controle do Robô

```
┌─────────────────────────────────┐
│   CONTROLE DO ROBÔ              │
├─────────────────────────────────┤
│ Par:       [ ADA/USDT        ]  │
│ Timeframe: [ 5m              ]  │
│ Payout:    [ 1.00            ]  │
│                                 │
│ [▶ Iniciar]  [⏹ Parar]         │
└─────────────────────────────────┘
```

#### **Par (Símbolo)**
Define qual ativo será negociado.

**Exemplos de pares válidos:**
- `ADA/USDT` - Cardano
- `BTC/USDT` - Bitcoin
- `ETH/USDT` - Ethereum
- `EUR/USD` - Euro/Dólar
- `XAU/USD` - Ouro

```
❓ Como escolher:
• Comece com pares líquidos (BTC, ETH, EUR/USD)
• Evite pares muito voláteis se está testando
• Verifique a disponibilidade na Quotex
```

#### **Timeframe**
Intervalo de tempo de cada vela do gráfico.

**Opções:**
- `1m` - 1 minuto (muito rápido)
- `5m` - 5 minutos ⭐ **(RECOMENDADO)**
- `15m` - 15 minutos (mais estável)
- `30m` - 30 minutos
- `1h` - 1 hora (para estratégias de longo prazo)

```
📊 Dica:
• 5m é equilibrado entre velocidade e confiabilidade
• Timeframes menores = mais operações
• Timeframes maiores = menos ruído
```

#### **Payout**
Taxa de retorno de cada operação ganhadora.

**Exemplos:**
- `0.85` = 85% de lucro se acertar
- `1.00` = 100% de lucro (retorno duplo)
- `1.50` = 150% de lucro

```
💰 Como funciona:
• Se ganhar com payout 0.85 em aposta de R$100:
  → Ganho: R$85 + R$100 = R$185
• Se perder:
  → Perda: R$100
```

---

### Botões de Controle

#### **▶ Iniciar**
Começa a executar operações automaticamente.

```
Ao clicar:
1. Robô se conecta à API Quotex
2. Começa a analisar o gráfico
3. Executa operações conforme estratégia
4. Atualiza saldo em tempo real
```

#### **⏹ Parar**
Interrompe o robô imediatamente.

```
Ao clicar:
1. Robô cessa novas operações
2. Operações em andamento são finalizadas
3. Saldo permanece salvo no histórico
```

---

## 📊 Entendendo o Painel

### Seção: Conta

```
┌──────────────────────┐
│ Saldo Inicial        │
│ R$ 1.000,00          │
├──────────────────────┤
│ Saldo Atual          │
│ R$ 1.148,00          │
└──────────────────────┘
```

- **Saldo Inicial**: Configurado em `.env` (INITIAL_BALANCE_BRL)
- **Saldo Atual**: Atualizado em tempo real após cada operação

### Métricas de Performance

```
┌─────────────────┬──────────────┬──────────────┐
│ Total de Ops    │ Ganhos       │ Perdas       │
│ 300             │ 195 (65%)    │ 105 (35%)    │
└─────────────────┴──────────────┴──────────────┘

Lucro Total: R$ 2.148,00 ✅
```

- **Total de Operações**: Quantas ordens foram executadas
- **Ganhos**: Operações vencedoras
- **Perdas**: Operações perdedoras
- **Win Rate**: Percentual de acerto
- **Lucro Total**: Ganhos - Perdas

---

### 📈 Gráficos em Tempo Real

#### **Equity (Patrimônio)**
```
     R$ 1500 │     ╱╲
     R$ 1400 │    ╱  ╲   ╱╲
     R$ 1300 │   ╱    ╲ ╱  ╲
     R$ 1200 │  ╱      ╱
     R$ 1100 │ ╱
     R$ 1000 └───────────────
              Tempo →
```

**O que significa:**
- Linha verde = crescimento do saldo
- Linha vermelha = queda do saldo
- Mostra evolução em tempo real do patrimônio

**Como interpretar:**
- Tendência para cima = sistema lucrativo ✅
- Oscilações = normal (parte do risco)
- Queda constante = revisar estratégia ⚠️

#### **Candlestick (Preço do Ativo)**
```
  │ ▁▂▃ ╭─╮     Corpo = diferença open/close
  │ ┃█┃ │▌│     Pavio = máx/mín
  │ ┃█┃ │▌│     Verde = alta ↗️
  │ ▔▕▔ ╰─╯     Vermelho = baixa ↘️
  └──────────
```

**Como usar:**
- Candles verdes = preço subindo
- Candles vermelhos = preço caindo
- Ajuda a validar as decisões do robô

---

### 📋 Tabela de Operações

```
Index │ Entry Dir │ Candle Dir │ Stake │ Win  │ Profit
──────┼───────────┼────────────┼───────┼──────┼────────
  100 │ green     │ red        │  10   │ ❌   │ -10
  101 │ green     │ red        │  20   │ ❌   │ -20
  102 │ green     │ red        │  50   │ ❌   │ -50
  103 │ green     │ red        │ 100   │ ❌   │ -100
  104 │ green     │ green      │ 200   │ ✅   │ +200
```

**Entendendo cada coluna:**

| Coluna | Significado |
|--------|------------|
| **Index** | Número sequencial da operação |
| **Entry Dir** | Direção predita (CALL=green/PUT=red) |
| **Candle Dir** | Direção real (o que aconteceu) |
| **Stake** | Valor em BRL apostado |
| **Win** | ✅ Ganhou ou ❌ Perdeu |
| **Profit** | Lucro ou prejuízo em BRL |

**Leitura rápida:**
- ✅ Coluna verde = Operação vencedora
- ❌ Coluna vermelha = Operação perdedora
- Valor positivo = lucro
- Valor negativo = perda

---

## ⚙️ Configurações Avançadas

### Acessar Arquivo de Configuração

Edite `.env` para ajustar parâmetros:

```bash
c:\Users\46\Desktop\ROBO TRADE\.env
```

### Parâmetros Importantes

#### **Modo de Operação**
```env
# Simulação (Paper Trading) - SEM RISCO
MODE=paper

# Ao Vivo (Live Trading) - COM RISCO DE PERDA
MODE=live
```

```
⚠️ AVISO:
• Sempre comece com MODE=paper
• Só use MODE=live após testar extensamente
• Mode=live usa DINHEIRO REAL
```

#### **Credenciais Quotex**
```env
QUOTEX_EMAIL=seu_email
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
QUOTEX_ENVIRONMENT=demo  # ou 'live'
```

#### **Configurações de Martingale**
```env
INITIAL_BALANCE_BRL=1000      # Saldo inicial
PAYOUT_RATIO=0.85            # Taxa de retorno
EXPIRATION_TIME=60            # Tempo da operação (segundos)
```

---

## 🔄 Fluxo de uma Operação

### Passo a Passo

```
1. ANÁLISE
   ↓ Robô analisa o gráfico
   ↓ Detecta padrão (preço subindo/descendo)
   
2. DECISÃO
   ↓ Decide: CALL (aposta em alta) ou PUT (aposta em baixa)
   ↓ Calcula valor da aposta
   
3. EXECUÇÃO
   ↓ Envia ordem para API Quotex
   ↓ Quotex abre a operação
   
4. ESPERA
   ↓ Robô aguarda expiração (normalmente 60s)
   
5. RESULTADO
   ↓ Verifica se acertou ou errou
   ↓ Atualiza saldo
   ↓ Registra no histórico
   
6. PRÓXIMA
   ↓ Volta ao passo 1
```

### Exemplo Prático

```
OPERAÇÃO #104:
├─ Par: ADA/USDT
├─ Hora: 14:35:20
├─ Decisão: CALL (preço vai subir)
├─ Aposta: R$ 200
├─ Expiração: 60 segundos
│
├─ Resultado: ✅ ACERTOU!
│  Preço fechou mais alto
│  Ganho: 200 × 1.00 = R$ 200
│
└─ Novo Saldo: R$ 1.200,00 (era 1.000,00)
```

---

## 🛡️ Modos de Operação

### Modo Paper (Simulação)

```
✅ Vantagens:
• SEM RISCO - usa dinheiro fictício
• Testa a estratégia sem perder dinheiro
• Ideal para aprender o sistema

⚠️ Cuidado:
• Resultados simulados podem diferir do real
• Spread/latência não são emulados
```

**Como usar:**
```
1. Edite .env: MODE=paper
2. Clique em [▶ Iniciar]
3. Observar operações sem risco
4. Verificar se ganha ou perde
```

### Modo Live (Ao Vivo)

```
⚠️ CUIDADO:
• USA DINHEIRO REAL da sua conta Quotex
• Possibilidade de perder investimento
• SÓ USE APÓS VALIDAR EM PAPER

✅ Vantagens:
• Operações reais com spreads reais
• Ganhos reais (se der lucro)
```

**Como usar:**
```
1. Valide extensamente em MODE=paper
2. Edite .env: MODE=live
3. Edite .env: QUOTEX_ENVIRONMENT=live
4. Comece com saldo pequeno (ex: R$ 100)
5. Clique em [▶ Iniciar]
6. Monitore constantemente
```

---

## 🔧 Troubleshooting (Resolução de Problemas)

### Problema: "Connection refused" ao acessar http://127.0.0.1:5000

```
❌ Erro: Cannot connect to server

✅ Solução:
1. Verifique se o servidor está rodando
   → Terminal deve mostrar:
     * Running on http://127.0.0.1:5000

2. Se não estiver rodando:
   → Execute: python -m robo_trade.dashboard
   
3. Aguarde 2-3 segundos
4. Recarregue a página (F5)
```

### Problema: "Credenciais inválidas"

```
❌ Erro: Login falhou (email/senha)

✅ Solução:
1. Abra https://quotex.io/
2. Confirme que consegue entrar com seu email e senha
3. Edite .env e ajuste:
   QUOTEX_EMAIL=seu_email
   QUOTEX_PASSWORD=sua_senha
4. Salve o arquivo
5. Reinicie o servidor
```

### Problema: Robô não faz operações

```
❌ Robô iniciou mas não executa operações

✅ Solução:
1. Verifique saldo em .env:
   INITIAL_BALANCE_BRL=1000  (deve ser > 0)

2. Verifique par válido:
   SYMBOL=ADA/USDT  (valid no Quotex)

3. Verifique modo:
   MODE=paper  (comece em paper)

4. Verifique logs no terminal (procure por erros)

5. Se nada funcionar:
   → Execute: python test_quotex_connection.py
   → Isso testa a conexão com a API
```

### Problema: Saldo não atualiza

```
❌ Saldo congelado/não muda

✅ Solução:
1. Robô pode estar pausado - clique [▶ Iniciar]
2. Recarregue a página: F5
3. Verifique conexão com Quotex:
   → python test_quotex_connection.py
4. Se persistir, reinicie o servidor:
   → Feche terminal (Ctrl+C)
   → Execute novamente: python -m robo_trade.dashboard
```

---

## 📊 Interpretando Resultados

### Taxa de Acerto (Win Rate)

```
Win Rate = (Ganhos / Total) × 100

Exemplo:
• 195 ganhos em 300 operações
• Win Rate = (195/300) × 100 = 65%
```

**Interpretação:**

| Taxa | Significado |
|------|------------|
| < 50% | Perdendo mais do que ganhando ❌ |
| 50-55% | Viável (com payout > 0.85) ⚠️ |
| 55-65% | Bom desempenho ✅ |
| > 65% | Excelente desempenho 🎉 |

```
⚠️ Importante:
Mesmo com 65% de acerto, é possível perder dinheiro
se o payout for muito baixo!

Cálculo do break-even:
payout_necessário = (100 / taxa_acerto) - 1
```

### Lucro/Prejuízo

```
Lucro = Ganhos - Perdas

Exemplo:
• Ganhos: 195 × 85 = R$ 16.575
• Perdas: 105 × 100 = R$ 10.500
• Lucro: R$ 6.075

Retorno %:
Retorno = (Lucro / Saldo Inicial) × 100
Retorno = (6.075 / 1.000) × 100 = 607.5%
```

---

## 🎯 Boas Práticas

### 1️⃣ Sempre Comece em Simulação

```
❌ ERRADO:
1. Criar conta Quotex
2. Ir direto para MODE=live
3. Perder tudo em 1 hora

✅ CERTO:
1. Configurar MODE=paper
2. Rodar 100+ operações
3. Validar que é lucrativo
4. SÓ DEPOIS mudar para MODE=live
```

### 2️⃣ Teste com Pequenos Valores

```
Quando FOR para MODE=live:

❌ ERRADO:
INITIAL_BALANCE_BRL=10000

✅ CERTO:
INITIAL_BALANCE_BRL=100
→ Testa a estratégia
→ Minimiza risco
→ Aumenta depois se der certo
```

### 3️⃣ Monitore Constantemente

```
Enquanto o robô roda:

✅ Cada 5-10 minutos:
• Verifique saldo
• Observe gráficos
• Procure por operações anormais

⚠️ Nunca deixe rodando sem supervisão
```

### 4️⃣ Use Stop Loss Mental

```
Defina limite de perda:

Exemplo:
• Saldo inicial: R$ 1.000
• Stop loss: -50% (R$ 500)
• Se chegar a R$ 500 → PARAR

Código prático:
1. Se saldo < R$ 500
2. Clique [⏹ Parar]
3. Revise a estratégia
4. Volte quando souber o problema
```

### 5️⃣ Diversifique Pares

```
Não use sempre o mesmo par:

❌ ERRADO:
SYMBOL=ADA/USDT  (sempre)

✅ CERTO:
• Segunda: ADA/USDT
• Terça: BTC/USDT
• Quarta: EUR/USD
• Quinta: ETH/USDT

Benefício:
• Menos risco concentrado
• Aprende comportamento de múltiplos ativos
```

---

## 📞 Próximos Passos

### Se Deu Certo em Paper ✅

```
1. Documente sua estratégia
2. Calcule o retorno esperado
3. Mude para MODE=live
4. Comece pequeno
5. Aumente gradualmente
```

### Se Não Deu Certo ❌

```
1. Analise o histórico de operações
2. Veja quais pares tiveram melhor resultado
3. Teste diferentes timeframes
4. Ajuste a estratégia
5. Volte ao passo 1
```

### Para Saber Mais

📖 **Leia também:**
- `PASSO_A_PASSO.md` - Guia detalhado passo a passo
- `GUIA_QUOTEX.md` - Documentação completa da API
- `INICIO_RAPIDO.md` - Quick start em 5 minutos
- `RESUMO_IMPLEMENTACAO.md` - Detalhes técnicos

---

## 💡 Dicas Finais

```
🎯 Recapitulando:

1. Iniciar:     python -m robo_trade.dashboard
2. Acessar:     http://127.0.0.1:5000
3. Configurar:  Par, Timeframe, Payout
4. Testar:      MODE=paper por 100+ operações
5. Validar:     Se lucrativo, considere MODE=live
6. Executar:    Clique [▶ Iniciar]
7. Monitorar:   Acompanhe o resultado

⚠️ Sempre priorize a segurança:
• Comece pequeno
• Teste antes de escalar
• Monitore constantemente
• Tenha um plano de parada

🎉 Parabéns! Você agora sabe como usar o ROBO TRADE!
```

---

**Última atualização:** Dezembro 2025
**Versão:** 1.0
**Suporte:** Consulte a documentação anexa ou revise os logs do terminal
