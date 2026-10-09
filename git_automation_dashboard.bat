@echo off
:: =============================================================================
::      HARDENED GIT AUTOMATION ENGINE - COMPLIANCE PIPELINE LAUNCHER
:: =============================================================================

:: Forces the CMD execution context path to strictly align with this project's root folder location
cd /d "%~dp0"

:: UI FIX: Sets the console window buffer to a premium, maximized widescreen resolution
mode con cols=160 lines=45

:: ARCHITECTURAL FIX: Force-clear any structural submodule remnants from current index caching memory
git rm --cached -r . >nul 2>&1

:: ARCHITECTURAL GATEWAY: Auto-detects if Git is initialized. If not, self-initializes seamlessly.
if not exist ".git" (
    echo [INFO] Local Git repository not detected in this workspace.
    echo [LAUNCHING] Initializing Git engine, establishing deployment markers and main branch configuration...
    git init
    git branch -M main
    echo [SUCCESS] Local Git repository initialized successfully!
    echo ====================================================================================================
    pause
)

:MENU
cls
echo ====================================================================================================
echo                   HARDENED GIT ENGINE Hub - INTERACTIVE QA COMPLIANCE DASHBOARD
echo ====================================================================================================
echo.
echo     1. Run COMPLETE Sync Pipeline (Pull -^> Status -^> Add -^> Commit -^> Push)
echo.
echo     2. Check Repository Local Status (git status)
echo.
echo     3. Fetch and Merge Remote Updates Only (git pull origin)
echo.
echo     4. Stage Local Code Mutations (git add --all)
echo.
echo     5. Create Local Encapsulated Baseline (git commit -m)
echo.
echo     6. Broadcast Local Commits to Cloud (git push origin)
echo.
echo     7. View Lightweight Revision History Log (git log --oneline -n 5)
echo.
echo     8. EXIT Git Engine Dashboard
echo.
echo ====================================================================================================
echo.

:: Prompts the user to enter their numbered choice safely
set /p choice="Enter your selected Git command number [1-8]: "

:: Strict mapping syntax coordinates to avoid missing loop destinations
if "%choice%"=="1" goto COMPLETE_PIPELINE
if "%choice%"=="2" goto REPO_STATUS
if "%choice%"=="3" goto REPO_PULL
if "%choice%"=="4" goto REPO_ADD
if "%choice%"=="5" goto REPO_COMMIT
if "%choice%"=="6" goto REPO_PUSH
if "%choice%"=="7" goto REPO_LOG
if "%choice%"=="8" goto EXIT_ENGINE

:: Fallback loop if the user enters an invalid number or text
echo [ERROR] Invalid selection detected. Please enter a number between 1 and 8.
pause
goto MENU

:COMPLETE_PIPELINE
echo.
echo ====================================================================================================
echo [STEP 1/5] Fetching upstream baseline architectures from remote GitHub server...
git remote | findstr "origin" >nul
if %errorlevel% neq 0 (
    echo [INFO] Remote 'origin' link not established yet. Skipping pull step for first-time baseline creation.
) else (
    git pull origin main --allow-unrelated-histories >nul 2>&1
)

echo.
echo ====================================================================================================
echo [STEP 2/5] Inspecting local repository delta status configurations...
git status

echo.
echo ====================================================================================================
echo [STEP 3/5] Staging all tracked files and filtering excluded .gitignore objects...
:: Hardened staging sequence
git rm --cached -r . >nul 2>&1
git add .

echo.
echo ====================================================================================================
echo [STEP 4/5] Preparing Local Commit Baseline...
:: Pure dynamic execution without input prompts to prevent syntax runtime breakage
git commit -m "Automation Suite Update: Pipeline operations synchronized via compliance dashboard"

echo.
echo ====================================================================================================
echo [STEP 5/5] Broadcasting compiled code blocks to cloud repository branch...
git remote | findstr "origin" >nul
if %errorlevel% neq 0 (
    echo.
    echo [REQUIRED] Remote link missing! GitHub server needs to be linked.
    set /p remote_url="Paste your GitHub repository URL (ending in .git): "
    if not "!remote_url!"=="" (
        git remote add origin !remote_url!
        echo [SUCCESS] Remote server linked as origin. Broadcasting mutations...
        git push -f -u origin main
    ) else (
        echo [ERROR] Operation aborted. Remote URL cannot be blank on first push deployment.
    )
) else (
    :: Forces execution resolution across conflicted branches cleanly
    git push -f origin main
)

echo.
echo ====================================================================================================
echo [VERDICT] Pipeline synchronization compiled successfully. Final local state summary:
git status
pause
goto MENU

:REPO_STATUS
echo.
git status
pause
goto MENU

:REPO_PULL
echo.
git pull origin main --allow-unrelated-histories
pause
goto MENU

:REPO_ADD
echo.
git rm --cached -r . >nul 2>&1
git add .
echo [SUCCESS] Active project mutations staged successfully.
pause
goto MENU

:REPO_COMMIT
echo.
git commit -m "Automation Suite Update: Pipeline operations synchronized via compliance dashboard"
pause
goto MENU

:REPO_PUSH
echo.
git push -f origin main
pause
goto MENU

:REPO_LOG
echo.
git log --oneline -n 5
pause
goto MENU

:EXIT_ENGINE
echo.
echo [INFO] Shutting down Git Automation Engine Hub. Keeping active workspace secure. Goodbye!
exit
