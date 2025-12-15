@echo off
setlocal
python -m pip install -r requirements.txt || goto :end
python -m robo_trade.trader backtest || goto :end
python -m robo_trade.trader martingale_backtest || goto :end
python -m robo_trade.trader martingale_demo || goto :end
echo All runs completed.
:end
endlocal
