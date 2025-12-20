# 🚀 Deploy Rápido - Railway (5 minutos)

## Passo 1: Preparar Código

```bash
# Navegar para o projeto
cd "c:\Users\46\Desktop\ROBO TRADE"

# Inicializar Git (se ainda não tiver)
git init
git add .
git commit -m "Preparar para deploy"
```

## Passo 2: Criar Conta Railway

1. Acesse: https://railway.app
2. Clique em **"Start a New Project"**
3. Faça login com GitHub

## Passo 3: Deploy

### Opção A: Deploy via GitHub (Recomendado)

```bash
# 1. Criar repositório no GitHub
# Vá em: https://github.com/new
# Nome: robo-trade
# Privado: ✓ (recomendado)

# 2. Conectar código ao GitHub
git remote add origin https://github.com/SEU_USUARIO/robo-trade.git
git branch -M main
git push -u origin main

# 3. No Railway:
# - Clique em "Deploy from GitHub repo"
# - Selecione "robo-trade"
# - Railway fará deploy automaticamente
```

### Opção B: Deploy via CLI Railway

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
railway init
railway up
```

## Passo 4: Configurar Variáveis

No painel Railway:
1. Clique no projeto
2. Vá em **"Variables"**
3. Adicione:

```
SECRET_KEY=cole-aqui-a-chave-gerada-abaixo
AVALON_EMAIL=seu_email@avalon.com
AVALON_PASSWORD=sua_senha_real
DEBUG=false
```

**Gerar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Passo 5: Acessar Online

1. No Railway, clique em **"Settings"**
2. Em **"Domains"**, clique em **"Generate Domain"**
3. Você receberá uma URL: `https://robo-trade-production-xxxx.railway.app`
4. Acesse a URL e faça login!

## ✅ Pronto!

Seu robô está online 24/7! 🎉

### URLs Úteis:
- **App:** https://seu-app.railway.app
- **Logs:** Painel Railway → Deployments → View Logs
- **Settings:** Painel Railway → Settings

### Próximos Passos:
1. ✅ Fazer login no sistema
2. ✅ Configurar robô em modo DEMO
3. ✅ Testar algumas operações
4. ✅ Monitorar logs
5. ✅ Quando confiante, mudar para REAL

## 🔄 Atualizações Futuras

Sempre que fizer mudanças no código:

```bash
git add .
git commit -m "Descrição da mudança"
git push
# Railway faz deploy automático!
```

## 💰 Custos

- **Free Tier:** $5 de crédito grátis/mês
- **Uso típico deste app:** ~$3-4/mês
- **Upgrade:** $5/mês para mais recursos

## 📊 Monitorar

### Ver Logs em Tempo Real:
```bash
railway logs
```

### Verificar Status:
- Painel Railway mostra: CPU, RAM, Deploy status
- Procure por ✅ ou ❌ nos logs

## ⚠️ Troubleshooting

### "Build Failed"
```bash
# Verificar railway.toml está correto
cat railway.toml

# Verificar requirements.txt
cat requirements.txt
```

### "Application Error"
- Vá em Variables
- Confirme que SECRET_KEY, AVALON_EMAIL, AVALON_PASSWORD estão configurados
- Veja logs: railway logs

### WebSocket não conecta
- Confirme credenciais corretas
- Veja logs para mensagens específicas do Avalon
- Teste em modo DEMO primeiro

## 🎯 Checklist Final

- [ ] Código no GitHub
- [ ] Projeto criado no Railway
- [ ] Deploy bem-sucedido (verde)
- [ ] Variáveis configuradas
- [ ] Domínio gerado
- [ ] Login funcionando
- [ ] WebSocket conectado
- [ ] Primeira operação em DEMO

---

**🎉 Parabéns! Seu robô está online e operando!**
