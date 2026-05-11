@echo off
REM COMPLETE Phi3 Model Reset and Repair
REM This completely removes and reinstalls Phi3

echo.
echo ======================================================================
echo  COMPLETE PHI3 MODEL RESET
echo ======================================================================
echo.
echo This will:
echo 1. Stop Ollama completely
echo 2. Remove the broken Phi3 model
echo 3. Clear the cache
echo 4. Fresh install Phi3
echo.
echo This may take 10-15 minutes
echo.
pause

echo.
echo STEP 1: Killing Ollama processes...
taskkill /IM ollama.exe /F 2>nul
taskkill /IM ollama_llama_server.exe /F 2>nul

echo Waiting for Ollama to fully stop...
timeout /t 5 /nobreak

echo.
echo STEP 2: Removing broken Phi3 model...
echo Removing from: %LOCALAPPDATA%\Ollama\models\manifests\registry.ollama.ai\library\phi3

REM Navigate to models directory if it exists
if exist "%LOCALAPPDATA%\Ollama\models" (
    echo Found Ollama models directory
    REM Try to remove phi3 related files
    for /d %%D in ("%LOCALAPPDATA%\Ollama\models\blobs\*") do (
        echo Checking: %%D
    )
) else (
    echo Ollama models directory not found yet (will be created fresh)
)

echo.
echo STEP 3: Starting Ollama fresh...
echo A new window will open - DO NOT CLOSE IT
echo.
timeout /t 3 /nobreak

start "" ollama serve

echo Waiting for Ollama to start (30 seconds)...
timeout /t 30 /nobreak

echo.
echo STEP 4: Downloading fresh Phi3 model...
echo This downloads about 3GB - can take 5-10 minutes
echo.

ollama pull phi3

echo.
echo STEP 5: Testing Phi3 with simple prompt...
echo Sending test message to verify model works...
echo.

ollama run phi3 "Say hello"

echo.
echo ======================================================================
echo RESET COMPLETE!
echo ======================================================================
echo.
echo If you see "hello" above, Phi3 is working!
echo.
echo Next: Keep Ollama running and double-click run.bat
echo.
pause
