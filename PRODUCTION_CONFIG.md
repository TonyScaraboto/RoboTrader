# ⚙️ Configuração para Produção

## Variáveis de Ambiente Necessárias

### Obrigatórias

```env
# Flask Secret Key (NUNCA use a padrão em produção!)
SECRET_KEY=sua-chave-super-secreta-aleatoria-64-caracteres-minimo

# Avalon Broker Credentials
AVALON_EMAIL=seu_email_real@exemplo.com
AVALON_PASSWORD=sua_senha_real_aqui

# Environment
DEBUG=false
HOST=0.0.0.0
PORT=5000
```

### Opcionais

```env
# Avalon Default Environment (demo ou real)
AVALON_ENVIRONMENT=demo

# Database (se usar PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Workers Gunicorn
WEB_CONCURRENCY=2
```

## 🔒 Gerar SECRET_KEY Segura

### Python:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### PowerShell:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### Online:
```bash
# Use um gerador online confiável:
# https://randomkeygen.com/
# Copie uma chave "CodeIgniter Encryption Key" (256-bit)
```

## 🚀 Configuração por Plataforma

### Railway

1. **Via Interface:**
   - Vá em projeto → Variables
   - Clique "New Variable"
   - Cole cada variável

2. **Via CLI:**
   ```bash
   railway variables set SECRET_KEY="sua-chave"
   railway variables set AVALON_EMAIL="seu-email"
   railway variables set AVALON_PASSWORD="sua-senha"
   railway variables set DEBUG="false"
   ```

### Render.com

1. **Via Interface:**
   - Dashboard → Environment
   - Add Environment Variable
   - Cole cada variável

2. **Via render.yaml:**
   ```yaml
   services:
     - type: web
       name: robo-trade
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT
       envVars:
         - key: SECRET_KEY
           sync: false
         - key: AVALON_EMAIL
           sync: false
         - key: AVALON_PASSWORD
           sync: false
         - key: DEBUG
           value: false
   ```

### VPS (DigitalOcean, AWS, etc.)

1. **Criar arquivo .env:**
   ```bash
   nano /home/robotrade/robo-trade/.env
   ```

2. **Adicionar variáveis:**
   ```env
   SECRET_KEY=sua-chave-aqui
   AVALON_EMAIL=seu-email
   AVALON_PASSWORD=sua-senha
   DEBUG=false
   ```

3. **Proteger arquivo:**
   ```bash
   chmod 600 .env
   chown robotrade:robotrade .env
   ```

### Docker

1. **Via docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - SECRET_KEY=${SECRET_KEY}
         - AVALON_EMAIL=${AVALON_EMAIL}
         - AVALON_PASSWORD=${AVALON_PASSWORD}
         - DEBUG=false
       env_file:
         - .env
       restart: unless-stopped
   ```

2. **Via docker run:**
   ```bash
   docker run -d \
     --name robotrade \
     -p 5000:5000 \
     -e SECRET_KEY="sua-chave" \
     -e AVALON_EMAIL="seu-email" \
     -e AVALON_PASSWORD="sua-senha" \
     -e DEBUG=false \
     --restart unless-stopped \
     robo-trade
   ```

## 🔐 Segurança

### ✅ Checklist de Segurança

- [ ] SECRET_KEY aleatória e forte (64+ caracteres)
- [ ] DEBUG=false em produção
- [ ] .env no .gitignore
- [ ] HTTPS ativo (Railway/Render fazem automático)
- [ ] Credenciais nunca no código
- [ ] Variáveis nunca commitadas no Git
- [ ] Arquivo .env com permissões 600 (VPS)
- [ ] Firewall configurado (VPS)
- [ ] Senhas fortes no Avalon Broker
- [ ] Backup de variáveis de ambiente

### ❌ NUNCA Faça Isso

```python
# ❌ ERRADO - Hardcoded
app.secret_key = "dev-secret-key"
avalon_email = "meu_email@example.com"
avalon_password = "minhasenha123"

# ✅ CORRETO - Variáveis de ambiente
app.secret_key = os.getenv('SECRET_KEY')
avalon_email = os.getenv('AVALON_EMAIL')
avalon_password = os.getenv('AVALON_PASSWORD')
```

### 🛡️ Proteção de Credenciais

1. **Nunca commitar .env:**
   ```bash
   # Verificar se .env está no .gitignore
   cat .gitignore | grep .env
   
   # Verificar se .env foi commitado acidentalmente
   git log --all --full-history -- .env
   
   # Se foi commitado, remover do histórico:
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Rotacionar credenciais:**
   - Mude SECRET_KEY a cada 3 meses
   - Use senhas diferentes para demo/real
   - Ative 2FA no Avalon se disponível

3. **Monitorar acessos:**
   - Veja logs de login
   - Monitore IPs de acesso
   - Configure alertas de falha de login

## 📊 Configurações de Performance

### Workers Gunicorn

```bash
# Fórmula: (2 x CPU cores) + 1
# Exemplo para 1 CPU:
workers = 2

# Para 2 CPUs:
workers = 5

# Railway/Render (1 CPU):
gunicorn run:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT

# VPS (2+ CPUs):
gunicorn run:app --workers 5 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT
```

### Timeout WebSocket

```python
# No robo_trade/avalon.py
# Já configurado para produção:
timeout = 30  # segundos para conexão
ping_interval = 25  # heartbeat
```

## 🔄 Atualizações

### Variáveis que podem mudar:

1. **SECRET_KEY** - Rotacionar trimestralmente
2. **AVALON_PASSWORD** - Se mudar senha
3. **DEBUG** - Sempre false em produção
4. **WEB_CONCURRENCY** - Ajustar conforme carga

### Como atualizar:

```bash
# Railway CLI
railway variables set SECRET_KEY="nova-chave"

# Render
# Via interface: Environment → Edit

# VPS
nano .env  # Editar valor
sudo supervisorctl restart robotrade
```

## 📝 Template .env para Produção

```env
# ===========================================
# ROBO TRADE - Configuração de Produção
# ===========================================
# ⚠️ NUNCA compartilhe este arquivo!
# ⚠️ NUNCA commite no Git!
# ===========================================

# Flask
SECRET_KEY=cole-aqui-sua-chave-64-caracteres-minimo-gerada-com-secrets
DEBUG=false
HOST=0.0.0.0
PORT=5000

# Avalon Broker
AVALON_EMAIL=seu_email_real@exemplo.com
AVALON_PASSWORD=sua_senha_super_segura_aqui
AVALON_ENVIRONMENT=demo

# Performance (opcional)
WEB_CONCURRENCY=2

# Database (se usar PostgreSQL - opcional)
# DATABASE_URL=postgresql://user:pass@host:5432/db

# ===========================================
# Gerado em: 2025-12-20
# Última atualização: 2025-12-20
# ===========================================
```

## ✅ Validação de Configuração

### Script de Teste:

```bash
# Criar test_config.py
cat > test_config.py << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Verificando configuração...\n")

checks = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "AVALON_EMAIL": os.getenv("AVALON_EMAIL"),
    "AVALON_PASSWORD": os.getenv("AVALON_PASSWORD"),
    "DEBUG": os.getenv("DEBUG"),
}

for key, value in checks.items():
    if value:
        masked = "***" + value[-4:] if len(value) > 4 else "***"
        print(f"✅ {key}: {masked}")
    else:
        print(f"❌ {key}: NÃO CONFIGURADO!")

# Verificar SECRET_KEY
secret = checks["SECRET_KEY"]
if secret:
    if len(secret) < 32:
        print(f"\n⚠️ SECRET_KEY muito curta! ({len(secret)} caracteres)")
        print("   Recomendado: 64+ caracteres")
    else:
        print(f"\n✅ SECRET_KEY tem {len(secret)} caracteres")

# Verificar DEBUG
if checks["DEBUG"] and checks["DEBUG"].lower() in ("true", "1", "yes"):
    print("\n⚠️ DEBUG está ATIVO! Desative em produção!")
else:
    print("\n✅ DEBUG está desativado")

print("\n🎯 Configuração validada!")
EOF

# Executar
python test_config.py
```

## 🆘 Recuperação de Desastres

### Backup de Variáveis:

```bash
# Exportar variáveis (Railway)
railway variables > railway_vars_backup.txt

# VPS
cp .env .env.backup.$(date +%Y%m%d)
```

### Restaurar:

```bash
# Railway
# Copiar valores do railway_vars_backup.txt
# Adicionar manualmente via interface

# VPS
cp .env.backup.20251220 .env
sudo supervisorctl restart robotrade
```

---

**⚙️ Configuração correta = App estável e seguro!**
