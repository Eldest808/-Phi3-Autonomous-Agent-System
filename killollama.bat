@echo off
REM Kill All Ollama Processes and Clear Port

echo.
echo ======================================================================
echo  KILLING ALL OLLAMA PROCESSES
echo ======================================================================
echo.

echo Finding and killing Ollama processes...
echo.

REM Kill all ollama processes
tasklist | find /I "ollama" >nul
if %ERRORLEVEL% EQU 0 (
    echo Found Ollama processes, killing them...
    taskkill /F /IM ollama.exe 2>nul
    taskkill /F /IM ollama_llama_server.exe 2>nul
    taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Ollama*" 2>nul
    echo ✓ Ollama processes killed
) else (
    echo No Ollama processes found
)

echo.
echo Waiting 5 seconds for port to clear...
timeout /t 5 /nobreak

echo.
echo ======================================================================
echo  VERIFYING PORT IS CLEAR
echo ======================================================================
echo.

echo Checking if port 11434 is available...
netstat -ano | find ":11434" >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 11434 still in use!
    echo Trying alternative method...
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":11434"') do (
        echo Killing process %%a
        taskkill /PID %%a /F 2>nul
    )
    echo Waiting 5 more seconds...
    timeout /t 5 /nobreak
) else (
    echo ✓ Port 11434 is free
)

echo.
echo ======================================================================
echo  STARTING OLLAMA
echo ======================================================================
echo.

echo Starting Ollama on port 11434...
echo A new window will open - DO NOT CLOSE IT
echo.
timeout /t 2 /nobreak

start "Ollama Server" ollama serve

echo Waiting 10 seconds for Ollama to start...
timeout /t 10 /nobreak

echo.
echo ✓ Ollama should now be running!
echo Keep this window in the background.
echo.
pause
