@echo off
REM Phi3 Autonomous Agent - Web Dashboard Launcher
REM Windows batch file to run phi3_web_dashboard.py

echo.
echo ======================================================================
echo  PHI3 AUTONOMOUS AGENT - WEB DASHBOARD
echo ======================================================================
echo.
echo Starting web dashboard at http://localhost:5000
echo.
echo Opening browser in 2 seconds...
echo.

REM Run the web dashboard
python phi3_web_dashboard.py &

REM Wait 2 seconds for server to start
timeout /t 2 /nobreak

REM Open browser automatically
start http://localhost:5000

REM Keep window open
pause
