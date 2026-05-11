@echo off
REM Simple Ollama Restart

echo.
echo ======================================================================
echo  OLLAMA RESTART
echo ======================================================================
echo.

echo STEP 1: Stopping all Ollama processes...
taskkill /IM ollama.exe /F 2>nul
taskkill /IM ollama_llama_server.exe /F 2>nul

echo Waiting 3 seconds...
timeout /t 3 /nobreak

echo.
echo STEP 2: Starting Ollama fresh...
echo.
echo A window will open saying:
echo "Listening on 127.0.0.1:11434"
echo.
echo DO NOT CLOSE THAT WINDOW!
echo.
pause

start "Ollama Server" cmd /k "ollama serve"

echo.
echo Waiting 15 seconds for Ollama to start...
timeout /t 15 /nobreak

echo.
echo STEP 3: Loading Phi3 model...
echo.
ollama run phi3 "Say hello"

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✓ SUCCESS! Phi3 is working!
    echo.
    echo You can now close this window and run: run.bat
) else (
    echo ✗ FAILED - Phi3 is still broken
    echo.
    echo Try this:
    echo 1. Run: ollama pull phi3
    echo 2. Wait for it to download
    echo 3. Then run this script again
)

echo.
pause
