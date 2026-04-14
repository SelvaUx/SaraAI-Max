@echo off
echo.
echo  =============================================
echo   SaraAI Max - Installation
echo   by Selva Pandi (SelvaUx)
echo  =============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

:: Check pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found.
    pause
    exit /b 1
)

echo [1/4] Installing core dependencies...
pip install requests rich psutil

echo.
echo [2/4] Installing SaraAI Max (editable)...
pip install -e .

echo.
echo [3/4] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama not found.
    echo           Download from: https://ollama.com/download
    echo           Then run: ollama pull llama3.2
) else (
    echo [OK] Ollama found.
)

echo.
echo [4/4] Optional: Install voice support?
set /p VOICE="Install voice support? (y/n): "
if /i "%VOICE%"=="y" (
    pip install pyttsx3 SpeechRecognition
    echo NOTE: For PyAudio on Windows, run:
    echo   pip install pipwin
    echo   pipwin install pyaudio
)

echo.
echo  =============================================
echo   Installation Complete!
echo.
echo   Run Sara with:  sara
echo   Or one-shot:    sara "what is machine learning"
echo   Voice mode:     sara --voice
echo   Help:           sara --help
echo  =============================================
echo.
pause
