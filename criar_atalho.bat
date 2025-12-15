@echo off
REM Cria um atalho VBS para melhor apresentação
REM Este arquivo cria um atalho no Desktop com ícone

setlocal

set "SCRIPT_PATH=%~dp0"
set "BAT_FILE=%SCRIPT_PATH%ROBO_TRADE.bat"
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\ROBO TRADE.lnk"

echo Criando atalho no Desktop...
echo.

REM Usar VBScript para criar o atalho
powershell -NoProfile -Command ^
  "$shell = New-Object -ComObject WScript.Shell; " ^
  "$link = $shell.CreateShortcut('%SHORTCUT%'); " ^
  "$link.TargetPath = '%BAT_FILE%'; " ^
  "$link.WorkingDirectory = '%SCRIPT_PATH%'; " ^
  "$link.Description = 'Iniciar ROBO TRADE'; " ^
  "$link.IconLocation = 'C:\Windows\System32\cmd.exe,0'; " ^
  "$link.WindowStyle = 1; " ^
  "$link.Save(); " ^
  "Write-Host 'Atalho criado: %SHORTCUT%'"

echo.
echo Atalho criado com sucesso no Desktop!
echo.
pause
