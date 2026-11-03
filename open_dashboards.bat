@echo off
cd /d "%~dp0"
echo Server running - keep this window open. Close it to stop.
start "" http://localhost:8765/dividend/dashboard.html
start "" http://localhost:8765/etf/etf_dashboard.html
python -m http.server 8765
