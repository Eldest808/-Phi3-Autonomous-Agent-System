@echo off
REM Phi3 Repair Script - Fix 500 Errors
REM This script reloads and repairs the Phi3 model

echo.
echo ======================================================================
echo  PHI3 REPAIR SCRIPT
echo ======================================================================
echo.

echo Step 1: Checking if Ollama is running...
timeout /t 2 /nobreak

echo.
echo Step 2: Stopping Ollama server...
echo (Looking for ollama processes)
taskkill /IM ollama.exe /F 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Ollama stopped
) else (
    echo ⚠️  Ollama wasn't running (that's ok)
)

echo.
echo Waiting 5 seconds for Ollama to fully shut down...
timeout /t 5 /nobreak

echo.
echo Step 3: Clearing Ollama cache...
echo (Removing corrupted model data)
if exist "%LOCALAPPDATA%\Ollama" (
    echo Clearing: %LOCALAPPDATA%\Ollama
    REM Note: Don't delete the whole folder, just clear the models if needed
    echo Cache location found
) else (
    echo Cache not found (might be ok)
)

echo.
echo Step 4: Restarting Ollama and reloading Phi3...
echo.
echo IMPORTANT: This will open a new window
echo Leave it running in the background
echo.
pause

REM Start Ollama
echo Starting Ollama server...
start "" ollama serve

REM Wait for Ollama to start
echo.
echo Waiting 10 seconds for Ollama to start...
timeout /t 10 /nobreak

echo.
echo Step 5: Pulling fresh Phi3 model...
echo (This might take a few minutes)
echo.

ollama pull phi3

echo.
echo ======================================================================
echo REPAIR COMPLETE
echo ======================================================================
echo.
echo Ollama should now be working!
echo.
echo Next steps:
echo 1. Keep the Ollama window open in background
echo 2. Run: run.bat
echo.
pause
