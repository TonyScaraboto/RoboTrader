@echo off
echo ========================================
echo  Deploy Robo Trader para GitHub/Railway
echo ========================================
echo.

set /p GITHUB_URL="Cole a URL do repositorio GitHub (https://github.com/...): "

echo.
echo Conectando ao repositorio...
git remote add origin %GITHUB_URL%

echo.
echo Renomeando branch para main...
git branch -M main

echo.
echo Enviando codigo para GitHub...
git push -u origin main

echo.
echo ========================================
echo  Codigo enviado com sucesso!
echo ========================================
echo.
echo Proximos passos:
echo 1. Acesse: https://railway.app/new
echo 2. Clique em "Deploy from GitHub repo"
echo 3. Selecione "robo-trader"
echo 4. Configure variaveis de ambiente
echo 5. Gere dominio e acesse!
echo.
pause
