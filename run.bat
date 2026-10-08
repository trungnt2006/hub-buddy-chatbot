@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title HUB-Buddy Web Chatbot Launcher

cd /d "%~dp0"
if exist "chatbot\run.py" cd /d "%~dp0chatbot"

if exist ".venv\Scripts\python.exe" (
    set "PY_EXE=.venv\Scripts\python.exe"
) else (
    set "PY_EXE=py"
)

echo =======================================================
echo          HUB-Buddy Web Chatbot Launcher
echo =======================================================
echo.
echo [1] Kiem tra Python tai: %PY_EXE%
echo [2] Dang mo trinh duyet tai: http://127.0.0.1:2610
echo [3] Dang khoi dong may chu... Nhan Ctrl+C de dung.
echo.

start http://127.0.0.1:2610

"%PY_EXE%" run.py

if errorlevel 1 (
    echo.
    echo [LOI] May chu dung dot ngot hoac cong 2610 dang ban.
    pause
)
