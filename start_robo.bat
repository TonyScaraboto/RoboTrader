@echo off
REM Robo Trade - Script de Inicialização Rápido
REM Uso: Duplo clique para iniciar o painel

title Robo Trade - Painel de Controle
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    ROBO TRADE - PAINEL                     ║
echo ║              Trading Automático com Quotex                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar se está na pasta correta
if not exist "robo_trade\dashboard.py" (
    echo ✗ Erro: arquivo dashboard.py não encontrado!
    echo   Certifique-se de executar este script na pasta raiz do projeto.
    echo.
    pause
    exit /b 1
)

REM Verificar .env
if not exist ".env" (
    echo ✗ Aviso: arquivo .env não encontrado!
    echo   Você precisa configurar suas credenciais da conta Quotex.
    echo.
    echo   Criando arquivo .env padrão...
    copy NUL .env >nul
    
    echo. >> .env
    echo # Quotex Demo Account >> .env
    echo QUOTEX_EMAIL=seu_email_quotex >> .env
    echo QUOTEX_PASSWORD=sua_senha_quotex >> .env
    echo QUOTEX_LANG=pt >> .env
    echo QUOTEX_ENVIRONMENT=demo >> .env
    echo. >> .env
    echo # Trading Configuration >> .env
    echo SYMBOL=ADA/USDT >> .env
    echo EXPIRATION_TIME=60 >> .env
    echo PAYOUT_RATIO=85 >> .env
    echo INITIAL_BALANCE_BRL=1000 >> .env
    
    echo.
    echo ✓ Arquivo .env criado!
    echo.
    echo   Próximos passos:
    echo   1. Abra .env em um editor de texto
    echo   2. Substitua 'seu_email_quotex' pelo seu email
    echo   3. Substitua 'sua_senha_quotex' pela sua senha
    echo   4. Ajuste o idioma se quiser (pt/en/es)
    echo   5. Salve o arquivo e execute novamente
    echo.
    pause
    exit /b 1
)

REM Testar configuração
echo Testando configuração...
python test_quotex_connection.py 2>nul | find "Configuração OK" >nul
if errorlevel 1 (
    echo.
    echo ⚠️  Aviso: Sua configuração pode estar incompleta
    echo   Verifique o arquivo .env e a conexão com a internet
    echo.
)

echo.
echo ✓ Iniciando Robo Trade...
echo   Acesse: http://127.0.0.1:5000
echo.
echo ⚠️  NÃO FECHE ESTA JANELA enquanto estiver usando o painel!
echo.

REM Definir portas e iniciar Flask
set HOST=127.0.0.1
set PORT=5000
set FLASK_APP=robo_trade.dashboard

python -m robo_trade.dashboard

if errorlevel 1 (
    echo.
    echo ✗ Erro ao iniciar o Robo Trade!
    echo   Verifique a configuração do .env
    echo.
    pause
    exit /b 1
)
