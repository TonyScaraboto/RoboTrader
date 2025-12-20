# 🚀 Guia de Deploy - Robo Trade

Este guia explica como colocar o Robo Trade online para funcionar 24/7.

## 📋 Opções de Deploy

### 1. Railway (Recomendado - Mais Fácil) ⭐

**Vantagens:**
- Deploy automático a partir do GitHub
- Free tier generoso (5$/mês de crédito grátis)
- PostgreSQL integrado
- Domínio HTTPS automático
- Fácil configuração

**Passos:**

1. **Criar conta no Railway**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Fazer upload do código para GitHub**
   ```bash
   cd "c:\Users\46\Desktop\ROBO TRADE"
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/SEU_USUARIO/robo-trade.git
   git push -u origin main
   ```

3. **Deploy no Railway**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha o repositório `robo-trade`
   - Railway detectará automaticamente o `railway.toml`

4. **Configurar Variáveis de Ambiente**
   - No painel do Railway, vá em "Variables"
   - Adicione:
     ```
     SECRET_KEY=SUA_CHAVE_SECRETA_AQUI
     AVALON_EMAIL=seu_email@exemplo.com
     AVALON_PASSWORD=sua_senha
     DEBUG=false
     ```

5. **Deploy Automático**
   - Railway fará o deploy automaticamente
   - Você receberá uma URL pública: `https://seu-app.railway.app`

### 2. Render.com (Alternativa Gratuita)

**Vantagens:**
- 750 horas grátis por mês
- Deploy fácil
- PostgreSQL grátis

**Passos:**

1. **Criar conta:** https://render.com
2. **New Web Service** → Conectar GitHub
3. **Configurações:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT`
   - Environment: Python 3
4. **Variáveis de Ambiente:** Adicionar as mesmas do Railway

### 3. VPS (DigitalOcean, Linode, AWS EC2)

**Para usuários avançados - Máximo controle**

#### Setup em Ubuntu 22.04:

```bash
# Conectar via SSH
ssh root@SEU_IP

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Python 3.12
apt install -y python3.12 python3.12-venv python3-pip nginx supervisor git

# Criar usuário
adduser robotrade
usermod -aG sudo robotrade
su - robotrade

# Clonar código
git clone https://github.com/SEU_USUARIO/robo-trade.git
cd robo-trade

# Criar ambiente virtual
python3.12 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn

# Configurar variáveis de ambiente
nano .env
# Adicionar:
# SECRET_KEY=sua_chave_secreta
# AVALON_EMAIL=seu_email
# AVALON_PASSWORD=sua_senha
# DEBUG=false

# Testar aplicação
gunicorn run:app --bind 0.0.0.0:5000
```

#### Configurar Supervisor (manter app rodando):

```bash
sudo nano /etc/supervisor/conf.d/robotrade.conf
```

Conteúdo:
```ini
[program:robotrade]
directory=/home/robotrade/robo-trade
command=/home/robotrade/robo-trade/venv/bin/gunicorn run:app --workers 2 --bind 0.0.0.0:5000
user=robotrade
autostart=true
autorestart=true
stderr_logfile=/var/log/robotrade/err.log
stdout_logfile=/var/log/robotrade/out.log
environment=PATH="/home/robotrade/robo-trade/venv/bin"
```

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/robotrade
sudo chown robotrade:robotrade /var/log/robotrade

# Iniciar
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start robotrade
```

#### Configurar Nginx (proxy reverso):

```bash
sudo nano /etc/nginx/sites-available/robotrade
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/robotrade /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Instalar SSL (HTTPS)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

### 4. Docker (Qualquer plataforma)

```bash
# Build da imagem
docker build -t robo-trade .

# Executar container
docker run -d \
  --name robotrade \
  -p 5000:5000 \
  -e SECRET_KEY=sua_chave_secreta \
  -e AVALON_EMAIL=seu_email \
  -e AVALON_PASSWORD=sua_senha \
  -e DEBUG=false \
  --restart unless-stopped \
  robo-trade

# Ver logs
docker logs -f robotrade

# Parar
docker stop robotrade

# Iniciar novamente
docker start robotrade
```

## 🔒 Segurança Importante

### 1. Variáveis de Ambiente (NUNCA compartilhe)

Crie arquivo `.env` (já listado no `.gitignore`):
```env
SECRET_KEY=chave-super-secreta-aleatoria-aqui
AVALON_EMAIL=seu_email_real@exemplo.com
AVALON_PASSWORD=sua_senha_real
DEBUG=false
HOST=0.0.0.0
PORT=5000
```

### 2. Gerar SECRET_KEY segura:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. HTTPS Obrigatório

Para produção, **sempre** use HTTPS:
- Railway/Render: Automático ✅
- VPS: Use Certbot (Let's Encrypt)

### 4. Firewall (VPS)

```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 📊 Monitoramento

### Logs no Railway/Render
- Interface web mostra logs em tempo real
- Procure por erros de conexão com Avalon

### Logs no VPS
```bash
# Logs do app
sudo tail -f /var/log/robotrade/out.log
sudo tail -f /var/log/robotrade/err.log

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Status do serviço
sudo supervisorctl status robotrade
```

## 🔄 Atualizações

### Railway/Render (Automático)
```bash
git add .
git commit -m "Atualização"
git push
# Deploy automático!
```

### VPS (Manual)
```bash
cd ~/robo-trade
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart robotrade
```

## 🌐 Acessar Online

Após deploy, acesse:
- **Railway:** `https://seu-app.railway.app`
- **Render:** `https://seu-app.onrender.com`
- **VPS:** `https://seu-dominio.com`

**Primeira vez:**
1. Acesse a URL
2. Faça login com credenciais do Avalon Broker
3. Sistema conectará automaticamente via WebSocket
4. Dashboard ficará online 24/7!

## ⚠️ Troubleshooting

### "Application Error" no Railway/Render
- Verifique logs no dashboard
- Confirme que todas variáveis de ambiente estão configuradas
- Verifique se `requirements.txt` está completo

### WebSocket não conecta
- Confirme que credenciais do Avalon estão corretas
- Verifique se o ambiente (demo/real) está configurado
- Veja logs para mensagens de erro específicas

### App fica lento
- Aumente número de workers do Gunicorn
- Considere upgrade do plano (Railway/Render)
- Monitore uso de CPU/RAM

## 💰 Custos Estimados

| Plataforma | Custo/mês | Recursos |
|------------|-----------|----------|
| Railway (Free) | $0 (limite 5$/mês) | 512MB RAM, sempre ativo |
| Render (Free) | $0 | 512MB RAM, dorme após inatividade |
| DigitalOcean | $6 | 1GB RAM, 25GB SSD, sempre ativo |
| AWS EC2 (t2.micro) | Grátis (1 ano) | 1GB RAM, sempre ativo |

## ✅ Checklist de Deploy

- [ ] Código no GitHub (privado recomendado)
- [ ] `.env` configurado com credenciais reais
- [ ] SECRET_KEY aleatória e segura
- [ ] Plataforma escolhida (Railway recomendado)
- [ ] Variáveis de ambiente configuradas na plataforma
- [ ] Deploy realizado com sucesso
- [ ] HTTPS ativo (automático Railway/Render)
- [ ] Teste de login funcionando
- [ ] WebSocket conectando ao Avalon
- [ ] Logs sendo monitorados
- [ ] Backups configurados (se VPS)

## 🎯 Recomendação Final

**Para começar rapidamente:** Use **Railway**
- Deploy em 5 minutos
- HTTPS automático
- $5 de crédito grátis/mês
- Escalável conforme crescer

**Para controle total:** Use **VPS** (DigitalOcean)
- Máximo controle
- Performance garantida
- Custo fixo baixo ($6/mês)
