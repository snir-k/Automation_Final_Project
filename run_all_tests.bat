@echo off
:: QA AUTOMATION FRAMEWORK HUB - ENTERPRISE CONTROL ROOT
cls
echo Loading QA Framework Automation Control Center...
call .venv\Scripts\activate
python git_automation_dashboard.py
if errorlevel 1 (
    echo [Critical Error] The Python central dashboard failed to load.
    pause
)
exit
