#!/usr/bin/env python3
"""
ROBO TRADE - Inicializador Executável
Compile com PyInstaller: pyinstaller --onefile --windowed launcher.py
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Mostra banner de inicialização"""
    print("\n" + "="*50)
    print("      ROBO TRADE - Inicializador")
    print("="*50 + "\n")

def check_python():
    """Verifica se Python está instalado"""
    print("[1/5] Verificando Python...", end=" ")
    try:
        version = sys.version.split()[0]
        print(f"OK - v{version}\n")
        return True
    except Exception as e:
        print(f"ERRO: {e}\n")
        return False

def check_project_structure():
    """Verifica se projeto está no lugar correto"""
    print("[2/5] Verificando estrutura do projeto...", end=" ")
    
    required_files = [
        "robo_trade/dashboard.py",
        "robo_trade/config.py",
        "robo_trade/quotex.py",
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"\nERRO: Arquivo {file} não encontrado!")
            print(f"Diretório atual: {os.getcwd()}")
            return False
    
    print("OK\n")
    return True

def check_and_create_env():
    """Verifica .env, cria se não existir"""
    print("[3/5] Verificando configuração (.env)...", end=" ")
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("\nCriando arquivo .env com valores padrão...")
        
        env_content = """# Configurações Quotex (email/senha)
    QUOTEX_EMAIL=seu_email_aqui
    QUOTEX_PASSWORD=sua_senha_aqui
    QUOTEX_LANG=pt
    QUOTEX_ENVIRONMENT=demo

# Configurações de Trading
SYMBOL=ADA/USDT
TIMEFRAME=5m
EXCHANGE=binance
MODE=paper

# Configurações de Saldo
INITIAL_BALANCE_BRL=1000
PAYOUT_RATIO=85.0
EXPIRATION_TIME=60

# Configurações do Servidor
HOST=127.0.0.1
PORT=5000
DEBUG=false
"""
        
        try:
            env_file.write_text(env_content)
            print("✓ Arquivo .env criado com sucesso!")
            print("⚠️  IMPORTANTE: Edite .env com suas credenciais Quotex\n")
            input("Pressione ENTER para continuar...")
            os.startfile(".env")  # Abre arquivo para editar
            return True
        except Exception as e:
            print(f"ERRO ao criar .env: {e}\n")
            return False
    else:
        print("OK\n")
        return True

def check_dependencies():
    """Verifica se dependências estão instaladas"""
    print("[4/5] Verificando dependências...", end=" ")
    
    try:
        import flask
        import dotenv
        import requests
        print("OK\n")
        return True
    except ImportError as e:
        print(f"\nAVISO: Dependência faltando: {e}")
        print("Instalando dependências...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", "requirements.txt"
            ])
            print("✓ Dependências instaladas!\n")
            return True
        except Exception as install_error:
            print(f"ERRO ao instalar: {install_error}\n")
            return False

def start_dashboard():
    """Inicia o Dashboard Flask"""
    print("[5/5] Iniciando Dashboard Flask...\n")
    
    print("="*50)
    print("    Dashboard iniciado com sucesso!")
    print("="*50)
    print("\n📊 Acesse em seu navegador:")
    print("   http://127.0.0.1:5000\n")
    print("⏹️  Pressione CTRL+C para parar\n")
    print("="*50 + "\n")
    
    # Abrir navegador automaticamente após 1s
    def open_browser():
        time.sleep(1)
        try:
            webbrowser.open("http://127.0.0.1:5000")
        except:
            pass
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar servidor
    try:
        os.environ["FLASK_ENV"] = "production"
        os.environ["HOST"] = "127.0.0.1"
        os.environ["PORT"] = "5000"
        
        from robo_trade.dashboard import app
        app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\nSistema parado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERRO ao iniciar dashboard: {e}")
        input("\nPressione ENTER para sair...")
        sys.exit(1)

def main():
    """Função principal"""
    print_banner()
    
    # Checklists
    if not check_python():
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    if not check_project_structure():
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    if not check_and_create_env():
        print("AVISO: Continuando sem criar .env\n")
    
    if not check_dependencies():
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    # Iniciar
    try:
        start_dashboard()
    except Exception as e:
        print(f"\nERRO CRÍTICO: {e}")
        input("Pressione ENTER para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()
