@echo off
echo =======================================================
echo Running PhishTrace Backend Pytest Suite...
echo =======================================================
cd /d "%~dp0backend"
python -m pytest tests
echo.
echo =======================================================
echo Building PhishTrace Frontend Bundle...
echo =======================================================
cd /d "%~dp0frontend"
npm run build
pause
