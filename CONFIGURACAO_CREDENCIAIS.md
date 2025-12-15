# 🔑 Configuração de Credenciais Quotex

Este guia mostra como configurar suas credenciais Quotex para usar o bot.

## 📝 Método 1: Arquivo .env (Recomendado)

### Passo 1: Copiar arquivo de exemplo
```bash
copy .env.example .env
```

### Passo 2: Editar .env
Abra o arquivo `.env` e preencha:

```ini
# Use o email e senha da sua conta Quotex
QUOTEX_EMAIL=seu@email.com
QUOTEX_PASSWORD=sua_senha_quotex
QUOTEX_LANG=pt
```

### Passo 3: Salvar e testar
```bash
python test_quotex_connection.py
```

---

## 🌐 Método 2: Interface Web (Mais Fácil)

### Passo 1: Iniciar o servidor
```bash
python -m robo_trade.dashboard
```

### Passo 2: Acessar Configurações
1. Abra http://127.0.0.1:5000
2. Clique em **⚙️ Configurações** no menu lateral
3. Preencha:
   - **Email**: seu@email.com
   - **Senha**: sua_senha_quotex
   - **Idioma**: Português (pt)
4. Clique em **💾 Salvar Configurações**
5. Teste a conexão com **🔌 Testar Conexão**

---

## 🔐 Segurança

### ⚠️ IMPORTANTE:
- **NUNCA** compartilhe seu arquivo `.env`
- O arquivo `.env` está no `.gitignore` (não vai para o Git)
- Suas credenciais ficam apenas no seu computador
- Use conta **DEMO** para testar antes de usar conta real

### 🛡️ Boas Práticas:
1. Comece sempre em modo **DEMO**
2. Teste todas as funcionalidades antes de usar dinheiro real
3. Use senhas fortes e únicas
4. Não compartilhe sua senha com ninguém

---

## 🌍 Idiomas Suportados

Configure `QUOTEX_LANG` com:
- `pt` - Português (Brasil)
- `en` - English
- `es` - Español

---

## ✅ Verificando Configuração

Execute o teste de conexão:
```bash
python test_quotex_connection.py
```

Você deve ver:
```
==================================================
TESTE 1: Verificando Configuração
==================================================
✓ QUOTEX_EMAIL: ✓ Configurado
✓ QUOTEX_PASSWORD: ✓ Configurado
✓ QUOTEX_LANG: pt
✓ QUOTEX_ENVIRONMENT: demo

✓ Configuração OK
```

---

## 🆘 Problemas Comuns

### ❌ "Credenciais ausentes"
**Solução**: Verifique se preencheu `QUOTEX_EMAIL` e `QUOTEX_PASSWORD` no `.env`

### ❌ "Login failed"
**Solução**: 
- Verifique se email e senha estão corretos
- Tente fazer login manualmente no site da Quotex
- Verifique se sua conta não está bloqueada

### ❌ "Connection failed"
**Solução**:
- Verifique sua conexão com internet
- Verifique se o site da Quotex está funcionando
- Tente novamente em alguns minutos

---

## 📞 Suporte

Se tiver problemas:
1. Verifique este guia novamente
2. Execute `python test_quotex_connection.py` para diagnóstico
3. Verifique os logs no terminal
4. Consulte a documentação da PyQuotex: https://github.com/cleitonleonel/pyquotex

---

## 🚀 Próximos Passos

Após configurar as credenciais:
1. ✅ Testar conexão (`python test_quotex_connection.py`)
2. ✅ Iniciar dashboard (`python -m robo_trade.dashboard`)
3. ✅ Acessar http://127.0.0.1:5000
4. ✅ Configurar estratégia de trading
5. ✅ Iniciar bot em modo DEMO
6. ✅ Monitorar resultados
7. ✅ Ajustar parâmetros conforme necessário
