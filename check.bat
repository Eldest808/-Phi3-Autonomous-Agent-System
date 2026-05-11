@echo off
REM Quick Ollama Status Check

echo.
echo ======================================================================
echo  OLLAMA QUICK DIAGNOSTICS
echo ======================================================================
echo.

echo TEST 1: Is Ollama running?
echo.
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ Ollama is responding
    echo.
    echo TEST 2: What models are installed?
    curl -s http://localhost:11434/api/tags
    echo.
    echo.
    echo TEST 3: Try loading Phi3...
    echo Sending test message to Phi3...
    echo (This will timeout if model is broken)
    timeout /t 3 /nobreak
    ollama run phi3 "hello" 2>&1 | timeout /t 10
) else (
    echo ✗ Ollama is NOT responding
    echo.
    echo SOLUTIONS:
    echo 1. Make sure you ran: ollama serve
    echo 2. It should say: "Listening on 127.0.0.1:11434"
    echo 3. Don't close that window
    echo.
    echo Run this in a NEW terminal:
    echo   ollama serve
)

echo.
echo ======================================================================
echo.
pause
