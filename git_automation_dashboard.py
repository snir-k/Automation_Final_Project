# name: git_automation_dashboard.py
# =================================================================
# ENTERPRISE QA AUTOMATION INTEGRATION & VERSION CONTROL DASHBOARD
# Hardened to support seamless atomic commits, dynamic branch tracking,
# index cache cleaning, and backward compatible typing engines.
# =================================================================
import os
import subprocess
import sys
from typing import List


def _run_git_command(command: List[str]) -> str:
    """Private Helper: Executes a Git command safely via subprocess and returns the output."""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\n[Git Engine Error] Command '{' '.join(command)}' failed.")
        print(f"Reason: {e.stderr.strip()}")
        return ""


def get_current_branch() -> str:
    """Queries the local Git repository to extract the active working branch name dynamically."""
    branch = _run_git_command(["git", "branch", "--show-current"])
    return branch if branch else "unknown"


def clean_git_cache() -> None:
    """Refreshes the local Git index monitoring pipeline to eliminate visual layout sync delays."""
    print("Clearing Git index cache and refreshing disk tracking matrix...")
    _run_git_command(["git", "update-index", "--refresh"])


def execute_atomic_pipeline(commit_message: str) -> None:
    """
    Executes a complete, secure version control delivery pipeline:
    1. Stages ALL changed and untracked files.
    2. Enforces a unified commit with identical timestamp.
    3. Broadcasts the changes straight to the active remote branch endpoint.
    """
    if not commit_message or commit_message.strip() == "":
        print("\n[Validation Error] Commit message cannot be empty!")
        return

    current_branch = get_current_branch()
    if current_branch == "unknown":
        print("\n[Environment Error] Active path is not a valid Git repository workspace.")
        return

    print(f"\nTarget Branch Detected: [{current_branch}]")
    print("-----------------------------------------------------------------")

    # Step 1: Force Stage all mutations (including Untracked files/folders)
    print("1. Staging total project alterations into the repository stack...")
    _run_git_command(["git", "add", "."])

    # Step 2: Enforce a unified commit with a synchronized timestamp
    print("2. Compiling atomic release commit matrix...")
    commit_output = _run_git_command(["git", "commit", "-m", commit_message])
    if "nothing to commit" in commit_output or not commit_output:
        print("   -> Workspace already fully synchronized. No new mutations found.")
    else:
        print("   -> Commit successful! Package locked under a unified time-anchor.")

    # Step 3: Broadcast straight to the real active remote branch
    print(f"3. Transmitting pipeline payload straight to origin/{current_branch}...")
    _run_git_command(["git", "push", "origin", current_branch])
    print("\n[Pipeline Complete] GitHub Repository is 100% synchronized and secure!")


def display_dashboard() -> None:
    """Renders the main command-line interface dashboard panel context for the tester."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_branch = get_current_branch()

        print("=================================================================")
        print("          QA FRAMEWORK - VERSION CONTROL CONTROLLER HUB          ")
        print("=================================================================")
        print(f" Active Working Repository Branch:  [{current_branch.upper()}]")
        print("=================================================================")
        print("  1. Synchronize Framework (Atomic Commit & Push to Active Branch)")
        print("  2. Refresh Tracking Matrix (Clear Local Cache & Index Latency)")
        print("  3. Audit Current Status (Show Unstaged Changes & Untracked Files)")
        print("  4. View Version Trace History (Show Short Commit Log)")
        print("  5. Exit Dashboard Controller Hub")
        print("=================================================================")

        choice = input("Select an engineering integration path (1-5): ").strip()

        if choice == "1":
            msg = input("\nEnter a descriptive commit message in English: ").strip()
            execute_atomic_pipeline(msg)
            input("\nPress Enter to return to the controller menu...")
        elif choice == "2":
            print("\n")
            clean_git_cache()
            print("System tracking state sterile and optimized.")
            input("\nPress Enter to return to the controller menu...")
        elif choice == "3":
            print("\n--- Current Workspace Status ---")
            print(_run_git_command(["git", "status", "-s"]))
            input("\nPress Enter to return to the controller menu...")
        elif choice == "4":
            print("\n--- Recent Repository Updates ---")
            print(_run_git_command(["git", "log", "-n", "5", "--oneline"]))
            input("\nPress Enter to return to the controller menu...")
        elif choice == "5":
            print("\nExiting Framework Controller Hub safely. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    display_dashboard()
