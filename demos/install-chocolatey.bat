@echo off
echo --- Checking for Chocolatey ---
WHERE choco >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Chocolatey not found. Installing now...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
) ELSE (
    echo Chocolatey is already installed.
)