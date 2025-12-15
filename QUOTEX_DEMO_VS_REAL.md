# 💰 Seletor de Ambiente Quotex (Demo vs Real)

## 🎯 O que é?

Você agora pode **escolher entre operar na conta Demo ou Real da Quotex** diretamente no painel do ROBO TRADE.

Isso permite:
- ✅ Testar estratégias com segurança na **Demo**
- ✅ Trocar para conta **Real** com um clique
- ✅ Aviso de segurança ao entrar em modo **Real**
- ✅ Gerenciar risco de forma consciente

---

## 📍 Onde Encontrar?

No topo do painel, você verá:

```
┌─────────────────────────────────────────┐
│ Quotex: [🏦 Demo ▼]                     │
│ Conta:  [📊 Todas as Contas ▼]          │
│ Tema:   [Auto ▼]                       │
│ Modo:   [Simulação (Paper) ▼]           │
│ Status: rodando (paper)                 │
└─────────────────────────────────────────┘
```

**Clique em "Quotex"** para mudar entre:
- 🏦 **Demo** - Conta de teste (sem risco)
- 💰 **Real** - Conta real (COM RISCO)

---

## 🔄 Como Mudar de Ambiente

### Passo 1: Clique no Seletor
```
Quotex: [🏦 Demo ▼]
         ↑
         Clique aqui
```

### Passo 2: Selecione a Opção
```
Quotex: [🏦 Demo ▼]
        ├─ 🏦 Demo (Sem Risco)
        └─ 💰 Real (COM RISCO) ← Clique aqui
```

### Passo 3: Confirme o Aviso
Se você estiver mudando para **Real**, verá este aviso:

```
⚠️ AVISO IMPORTANTE!

Você está prestes a trocar para a conta REAL da Quotex.

❌ Isso significa que você operará COM DINHEIRO REAL
❌ Operações perdidas resultarão em perda REAL de dinheiro
❌ Você é totalmente responsável pelas operações

✅ Tem certeza que deseja continuar?

(Recomendamos usar DEMO até validar sua estratégia)

[Cancelar] [OK]
```

### Passo 4: Confirmação
Se tudo correr bem, você verá:

```
✅ Ambiente alterado para REAL (Conta Quotex Real)

⚠️ LEMBRE-SE: Operações agora afetam sua conta real!
📊 Monitore constantemente!
```

---

## 🏦 Entendendo Cada Ambiente

### Demo (Seguro)

```
🏦 Demo - Sem Risco

✅ Vantagens:
• Nenhum dinheiro real é usado
• Você pode testar estratégias à vontade
• Ideal para aprender e validar
• Sem pressão emocional

❌ Limitações:
• Spreads podem ser diferentes do real
• Latência pode não ser exatamente igual
• Resultados podem diferir ligeiramente

💡 Use quando:
✓ Começar a usar o ROBO TRADE
✓ Testar nova estratégia
✓ Validar configurações
✓ Aprender como funciona
```

### Real (Produção)

```
💰 Real - COM RISCO REAL

✅ Vantagens:
• Resultados exatamente como acontecem no mercado
• Spreads reais da corretora
• Latência real da API
• Ganhos são SEUS (reais)

⚠️ Cuidados:
• Perdas são SUAS (reais)
• Requer atenção constante
• Risco de perder capital investido
• Responsabilidade do operador

💡 Use quando:
✓ Validou estratégia em Demo
✓ Taxa de acerto > 55%
✓ Entende o risco
✓ Pode perder dinheiro sem pânico
```

---

## 📊 Fluxo Recomendado

### Iniciante

```
1. DEMO (Mínimo 100 operações)
   ├─ Teste a estratégia padrão
   ├─ Ajuste parâmetros
   └─ Valide desempenho

2. DEMO (Mais 100 operações)
   ├─ Teste com diferentes pares
   ├─ Teste diferentes timeframes
   └─ Ganhe experiência

3. REAL (Com capital mínimo)
   ├─ Comece com R$ 50-100
   ├─ Valide que API funciona
   └─ Prepare para escalar

4. REAL (Escalamento gradual)
   ├─ Aumente para R$ 500
   ├─ Depois R$ 1.000
   └─ Continuar conforme lucrar
```

### Experiente

```
1. DEMO (Rápida validação)
   ├─ 20-30 operações
   └─ Validar parâmetros

2. REAL (Capital pequeno)
   ├─ Comece com R$ 100-200
   ├─ Valide estratégia em condições reais
   └─ Escale conforme lucro
```

---

## ⚠️ Avisos Importantes

### Antes de Mudar para REAL

```
✅ CHECKLIST DE SEGURANÇA:

□ Testest em DEMO com sucesso (>55% acerto)
□ Validou em 100+ operações
□ Entende o risco de perda
□ Tem capital que pode perder
□ API está funcionando corretamente
□ Credenciais estão corretas
□ Saldo Quotex está visível
□ Modo (Paper/Live) está correto
```

### Operando em REAL

```
⚠️ CUIDADOS:

1. Monitore CONSTANTEMENTE
   • Cada operação afeta seu dinheiro
   • Não deixe rodando sozinho

2. Entenda o Risco
   • Taxa de 55% ainda significa 45% perdendo
   • Martingale aumenta o risco
   • Banca pode acabar rapidamente

3. Tenha um Stop Loss
   • Exemplo: Se perder 50%, PARAR
   • Nunca deixar perder tudo
   • Preservar o que ganha

4. Use Capital Pequeno
   • Comece com R$ 100-200
   • Não invista economia
   • Invista apenas o que pode perder
```

---

## 🔐 Segurança

### As Credenciais Estão Seguras?

```
✅ SIM - Seu Token API está seguro:

1. Armazenado apenas em .env (não no código)
2. Nunca enviado para servidor remoto
3. Apenas usado para requisições à Quotex
4. Você tem controle total
```

### Como Revogar Acesso?

Se suspeitar que o token foi comprometido:

```
1. Acesse: https://quotex.io/
2. Vá para: Configurações > Segurança > API
3. Clique: "Revogar Token"
4. Gere um novo token
5. Atualize em .env com o novo token
6. Restart do servidor
```

---

## 🔄 Configuração Técnica

### Como Funciona no Backend?

```
1. Você clica em "💰 Real"
2. JavaScript envia POST para /set-quotex-environment
3. Flask atualiza settings.quotex_environment = 'live'
4. Próximas operações usam a conta Real
5. Se há broker ativo, recria com novo ambiente
```

### Arquivo Que Controla Isso

```
robo_trade/config.py:
├─ quotex_environment = 'demo'  # ou 'live'
└─ Carregado de: QUOTEX_ENVIRONMENT em .env
```

---

## 📱 Exemplos Práticos

### Exemplo 1: Iniciante Começando

```
DIA 1: Segunda
├─ 1. Painel abre em DEMO (padrão)
├─ 2. Configura: ADA/USDT, 5m, 85% payout
├─ 3. Clica [▶ Iniciar]
├─ 4. Observa 20 operações na tabela
└─ 5. Se ganhar 15/20, segue para próximo

DIA 2: Terça
├─ 1. Continua em DEMO
├─ 2. Já tem 100+ operações
├─ 3. Taxa de acerto está em 65%
├─ 4. Acha confortável com estratégia
└─ 5. Pronto para validar em REAL

DIA 3: Quarta
├─ 1. Clica em Quotex: [🏦 Demo ▼]
├─ 2. Seleciona: [💰 Real]
├─ 3. Lê aviso e clica OK
├─ 4. Agora Quotex: [💰 Real]
├─ 5. Começa com R$ 50 (pequeno)
├─ 6. Executa 20 operações
├─ 7. Resultado: +R$ 15 (30% retorno!)
└─ 8. Pronto para escalar
```

### Exemplo 2: Teste Rápido

```
SITUAÇÃO: Quer testar um parâmetro novo

DEMO:
├─ Par: BTC/USDT (novo)
├─ 5 operações teste
├─ Resultado: 60% acerto
└─ Testa mais 25 operações: 58% mantém

REAL (escala pequena):
├─ R$ 50 iniciais
├─ Mesma estratégia
├─ 5 operações
└─ Se ganhar, validou! Se não, volta DEMO

CONCLUSÃO: Estratégia validada em REAL
```

### Exemplo 3: Operando 2 Ambientes

```
SITUAÇÃO: Quer testar algo novo ENQUANTO 
          continua lucrando em DEMO

SOLUÇÃO: Use as 3 contas disponíveis!

├─ Conta 1 (DEMO): Estratégia estabelecida
├─ Conta 2 (DEMO): Teste nova estratégia
└─ Conta 3 (REAL):Produção com capital real

Quotex: [🏦 Demo ▼] (controla 1+2)
Modo:   [Simulação ▼] (controla 1+2)
Modo:   [Real ▼]     (controla 3)

Com seletor de Contas pode alternar
entre vendo DEMO (Contas 1+2) e 
REAL (Conta 3)
```

---

## 🎯 Resumo

| Aspecto | Demo | Real |
|--------|------|------|
| **Risco** | ✅ Nenhum | ⚠️ Total |
| **Dinheiro Real** | ❌ Não | ✅ Sim |
| **Spreads** | Simulado | Real |
| **Quando Usar** | Testes | Produção |
| **Ganhos** | Fictícios | Reais (seus!) |
| **Perdas** | Nenhuma | Reais (suas!) |

---

## 📞 Dúvidas Frequentes

**P: Perdi em REAL. Posso voltar para DEMO?**
R: Sim! Clique em Quotex > Demo. Mas o dinheiro perdido não volta. Por isso teste em DEMO primeiro.

**P: Quanto devo começar em REAL?**
R: Comece com R$ 50-100. Não invista mais que consegue perder.

**P: A estratégia que ganhou em DEMO vai ganhar em REAL?**
R: Geralmente sim, mas spreads e latência podem afetar. Não garante igualdade.

**P: Posso deixar rodando em REAL enquanto durmo?**
R: ❌ Não recomendado. Acompanhe as operações.

**P: Qual a melhor taxa para começar em REAL?**
R: Acima de 60%. Abaixo de 55% é arriscado.

---

**Última atualização:** Dezembro 2025
**Versão:** 1.0 - Seletor Demo/Real
