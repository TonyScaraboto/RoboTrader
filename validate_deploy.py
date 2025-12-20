#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validação pré-deploy
Verifica se tudo está configurado corretamente antes de fazer deploy
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_env_var(name, required=True, min_length=None):
    """Verifica variável de ambiente"""
    value = os.getenv(name)
    
    if not value:
        if required:
            print(f"❌ {name}: NÃO CONFIGURADO (OBRIGATÓRIO)")
            return False
        else:
            print(f"⚠️  {name}: Não configurado (opcional)")
            return True
    
    if min_length and len(value) < min_length:
        print(f"⚠️  {name}: Muito curto ({len(value)} caracteres, recomendado {min_length}+)")
        return False
    
    # Mascarar valor
    if len(value) > 6:
        masked = value[:2] + "*" * (len(value)-4) + value[-2:]
    else:
        masked = "***"
    
    print(f"✅ {name}: {masked} ({len(value)} caracteres)")
    return True

def check_file_exists(filepath, required=True):
    """Verifica se arquivo existe"""
    path = Path(filepath)
    
    if path.exists():
        size = path.stat().st_size
        print(f"✅ {filepath}: Existe ({size} bytes)")
        return True
    else:
        if required:
            print(f"❌ {filepath}: NÃO ENCONTRADO (OBRIGATÓRIO)")
        else:
            print(f"⚠️  {filepath}: Não encontrado (opcional)")
        return required == False

def check_gitignore():
    """Verifica se .env está no .gitignore"""
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        print("⚠️  .gitignore não encontrado")
        return False
    
    content = gitignore_path.read_text()
    if ".env" in content:
        print("✅ .env está no .gitignore")
        return True
    else:
        print("❌ .env NÃO está no .gitignore! Adicione agora!")
        return False

def check_imports():
    """Verifica se dependências principais estão instaladas"""
    print_header("VERIFICANDO DEPENDÊNCIAS PYTHON")
    
    dependencies = {
        'flask': 'Flask',
        'websockets': 'WebSockets',
        'aiohttp': 'aiohttp',
        'dotenv': 'python-dotenv',
        'pandas': 'pandas',
        'numpy': 'numpy',
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name}: Instalado")
        except ImportError:
            print(f"❌ {name}: NÃO INSTALADO")
            all_ok = False
    
    return all_ok

def check_robo_trade_structure():
    """Verifica estrutura do projeto"""
    print_header("VERIFICANDO ESTRUTURA DO PROJETO")
    
    required_files = [
        "robo_trade/__init__.py",
        "robo_trade/dashboard.py",
        "robo_trade/avalon.py",
        "robo_trade/config.py",
        "run.py",
        "requirements.txt",
    ]
    
    all_ok = True
    for file in required_files:
        if not check_file_exists(file):
            all_ok = False
    
    return all_ok

def validate_secret_key():
    """Valida SECRET_KEY"""
    secret = os.getenv("SECRET_KEY")
    
    if not secret:
        return False
    
    # Verificar se é a chave padrão (perigoso!)
    dangerous_keys = [
        "dev-secret-key-change-in-production",
        "secret",
        "secret-key",
        "changeme",
    ]
    
    if secret.lower() in dangerous_keys:
        print("❌ SECRET_KEY está usando valor PADRÃO! Mude antes do deploy!")
        return False
    
    if len(secret) < 32:
        print(f"⚠️  SECRET_KEY é curta ({len(secret)} chars). Recomendado: 64+")
        return False
    
    return True

def main():
    """Função principal de validação"""
    print_header("🔍 VALIDAÇÃO PRÉ-DEPLOY - ROBO TRADE")
    
    # Carregar .env se existir
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv()
        print("✅ Arquivo .env carregado\n")
    else:
        print("⚠️  Arquivo .env não encontrado - usando variáveis do sistema\n")
    
    all_checks_passed = True
    
    # 1. Verificar estrutura do projeto
    if not check_robo_trade_structure():
        all_checks_passed = False
    
    # 2. Verificar dependências
    if not check_imports():
        all_checks_passed = False
        print("\n💡 Execute: pip install -r requirements.txt")
    
    # 3. Verificar variáveis de ambiente
    print_header("VERIFICANDO VARIÁVEIS DE AMBIENTE")
    
    env_checks = [
        ("SECRET_KEY", True, 32),
        ("AVALON_EMAIL", True, None),
        ("AVALON_PASSWORD", True, 6),
        ("DEBUG", False, None),
        ("HOST", False, None),
        ("PORT", False, None),
    ]
    
    for check in env_checks:
        if not check_env_var(*check):
            all_checks_passed = False
    
    # 4. Validar SECRET_KEY especificamente
    print("\n📝 Validando SECRET_KEY...")
    if not validate_secret_key():
        all_checks_passed = False
    else:
        print("✅ SECRET_KEY parece segura")
    
    # 5. Verificar DEBUG em produção
    debug = os.getenv("DEBUG", "").lower()
    if debug in ("true", "1", "yes"):
        print("\n⚠️  DEBUG está ATIVO! Desative para produção:")
        print("   DEBUG=false")
        all_checks_passed = False
    else:
        print("\n✅ DEBUG está desativado (correto para produção)")
    
    # 6. Verificar .gitignore
    print_header("VERIFICANDO GIT")
    if not check_gitignore():
        all_checks_passed = False
    
    # 7. Verificar arquivos de deploy
    print_header("VERIFICANDO ARQUIVOS DE DEPLOY")
    
    deploy_files = [
        ("Procfile", False),
        ("railway.toml", False),
        ("Dockerfile", False),
        ("requirements.txt", True),
        ("runtime.txt", False),
    ]
    
    for file, required in deploy_files:
        check_file_exists(file, required)
    
    # 8. Teste rápido de importação do app
    print_header("TESTANDO IMPORTAÇÃO DO APP")
    
    try:
        from robo_trade.dashboard import app
        print("✅ App Flask importado com sucesso")
        print(f"✅ App name: {app.name}")
    except Exception as e:
        print(f"❌ Erro ao importar app: {e}")
        all_checks_passed = False
    
    # Resultado final
    print_header("RESULTADO DA VALIDAÇÃO")
    
    if all_checks_passed:
        print("✅ TODAS AS VERIFICAÇÕES PASSARAM!")
        print("\n🚀 Sistema pronto para deploy!")
        print("\n📋 Próximos passos:")
        print("   1. git add .")
        print("   2. git commit -m 'Preparar para deploy'")
        print("   3. git push origin main")
        print("   4. Fazer deploy na plataforma escolhida")
        print("\n📖 Veja DEPLOY.md ou QUICK_START.md para instruções")
        return 0
    else:
        print("❌ ALGUMAS VERIFICAÇÕES FALHARAM!")
        print("\n⚠️  Corrija os problemas antes de fazer deploy")
        print("\n💡 Dicas:")
        print("   - Configure todas variáveis obrigatórias no .env")
        print("   - Execute: pip install -r requirements.txt")
        print("   - Gere SECRET_KEY: python -c 'import secrets; print(secrets.token_hex(32))'")
        print("   - Configure DEBUG=false para produção")
        return 1

if __name__ == "__main__":
    sys.exit(main())
