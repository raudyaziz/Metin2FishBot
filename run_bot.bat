@echo off
rem Metin2 runs as administrator, so the bot must too or Windows drops its clicks.
net session >nul 2>&1
if errorlevel 1 (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"
call metin2\Scripts\activate.bat
python hack.py
if errorlevel 1 pause
