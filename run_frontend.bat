@echo off
echo =======================================================
echo Starting PhishTrace SOC Frontend Application...
echo =======================================================
cd /d "%~dp0frontend"
npm run dev
pause
