@echo off
cd /d "%~dp0"
echo Waiting 7 minutes before running rar.bat...
timeout /t 450 /nobreak
call join_and_crop.bat