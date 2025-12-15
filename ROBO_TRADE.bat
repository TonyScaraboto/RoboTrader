@echo off
REM ============================================
REM ROBO TRADE - Inicializador
REM ============================================
REM Este arquivo inicia o ROBO TRADE automaticamente

setlocal enabledelayedexpansion

REM Cores para output
cls
echo.
echo ============================================
echo      ROBO TRADE - Inicializando...
echo ============================================
echo.

REM Verificar se estamos no diretório correto
if not exist "robo_trade\dashboard.py" (
    echo ERRO: Arquivo dashboard.py nao encontrado!
    echo.
    echo Este arquivo deve estar no mesmo diretorio que a pasta robo_trade/
    echo.
    echo Local esperado: %CD%\robo_trade\dashboard.py
    echo.
    pause
    exit /b 1
)

REM Verificar se Python está instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Instale Python 3.10+ em: https://www.python.org/
    echo.
    pause
    exit /b 1
)
echo OK - Python encontrado
echo.

REM Verificar se .env existe, senao criar
echo [2/4] Verificando configuracao...
if not exist ".env" (
    echo AVISO: Arquivo .env nao encontrado
    echo Criando arquivo .env com valores padrao...
    echo.
    (
        echo REM Configuracoes Quotex (email/senha)
        echo QUOTEX_EMAIL=seu_email_aqui
        echo QUOTEX_PASSWORD=sua_senha_aqui
        echo QUOTEX_LANG=pt
        echo QUOTEX_ENVIRONMENT=demo
        echo.
        echo REM Configuracoes de Trading
        echo SYMBOL=ADA/USDT
        echo TIMEFRAME=5m
        echo EXCHANGE=binance
        echo MODE=paper
        echo.
        echo REM Configuracoes de Saldo
        echo INITIAL_BALANCE_BRL=1000
        echo PAYOUT_RATIO=85.0
        echo EXPIRATION_TIME=60
    ) > .env
    echo.
    echo Arquivo .env criado! EDITE COM SUAS CREDENCIAIS QUOTEX
    echo.
    pause
    echo.
)
echo OK - Configuracao encontrada
echo.

REM Executar teste de conexao
echo [3/4] Testando conexao com API...
echo.
python test_quotex_connection.py 2>nul
if errorlevel 1 (
    echo AVISO: Teste de conexao falhou
    echo Continuando mesmo assim...
) else (
    echo OK - Teste passado
)
echo.

REM Iniciar Dashboard
echo [4/4] Iniciando Dashboard...
echo.
echo ============================================
echo      Sistema iniciado com sucesso!
echo ============================================
echo.
echo Acesse em seu navegador:
echo   http://127.0.0.1:5000
echo.
echo Aperte CTRL+C para parar
echo.
echo ============================================
echo.

REM Definir variaveis de ambiente
set HOST=127.0.0.1
set PORT=5000
set FLASK_ENV=production

REM Iniciar o servidor
python -m robo_trade.dashboard

REM Se chegou aqui, o servidor foi parado
echo.
echo Sistema parado.
echo.
pause
