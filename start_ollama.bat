@echo off
REM Start Ollama Server

echo.
echo ======================================================================
echo  STARTING OLLAMA SERVER
echo ======================================================================
echo.
echo Starting Ollama...
echo.
echo IMPORTANT:
echo - This window will stay open
echo - DO NOT CLOSE THIS WINDOW
echo - Keep it running in the background
echo - You should see: "Listening on 127.0.0.1:11434"
echo.
echo ======================================================================
echo.

ollama serve

echo.
echo Ollama stopped! If you closed this by accident, run this script again.
pause
