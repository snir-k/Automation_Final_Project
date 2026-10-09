@echo off
:: =============================================================================
::      AUTOMATED QA EXECUTION ENGINE - INTERACTIVE DASHBOARD (48 TESTS)
:: =============================================================================

:: Forces the CMD execution context path to strictly align with this file's root folder location
cd /d "%~dp0"

:MENU
cls
echo =============================================================================
echo               AUTOMATED QA TEST ENGINE - EXECUTION INTERACTIVE MENU
echo =============================================================================
echo  1. Run COMPLETE Suite (All 48 Tests + Generate Full HTML Report)
echo  2. Run ONLY Backend Integration Tests (test_product_flow.py - 26 Tests)
echo  3. Run ONLY Isolated Unit Tests (test_product_unit.py - 3 Tests with Mocks)
echo  4. Run ONLY Web API Testing Suite (test_product_api.py - 8 Requests Tests)
echo  5. Run ONLY Browser UI Forms Suite (test_browser_forms.py - 6 Selenium Tests)
echo  6. Run ONLY Browser UI Navigation Suite (test_browser_navigation.py - 5 Tests)
echo  7. Run ONLY Defensive and Robustness Tests (-m negative / -m types)
echo  8. EXIT Engine Dashboard
echo =============================================================================
echo.

:: Prompts the user to enter their numbered choice safely
set /p choice="Enter your selected execution number [1-8]: "

:: Activating the local virtual environment natively before running any test selection
call .venv\Scripts\activate

if "%choice%"=="1" goto COMPLETE
if "%choice%"=="2" goto INTEGRATION
if "%choice%"=="3" goto UNIT
if "%choice%"=="4" goto API
if "%choice%"=="5" goto FORMS
if "%choice%"=="6" goto NAVIGATION
if "%choice%"=="7" goto DEFENSIVE
if "%choice%"=="8" goto EXIT_ENGINE

:: Fallback loop if the user enters an invalid number or text
echo [ERROR] Invalid selection detected. Please enter a number between 1 and 8.
pause
goto MENU

:COMPLETE
echo.
echo [LAUNCHING] Executing all 48 test cases and generating compiled dashboard report...
pytest tests/ --html=reports/complete_automation_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:INTEGRATION
echo.
echo [LAUNCHING] Executing 26 backend integration test cases...
pytest tests/test_product_flow.py --html=reports/integration_tests_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:UNIT
echo.
echo [LAUNCHING] Executing 3 isolated unit tests utilizing MagicMock injection...
pytest tests/test_product_unit.py --html=reports/unit_tests_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:API
echo.
echo [LAUNCHING] Executing 8 REST API bare-metal requests tests with timestamp logic...
pytest tests/test_product_api.py --html=reports/api_testing_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:FORMS
echo.
echo [LAUNCHING] Executing 6 browser interface forms tests via Selenium...
:: FIX: Directed natively to the physical filename endpoint to ensure 100% item collection
pytest tests/test_browser_forms.py --html=reports/ui_forms_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:NAVIGATION
echo.
echo [LAUNCHING] Executing 5 browser viewport routing and window title verification tests...
:: FIX: Directed natively to the physical filename endpoint to ensure 100% item collection
pytest tests/test_browser_navigation.py --html=reports/ui_navigation_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:DEFENSIVE
echo.
echo [LAUNCHING] Executing payload hardening and runtime type validation guard clauses...
pytest tests/ -m "negative or types" --html=reports/defensive_hardening_report.html --self-contained-html --cache-clear -v
pause
goto MENU

:EXIT_ENGINE
echo.
echo [INFO] Shutting down QA Automation Dashboard Engine. Goodbye!
exit
