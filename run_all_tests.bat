@echo off
:: QA AUTOMATION FRAMEWORK HUB - ENTERPRISE RUNNER INTERFACE WITH QA DASHBOARD ENGINE
cls
:menu
echo =================================================================
echo        PRODUCT MANAGER QA AUTOMATION ECOSYSTEM RUNNER
echo =================================================================
echo  1. Run All 52 Suite Tests (Complete Integration Local Report)
echo  2. Run Integration Suite Only (test_product_flow.py - 28 Tests)
echo  3. Run Web API Network Suite Only (test_product_api.py - 10 Tests)
echo  4. Run UI Form Functional Suite Only (test_browser_forms.py - 6 Tests)
echo  5. Run UI Navigation E2E Suite Only (test_browser_navigation.py - 5 Tests)
echo  6. Run Isolated Unit Mock Suite Only (test_product_unit.py - 3 Tests)
echo  7. RUN EXPERIMENTAL SUITE - BROADCAST DIRECTLY TO JIRA CLOUD XRAY (Testing Mode)
echo  8. Launch Advanced QA Git Automation Dashboard (Dynamic CLI Tool)
echo  9. Exit Framework Automation Runner Hub
echo =================================================================
set /p choice="Select an architectural layer execution path (1-9): "

if "%choice%"=="1" (
    echo Launching complete 52 test execution routine...
    call .venv\Scripts\activate
    pytest tests/ --html=reports/complete_automation_report.html --self-contained-html --cache-clear -v
    pause
    goto menu
)
if "%choice%"=="2" (
    echo Executing 28 Integration Matrix layer tests...
    call .venv\Scripts\activate
    pytest tests/test_product_flow.py --html=reports/integration_report.html --self-contained-html -v
    pause
    goto menu
)
if "%choice%"=="3" (
    echo Testing 10 RESTful API network endpoints...
    call .venv\Scripts\activate
    pytest tests/test_product_api.py --html=reports/api_testing_report.html --self-contained-html -v
    pause
    goto menu
)
if "%choice%"=="4" (
    echo Activating 6 UI Form Selenium browser processes...
    call .venv\Scripts\activate
    pytest tests/test_browser_forms.py --html=reports/ui_browser_report.html --self-contained-html -v
    pause
    goto menu
)
if "%choice%"=="5" (
    echo Activating 5 UI E2E window navigation scripts...
    call .venv\Scripts\activate
    pytest tests/test_browser_navigation.py --html=reports/ui_navigation_report.html --self-contained-html -v
    pause
    goto menu
)
if "%choice%"=="6" (
    echo Evaluating 3 Isolated Unit validation Mock channels...
    call .venv\Scripts\activate
    pytest tests/test_product_unit.py --html=reports/unit_tests_report.html --self-contained-html -v
    pause
    goto menu
)
if "%choice%"=="7" (
    echo [EXPERIMENTAL] Activating cloud gateway tunnel and broadcasting results to Jira Xray...
    call .venv\Scripts\activate
    pytest tests/ --cache-clear -v
    pause
    goto menu
)
if "%choice%"=="8" (
    echo Launching dynamic QA Version Control Dashboard...
    call .venv\Scripts\activate
    python git_automation_dashboard.py
    if errorlevel 1 (
        echo [Critical Error] The Python controller crashed or failed to load.
        pause
    )
    goto menu
)
if "%choice%"=="9" exit
goto menu
