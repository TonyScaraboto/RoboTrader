# 🎬 PASSO A PASSO: Da Conta Quotex ao Primeiro Trade

## ⏰ Tempo Total: ~10 minutos

---

## **PASSO 1: Criar Conta Quotex** (2 min)

### 1.1 Acessar Quotex
- Abra: https://quotex.io/
- Clique em **"Sign Up"** ou **"Registar-se"**

### 1.2 Criar Conta
```
Email: seu_email@exemplo.com
Senha: Digite uma senha forte
```

### 1.3 Verificar Email
- Confirme o email enviado por Quotex
- Complete o cadastro

✅ **Conta criada!**

---

## **PASSO 2: Confirmar Credenciais** (3 min)

### 2.1 Validar Login
- Faça login em https://quotex.io/ com seu **email e senha**
- Confirme que o acesso funciona normalmente

### 2.2 Preparar Dados
Tenha em mãos:
- **Email** da conta Quotex
- **Senha** da conta Quotex
- (Opcional) **Idioma**: `pt`, `en` ou `es` para `QUOTEX_LANG`

✅ **Você tem as credenciais corretas!**

---

## **PASSO 3: Configurar .env** (1 min)

### 3.1 Abrir Arquivo
Navegue para: `c:\Users\46\Desktop\ROBO TRADE\`

Abra `.env` com notepad ou editor de texto

### 3.2 Editar Credenciais
Encontre estas linhas:
```ini
QUOTEX_EMAIL=seu_email
QUOTEX_PASSWORD=sua_senha
QUOTEX_LANG=pt
QUOTEX_ENVIRONMENT=demo
```

**Substitua pelos SEUS valores:**
```ini
QUOTEX_EMAIL=meuemail@exemplo.com
QUOTEX_PASSWORD=minha_senha
QUOTEX_LANG=pt
QUOTEX_ENVIRONMENT=demo
```

### 3.3 Salvar Arquivo
- Ctrl+S (ou File > Save)
- Feche o editor

✅ **Configurado!**

---

## **PASSO 4: Testar Integração** (2 min)

### 4.1 Abrir Prompt de Comando
- Tecle **Windows + R**
- Digite: `cmd`
- Pressione **Enter**

### 4.2 Navegar para Pasta
```bash
cd c:\Users\46\Desktop\ROBO TRADE
```

### 4.3 Executar Teste
```bash
python test_quotex_connection.py
```

### 4.4 Resultado Esperado
```
✓ QUOTEX_EMAIL: ✓ Configurado
✓ QUOTEX_PASSWORD: ✓ Configurado
✓ Cliente QuotexClient instanciado com sucesso
✓ Broker criado com sucesso
✓ Todos os testes completados!
```

Se vir isso, está tudo certo! ✅

---

## **PASSO 5: Iniciar o Painel** (1 min)

### 5.1 Opção A: Duplo Clique (Mais Fácil)
1. Navegue até: `c:\Users\46\Desktop\ROBO TRADE\`
2. Encontre: `start_robo.bat`
3. **Duplo clique** para executar

### 5.2 Opção B: Linha de Comando (Se anterior falhar)
```bash
cd c:\Users\46\Desktop\ROBO TRADE
python -m robo_trade.dashboard
```

### 5.3 Resultado
Você verá:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

✅ **Servidor rodando!**

---

## **PASSO 6: Acessar o Painel** (1 min)

### 6.1 Abrir Navegador
- Abra seu navegador (Chrome, Firefox, Edge)

### 6.2 Acessar URL
```
http://127.0.0.1:5000
```

### 6.3 Ver Painel
Você verá o painel com:
- 📊 Gráficos
- ⚙️ Controles
- 📈 Estatísticas

✅ **Painel aberto!**

---

## **PASSO 7: Primeiro Trade em Paper** (1 min)

### 7.1 Selecionar Modo Simulação
No painel, no canto superior direito:
- Encontre o selector "Modo"
- Selecione: **"Simulação (Paper)"**

### 7.2 Configurar Parâmetros
Na seção "Controle do Robô":

**Par**: `ADA/USDT` (já preenchido)  
**Timeframe**: `5m` (ja preenchido)  
**Payout**: `85` (já preenchido)

### 7.3 Iniciar
Clique no botão: **▶ Iniciar**

### 7.4 Observar
- ✅ Status muda para "executando"
- ✅ Gráficos atualizam
- ✅ Operações aparecem na tabela
- ✅ Nenhum dinheiro real é usado

**Deixe rodar por 5-10 minutos para ver funcionando**

### 7.5 Parar
Clique no botão: **⏹ Parar**

✅ **Primeiro teste completo!**

---

## **PASSO 8: Trade em LIVE (Cuidado!)** ⚠️

### 8.1 ✅ PRÉ-REQUISITOS
- [ ] Testou em Paper com sucesso?
- [ ] Monitora a tela regularmente?
- [ ] Tem créditos na conta demo?
- [ ] Entende a estratégia Martingale?

Se respondeu **SIM** a todos, pode prosseguir.

### 8.2 Selecionar Modo Live
No painel:
- Selector "Modo": selecione **"Real (Live)"**

### 8.3 Advertência
Você verá aviso:
```
⚠️ Modo Live ativado
Você colocará ORDENS REAIS em sua conta demo!
```

### 8.4 Iniciar
Clique: **▶ Iniciar**

### 8.5 Monitorar
- 👀 **Mantenha a tela aberta**
- 📊 Acompanhe as operações
- 🛑 Clique PARAR se algo errado
- 💰 Veja saldo diminuindo/aumentando

### 8.6 Parar
Quando estiver satisfeito:
Clique: **⏹ Parar**

✅ **Primeiro live trade realizado!**

---

## **PASSO 9: Análise de Resultados** (1 min)

### 9.1 Ver Histórico
No painel, na seção "Resumo":
- **Operações**: Total de trades
- **Ganhos**: Número de wins
- **Perdas**: Número de losses
- **Lucro**: Ganho/perda total em BRL

### 9.2 Ver Gráficos
- **Equidade**: Linha mostrando sua carteira ao longo do tempo
- **Candlestick**: Preço do par negociado
- **Tabela**: Detalhe de cada operação

### 9.3 Ver Arquivo CSV
```
c:\Users\46\Desktop\ROBO TRADE\data\martingale_operations.csv
```

Contém detalhes de cada operação:
- Hora
- Par
- Direção (UP/DOWN)
- Valor da aposta
- Ganhou/Perdeu
- Lucro

✅ **Análise completa!**

---

## **Checklist Final**

- [x] Conta Quotex criada
- [x] .env configurado
- [x] Teste passou
- [x] Painel iniciado
- [x] Teste em Paper OK
- [x] Teste em Live OK
- [x] Histórico consultado

## 🎉 **Você conseguiu!**

Agora você tem um robô de trading automático funcionando na Quotex!

---

## 🆘 Problemas?

### "Painel não abre em http://127.0.0.1:5000"
```
❌ Servidor pode não estar rodando
✅ Abra cmd e execute:
   cd c:\Users\46\Desktop\ROBO TRADE
   python -m robo_trade.dashboard
```

### "Erro: Email is required"
```
❌ QUOTEX_EMAIL não está em .env
✅ Verifique:
   - Arquivo .env existe?
   - QUOTEX_EMAIL=seu_email está preenchido?
   - Sem espaços antes/depois?
```

### "Erro: Password is required"
```
❌ QUOTEX_PASSWORD não está em .env
✅ Verifique:
   - Arquivo .env existe?
   - QUOTEX_PASSWORD=sua_senha está preenchido?
   - Sem espaços antes/depois?
```

### "Ordens não estão sendo colocadas"
```
❌ Pode estar em modo Paper
✅ Verifique:
   - Está em modo "Real (Live)"?
   - Email/senha estão corretos?
   - Pares existem (ADA/USDT é válido)?
```

### "Saldo mostra 0 BRL"
```
⚠️ Normal se API não responder
✅ Verifique:
   - Sua conexão com internet?
   - Em Paper = saldo simulado
   - Em Live = verifique conta Quotex
```

---

## 📚 Mais Informações

- **Guia Completo**: `GUIA_QUOTEX.md`
- **Início Rápido**: `INICIO_RAPIDO.md`
- **Setup Detalhado**: `QUOTEX_SETUP.md`
- **Logs**: `data/robo_trade.log`

---

## 💡 Dicas Importantes

✅ **Sempre test em Paper ANTES de Live**  
✅ **Monitore seu robô nos primeiros trades**  
✅ **Mantenha saldo e não use alavancagem**  
✅ **Pare se perder dinheiro constantemente**  
✅ **Backups regulares de seus dados**  

---

**Parabéns por completar o setup!** 🚀

Seu robô está pronto para operar 24/7 na conta demo Quotex!
