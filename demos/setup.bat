@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (echo Requesting administrative privileges... & goto UACPrompt) else ( goto gotAdmin )
:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs" & del "%temp%\getadmin.vbs" & exit /B
:gotAdmin
if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
pushd "%CD%" & CD /D "%~dp0"
:--------------------------------------

:: SCRIPT STARTS HERE WITH ADMIN RIGHTS
echo.
echo === STEP 1: Installing Chocolatey Package Manager ===
call install-chocolatey.bat

echo.
echo --- Chocolatey installation process finished. ---
echo.
echo === STEP 2: Installing Application Dependencies ===
echo A NEW window will now open to install Tesseract, Ghostscript, etc.
echo Please follow the prompts in the new window.
echo.
pause
echo Launching dependency installer...

start "Installing Dependencies" cmd /c "install-dependencies.bat & pause"

exit /B