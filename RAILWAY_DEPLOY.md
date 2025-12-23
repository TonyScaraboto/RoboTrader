# 🚀 Instruções para Criar Repositório no GitHub e Deploy no Railway

## Passo 1: Criar Repositório no GitHub

### Via Interface Web (Recomendado):

1. **Acesse GitHub:**
   - Vá para: https://github.com/new
   - Ou clique no + no canto superior direito → "New repository"

2. **Configurar Repositório:**
   - Repository name: `robo-trader`
   - Description: `Sistema de trading automatizado com Avalon Broker`
   - Visibilidade: **Private** (recomendado) ou Public
   - ❌ NÃO marque "Add a README file"
   - ❌ NÃO adicione .gitignore (já temos)
   - ❌ NÃO escolha licença ainda
   - Clique em **"Create repository"**

3. **Copiar URL do Repositório:**
   Após criar, você verá uma tela com comandos.
   Copie a URL que aparece, será algo como:
   ```
   https://github.com/SEU_USUARIO/robo-trader.git
   ```

## Passo 2: Conectar Repositório Local ao GitHub

Abra o PowerShell no diretório do projeto e execute:

```powershell
# Navegar para o projeto
cd "c:\Users\46\Desktop\ROBO TRADE"

# Adicionar remote do GitHub (substitua SEU_USUARIO pelo seu usuário GitHub)
git remote add origin https://github.com/SEU_USUARIO/robo-trader.git

# Verificar
git remote -v

# Renomear branch para main (padrão GitHub)
git branch -M main

# Push inicial
git push -u origin main
```

**Se pedir autenticação:**
- Use seu usuário GitHub
- Senha: Use um **Personal Access Token** (não a senha da conta)
- Gerar token: https://github.com/settings/tokens
  - Clique em "Generate new token (classic)"
  - Marque: repo, workflow
  - Copie o token gerado
  - Use como senha no Git

## Passo 3: Deploy no Railway

### 3.1 Conectar Railway ao GitHub:

1. **Acesse Railway:**
   - https://railway.app/dashboard

2. **Novo Projeto:**
   - Clique em **"New Project"**
   - Selecione **"Deploy from GitHub repo"**
   - Se pedir permissão, autorize Railway a acessar seus repositórios

3. **Selecionar Repositório:**
   - Encontre e clique em **"robo-trader"**
   - Railway começará o deploy automaticamente

### 3.2 Configurar Variáveis de Ambiente:

1. **Acessar Configurações:**
   - No projeto Railway, clique em **"Variables"**

2. **Adicionar Variáveis:**
   Clique em **"New Variable"** e adicione uma por uma:

   ```
   Nome: SECRET_KEY
   Valor: [cole aqui a chave gerada abaixo]
   ```

   ```
   Nome: AVALON_EMAIL
   Valor: seu_email_real@avalon.com
   ```

   ```
   Nome: AVALON_PASSWORD
   Valor: sua_senha_real_aqui
   ```

   ```
   Nome: DEBUG
   Valor: false
   ```

3. **Gerar SECRET_KEY:**
   Execute no PowerShell:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copie o resultado e use como valor de SECRET_KEY

### 3.3 Gerar Domínio:

1. **Configurações do Projeto:**
   - Clique em **"Settings"**
   - Role até **"Domains"**

2. **Gerar Domínio:**
   - Clique em **"Generate Domain"**
   - Você receberá uma URL: `https://robo-trader-production-xxxx.up.railway.app`

### 3.4 Aguardar Deploy:

1. **Acompanhar Build:**
   - Clique em **"Deployments"**
   - Veja os logs em tempo real
   - Aguarde aparecer "✓ Build successful"

2. **Verificar Logs:**
   - Procure por mensagens como:
     ```
     * Running on http://0.0.0.0:5000
     ```

## Passo 4: Acessar Sistema Online

1. **Abrir URL:**
   - Copie a URL do domínio gerado
   - Cole no navegador
   - Exemplo: `https://robo-trader-production-xxxx.up.railway.app`

2. **Fazer Login:**
   - Sistema abrirá na tela de login
   - Entre com email/senha do Avalon Broker
   - Escolha ambiente (Demo/Real)
   - Clique em "Entrar"

3. **Usar Sistema:**
   - Dashboard carregará automaticamente
   - WebSocket conectará ao Avalon
   - Sistema está online 24/7! 🎉

## 🔄 Atualizações Futuras

Sempre que fizer mudanças no código:

```powershell
cd "c:\Users\46\Desktop\ROBO TRADE"
git add .
git commit -m "Descrição da atualização"
git push origin main
```

Railway fará deploy automático!

## ⚠️ Troubleshooting

### "Build Failed" no Railway
- Veja os logs clicando em "View Logs"
- Verifique se todas variáveis foram configuradas
- Confirme que requirements.txt está completo

### "Application Error" ao acessar
- Vá em Variables
- Confirme SECRET_KEY, AVALON_EMAIL, AVALON_PASSWORD
- Veja logs: procure por erros em vermelho

### Git push pede senha
- Use Personal Access Token, não senha da conta
- Gerar em: https://github.com/settings/tokens
- Marque: repo, workflow
- Copie o token e use como senha

### "Remote already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/robo-trader.git
```

## ✅ Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Código enviado (git push)
- [ ] Railway conectado ao repositório
- [ ] Variáveis de ambiente configuradas
- [ ] SECRET_KEY gerada e configurada
- [ ] Domínio gerado no Railway
- [ ] Deploy concluído com sucesso
- [ ] Sistema acessível online
- [ ] Login funcionando
- [ ] WebSocket conectando ao Avalon

## 📞 Comandos Úteis

```powershell
# Ver status Git
git status

# Ver remotes
git remote -v

# Ver última commit
git log -1

# Ver branches
git branch

# Forçar push (cuidado!)
git push -f origin main
```

## 🎯 Resumo Rápido

1. Criar repo no GitHub: https://github.com/new
2. Conectar local:
   ```powershell
   git remote add origin https://github.com/SEU_USUARIO/robo-trader.git
   git branch -M main
   git push -u origin main
   ```
3. Railway: New Project → Deploy from GitHub → robo-trader
4. Configurar variáveis (SECRET_KEY, AVALON_EMAIL, AVALON_PASSWORD)
5. Gerar domínio
6. Acessar e fazer login!

---

**🚀 Seu robô estará online em menos de 10 minutos!**
