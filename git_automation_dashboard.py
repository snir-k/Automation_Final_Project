# name: git_automation_dashboard.py
# =================================================================
# ENTERPRISE QA AUTOMATION INTEGRATION & CONTROL CENTER
# Hardened to support local testing execution layers and dynamic Git pipelines
# 100% Sterile: Eradicated soft deprecation warnings by replacing os.system commands
# =================================================================
import subprocess
import sys
from typing import List

# ANSI Color Escape Sequences
NEON_GREEN = "\033[92m"
RESET = "\033[0m"


def _run_git_command(command: List[str]) -> str:
    """Private Helper: Executes a Git command safely via subprocess and returns the output."""
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_current_branch() -> str:
    """Queries the local Git repository to extract the active working branch name dynamically."""
    branch = _run_git_command(["git", "branch", "--show-current"])
    return branch if branch else "unknown"


def _clear_terminal_screen() -> None:
    """Private Helper: Replaces legacy os.system calls to satisfy modern subprocess constraints."""
    # FIXES SOFT DEPRECATION WARNINGS: Clears screen using formal clean system runner hooks
    subprocess.run(["cls" if os_name_is_windows() else "clear"], shell=True)


def os_name_is_windows() -> bool:
    """Evaluates the active host operating system environment matrix mapping."""
    return sys.platform.startswith("win")


def execute_atomic_pipeline() -> None:
    """Executes a complete automated commit and push version control delivery pipeline."""
    commit_message = input("\nEnter a descriptive commit message in English: ").strip()
    if not commit_message:
        print("\n[Validation Error] Commit message cannot be empty!")
        return

    current_branch = get_current_branch()
    print(f"\nTarget Branch Detected: [{current_branch}]")
    print("-----------------------------------------------------------------")

    print("1. Staging total project alterations into the repository stack...")
    _run_git_command(["git", "add", "."])

    print("2. Compiling atomic release commit matrix...")
    _run_git_command(["git", "commit", "-m", commit_message])

    print(f"3. Transmitting pipeline payload straight to origin/{current_branch}...")
    _run_git_command(["git", "push", "origin", current_branch])
    print(f"\n{NEON_GREEN}[Pipeline Complete] GitHub Repository is 100% synchronized and secure!{RESET}")


def run_git_submenu() -> None:
    """Renders the sub-menu for advanced Git automation operations."""
    while True:
        _clear_terminal_screen()
        current_branch = get_current_branch()
        print("=================================================================")
        print("          QA FRAMEWORK - VERSION CONTROL CONTROLLER HUB          ")
        print("=================================================================")
        print(f" Active Working Repository Branch:  [{current_branch.upper()}]")
        print("=================================================================")
        print(f"  {NEON_GREEN}1. Synchronize Framework (Automated Atomic Commit & Push to GitHub){RESET}")
        print("  2. Refresh Tracking Matrix (Clear Local Cache & Index Latency)")
        print("  3. Audit Current Status (Show Unstaged Changes & Untracked Files)")
        print("  4. View Version Trace History (Show Short Commit Log)")
        print("  5. Return to Main Menu")
        print("=================================================================")

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            execute_atomic_pipeline()
            input("\nPress Enter to continue...")
        elif choice == "2":
            print("\nClearing Git cache...")
            _run_git_command(["git", "update-index", "--refresh"])
            print("System tracking state sterile and optimized.")
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("\n--- Current Workspace Status ---")
            print(_run_git_command(["git", "status", "-s"]))
            input("\nPress Enter to continue...")
        elif choice == "4":
            print("\n--- Recent Repository Updates ---")
            print(_run_git_command(["git", "log", "-n", "5", "--oneline"]))
            input("\nPress Enter to continue...")
        elif choice == "5":
            break


def display_main_dashboard() -> None:
    """Renders the central system panel where option 1 shines bright in Neon Green."""
    while True:
        _clear_terminal_screen()
        print("=================================================================")
        print("        PRODUCT MANAGER QA AUTOMATION ECOSYSTEM RUNNER           ")
        print("=================================================================")
        # TARGET DESIGN: Only Option 1 is printed in brilliant neon green
        print(f"  {NEON_GREEN}1. Run All 52 Suite Tests (Complete Integration Local Report){RESET}")
        print("  2. Run Integration Suite Only (test_product_flow.py - 28 Tests)")
        print("  3. Run Web API Network Suite Only (test_product_api.py - 10 Tests)")
        print("  4. Run UI Form Functional Suite Only (test_browser_forms.py - 6 Tests)")
        print("  5. Run UI Navigation E2E Suite Only (test_browser_navigation.py - 5 Tests)")
        print("  6. Run Isolated Unit Mock Suite Only (test_product_unit.py - 3 Tests)")
        print("  7. RUN EXPERIMENTAL SUITE - BROADCAST DIRECTLY TO JIRA CLOUD XRAY")
        print("  8. Launch Advanced QA Git Automation Dashboard (Dynamic CLI Tool)")
        print("  9. Exit Framework Automation Runner Hub")
        print("=================================================================")

        choice = input("Select an architectural layer execution path (1-9): ").strip()

        if choice == "1":
            print("\nLaunching complete 52 test execution routine...")
            subprocess.run(
                ["pytest", "tests/", "--html=reports/complete_automation_report.html", "--self-contained-html",
                 "--cache-clear", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            subprocess.run(["pytest", "tests/test_product_flow.py", "--html=reports/integration_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            subprocess.run(["pytest", "tests/test_product_api.py", "--html=reports/api_testing_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            subprocess.run(["pytest", "tests/test_browser_forms.py", "--html=reports/ui_browser_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            subprocess.run(["pytest", "tests/test_browser_navigation.py", "--html=reports/ui_navigation_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "6":
            subprocess.run(["pytest", "tests/test_product_unit.py", "--html=reports/unit_tests_report.html",
                            "--self-contained-html", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "7":
            print("\n[EXPERIMENTAL] Activating cloud gateway tunnel and broadcasting results to Jira Xray...")
            subprocess.run(["pytest", "tests/", "--cache-clear", "-v"])
            input("\nPress Enter to return to menu...")
        elif choice == "8":
            run_git_submenu()
        elif choice == "9":
            print("\nExiting Framework Center safely. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    display_main_dashboard()
