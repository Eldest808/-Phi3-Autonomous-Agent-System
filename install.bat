@echo off
REM Install Python Dependencies for Phi3 Autonomous Agent

echo.
echo ======================================================================
echo  INSTALLING DEPENDENCIES
echo ======================================================================
echo.

echo Installing required Python packages...
echo.

pip install requests flask flask-cors pyautogui mss pillow python-dotenv colorama

echo.
echo ======================================================================
echo INSTALLATION COMPLETE
echo ======================================================================
echo.
echo All dependencies installed!
echo You can now run: run.bat
echo.
pause
