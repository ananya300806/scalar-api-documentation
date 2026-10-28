@echo off
cd /d "%~dp0"
echo Starting Scalar project at http://localhost:8000/
echo Press Ctrl+C to stop.
py -m http.server 8000
pause
