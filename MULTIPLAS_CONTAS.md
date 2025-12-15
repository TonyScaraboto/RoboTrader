# 📊 Sistema de Múltiplas Contas - ROBO TRADE

## 🎯 O que é?

O painel agora suporta **gerenciamento de múltiplas contas de trading** simultâneas. Você pode:

- ✅ Operar em **3 contas diferentes** ao mesmo tempo
- ✅ Visualizar dados **individualmente** por conta
- ✅ Ver um **resumo consolidado** de todas as contas
- ✅ Alternar entre contas com um **seletor simples**
- ✅ Comparar performance de cada conta em tempo real

---

## 🔄 Como Funciona

### Contas Disponíveis

```
┌─────────────────────────────────────┐
│ SELETOR DE CONTA (Dropdown)         │
├─────────────────────────────────────┤
│ 📊 Todas as Contas (Consolidado)    │
│ 👤 Conta 1 (Paper/Simulação)        │
│ 👤 Conta 2 (Paper/Simulação)        │
│ 👤 Conta 3 (Live/Ao Vivo)           │
└─────────────────────────────────────┘
```

**Configuração padrão:**
- **Conta 1**: Simulação - R$ 1.000 iniciais
- **Conta 2**: Simulação - R$ 1.000 iniciais
- **Conta 3**: Ao Vivo - R$ 1.000 iniciais

---

## 📈 Visualizações por Conta

### 1️⃣ Seleção "Todas as Contas"

Mostra um **resumo consolidado** de todos os dados:

```
┌─────────────────────────────────────────────────┐
│ 📊 RESUMO DE TODAS AS CONTAS                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Conta 1  │    │ Conta 2  │    │ Conta 3  │  │
│  │ R$ 1.100 │    │ R$ 950   │    │ R$ 1.250 │  │
│  │ 50%✅    │    │ -5%❌    │    │ 25%✅    │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│                                                 │
│  Total Investido: R$ 3.000                      │
│  Lucro Total:     R$ 300                        │
│  Retorno Total:   10%                           │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Dados exibidos:**
- Saldo atual de cada conta
- Taxa de retorno (%)
- Taxa de acerto (%)
- Total investido em todas as contas
- Lucro consolidado
- Retorno total do portfólio

### 2️⃣ Seleção de Conta Individual

Mostra **dados específicos** daquela conta:

```
┌────────────────────────────────────┐
│ 📊 EQUITY - CONTA 1 (PAPER)        │
├────────────────────────────────────┤
│ Conta: Conta 1 (Paper)             │
│ Modo: PAPER                        │
│ Saldo: R$ 1.100,00                 │
├────────────────────────────────────┤
│ [Gráfico de evolução de patrimônio]│
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ 💹 CANDLESTICK - CONTA 1 (PAPER)   │
├────────────────────────────────────┤
│ [Gráfico de preço em candlestick]  │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ OPERAÇÕES - CONTA 1                │
├────────────────────────────────────┤
│ Total: 150 operações               │
│ Ganhos: 100 (66,7%)                │
│ Perdas: 50 (33,3%)                 │
│ Lucro: +R$ 150                     │
└────────────────────────────────────┘
```

**Dados exibidos:**
- Nome e modo da conta (Paper/Live)
- Saldo atual
- Gráfico de Equity (evolução do patrimônio)
- Gráfico de Candlestick (preço do ativo)
- Histórico de operações dessa conta

---

## 🎮 Como Usar

### Alternar Entre Contas

```
1. Localize o dropdown "Conta:" no topo do painel
2. Clique para expandir as opções
3. Selecione:
   • "📊 Todas as Contas" → Ver resumo consolidado
   • "👤 Conta 1" → Ver dados individuais
   • "👤 Conta 2" → Ver dados individuais
   • "👤 Conta 3" → Ver dados individuais
```

**Resultado:**
- Gráficos se atualizam para a conta selecionada
- Títulos mudam para indicar qual conta está sendo visualizada
- Dados da conta (saldo, operações) são atualizados
- Histórico da tabela é filtrado para aquela conta

### Interpretar o Resumo Consolidado

**Exemplo:**

```
Conta 1 (Paper):        R$ 1.150,00  ✅ 50 ops | 70% acerto
Conta 2 (Paper):        R$ 900,00    ❌ 40 ops | 45% acerto
Conta 3 (Live):         R$ 1.250,00  ✅ 60 ops | 75% acerto

─────────────────────────────────────────────────

Total Investido:        R$ 3.000,00
Lucro Total:            R$ 300,00
Retorno Total:          10,00%
```

**O que significa:**
- **Conta 1**: Ganhando, boa taxa de acerto
- **Conta 2**: Perdendo dinheiro, baixa taxa de acerto
- **Conta 3**: Melhor performance, maior lucro
- **Portfólio**: +10% no total (diversificação reduz risco)

---

## 📊 Gráficos por Conta

### Equity (Patrimônio)

**Quando selecionada "Todas as Contas":**
- Mostra a soma do equity de todas as contas
- Linhas que sobem = lucro consolidado
- Linhas que descem = prejuízo consolidado

**Quando selecionada uma conta específica:**
- Mostra apenas o equity daquela conta
- Mais granular e detalhado
- Melhor para análise profunda

### Candlestick (Preço)

Mostra o histórico de preço do par selecionado:
- Velas verdes = preço subiu (CALL acertava)
- Velas vermelhas = preço caiu (PUT acertava)
- Útil para validar decisões do robô

---

## 🔧 Configurar Contas

### Adicionar/Modificar Contas

Para adicionar mais contas, edite o arquivo `dashboard.py`:

```javascript
// Linha ~415 (dentro do código JavaScript)

const accountsData = {
  all: { name: 'Todas as Contas', mode: 'mixed', initial: 3000, data: [] },
  account1: { name: 'Conta 1 (Paper)', mode: 'paper', initial: 1000, ... },
  account2: { name: 'Conta 2 (Paper)', mode: 'paper', initial: 1000, ... },
  account3: { name: 'Conta 3 (Live)', mode: 'live', initial: 1000, ... },
  // ADICIONE AQUI:
  account4: { name: 'Conta 4 (Paper)', mode: 'paper', initial: 500, ... },
};
```

E no HTML (procure por `id="accountSelect"`):

```html
<select id="accountSelect">
  <option value="all">📊 Todas as Contas</option>
  <option value="account1">👤 Conta 1 (Paper)</option>
  <option value="account2">👤 Conta 2 (Paper)</option>
  <option value="account3">👤 Conta 3 (Live)</option>
  <!-- ADICIONE AQUI: -->
  <option value="account4">👤 Conta 4 (Paper)</option>
</select>
```

---

## 💡 Casos de Uso

### Use Case 1: Testar Múltiplas Estratégias

```
Conta 1: Estratégia de Martingale Clássica
Conta 2: Estratégia de Fibonacci
Conta 3: Estratégia Manual (ao vivo)

→ Veja qual gera mais lucro
→ Identifique a melhor estratégia
→ Escale a vencedora
```

### Use Case 2: Diversificar Ativos

```
Conta 1: ADA/USDT + 5m
Conta 2: BTC/USDT + 15m
Conta 3: EUR/USD + 5m

→ Reduz risco de concentração
→ Aproveita diferentes padrões
→ Maior estabilidade
```

### Use Case 3: Separar Paper vs Live

```
Conta 1: Paper - Teste seguro
Conta 2: Paper - Validação
Conta 3: Live - Produção com capital real

→ Teste antes de colocar dinheiro real
→ Valide estratégia
→ Execute com confiança
```

### Use Case 4: Múltiplos Usuários

```
Conta 1: Operador A
Conta 2: Operador B
Conta 3: Bot Automático

→ Painel compartilhado
→ Cada um vê seus dados
→ Comparar desempenho
```

---

## 📊 Exemplo Prático

### Cenário: 3 Contas Operando Diferentes Estratégias

**Situação Inicial:**
```
Conta 1 (Paper):   R$ 1.000  | 0 ops | 0%
Conta 2 (Paper):   R$ 1.000  | 0 ops | 0%
Conta 3 (Live):    R$ 1.000  | 0 ops | 0%
Total:             R$ 3.000  | 0 ops | 0%
```

**Após 100 operações cada:**
```
Conta 1 (Martingale):    R$ 1.150  | 100 ops | 70% | +R$ 150 ✅
Conta 2 (Fibonacci):     R$ 900    | 100 ops | 45% | -R$ 100 ❌
Conta 3 (Live Manual):   R$ 1.250  | 100 ops | 75% | +R$ 250 ✅
─────────────────────────────────────────────────────────────
Total:                   R$ 3.300  | 300 ops | 63% | +R$ 300 ✅

Retorno: +10% no portfólio
Melhor Conta: Conta 3 (Live) com +25%
Pior Conta: Conta 2 (Fibonacci) com -10%

Conclusão: Escalar Conta 3, ajustar Conta 2
```

---

## ⚠️ Boas Práticas

### ✅ Faça Isso

```
1. Use Conta 1 para teste inicial
2. Valide em Conta 2 com diferentes parâmetros
3. Só mova para Conta 3 (Live) após sucesso
4. Monitore as 3 contas diariamente
5. Ajuste estratégias baseado em resultados
6. Mantenha diversificação de risco
```

### ❌ Evite Isso

```
1. ❌ Colocar tudo em uma única conta
2. ❌ Ir direto para Live sem validar em Paper
3. ❌ Ignorar conta perdedora (analise o porquê)
4. ❌ Deixar rodando sem supervisão
5. ❌ Mudar estratégia a cada dia
6. ❌ Assumir riscos desnecessários
```

---

## 📱 Interface Mobile

Em dispositivos móveis, o seletor de contas fica no topo:

```
┌─────────────────────────────┐
│ Conta: [📊 Todas ▼]  | ⚙️   │
│ Tema: [Auto ▼]             │
│ Modo: [Paper ▼]            │
│ Status: rodando (paper)     │
└─────────────────────────────┘

[Conteúdo abaixo...]
```

---

## 🔄 Atualização em Tempo Real

Os dados são atualizados **a cada 2 segundos**:

```
├─ 2s:  Busca dados da API
├─ 2s:  Atualiza gráficos
├─ 2s:  Atualiza saldos
├─ 2s:  Recalcula estatísticas
├─ 2s:  Renderiza UI
└─ Repete...
```

**Obs:** Se você deixar o painel aberto em múltiplas abas, cada uma faz suas próprias requisições. Isso é normal e esperado.

---

## 🐛 Troubleshooting

### Problema: Gráficos não aparecem

```
❌ Gráfico em branco

✅ Solução:
1. Aguarde 4 segundos (2 ciclos de atualização)
2. Clique em outra conta e volte
3. Recarregue a página (F5)
4. Verifique se há dados em "Operações"
```

### Problema: Dados desatualizados

```
❌ Saldo não muda

✅ Solução:
1. Verifique se o robô está rodando
2. Clique [▶ Iniciar] se necessário
3. Espere 2 segundos pelo próximo ciclo
4. Procure por erros no console (F12)
```

### Problema: Contas mostram valores iguais

```
❌ Conta 1, 2, 3 com mesmo saldo

✅ Solução:
1. Cada conta precisa de seu próprio histórico
2. Os dados são lidos do arquivo CSV
3. Verifique se há arquivo martingale_operations.csv
4. Certifique-se que cada conta tem dados diferentes
```

---

## 📚 Próximos Passos

1. **Teste em Paper**: Use Conta 1 e 2 para testar
2. **Valide Performance**: Compare resultados
3. **Escale para Live**: Use Conta 3 com capital real
4. **Monitore Diariamente**: Acompanhe as 3 contas
5. **Ajuste Estratégia**: Baseado em resultados

---

**Última atualização:** Dezembro 2025
**Versão:** 1.1 - Suporte a Múltiplas Contas
