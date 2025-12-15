@echo off
setlocal
cd /d "%~dp0.."
python -m pip install -r requirements.txt || goto :end
python -m robo_trade.trader backtest || goto :end
python -m robo_trade.trader martingale_backtest || goto :end
python -m robo_trade.trader martingale_demo || goto :end
set PORT=8080
python -m robo_trade.dashboard || goto :end
echo Dashboard running at http://127.0.0.1:8080/
:end
endlocal
