@echo off
setlocal
python -m pip install -r requirements.txt || goto :end
python -m robo_trade.dashboard || goto :end
echo Dashboard running at http://127.0.0.1:5000/
:end
endlocal
