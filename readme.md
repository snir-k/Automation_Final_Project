# 🛒 Product Management System - Automation Testing Framework v2.0

Comprehensive Enterprise-Grade Automation Testing Architecture built using **Python, Flask, Pytest, and Selenium WebDriver**. This repository contains the hardened **Sprint 2 (v2.0)** pipeline release, featuring full payload sanitization, binary file persistence, and automated regression testing.

---

## 📈 System Maturity Overview
* **Baseline Sprint 1:** 10 Known Bugs Detected | 48 Test Iterations Compiled (1 Expected Failure).
* **Hardened Sprint 2 (Current):** 13 Structural Vulnerabilities Destroyed | **52 Automated Test Iterations Passed (100% Success Rate)**.
* **Warning & Code Quality Metrics:** 0 Static Linter Warnings | 0 Redundant Declarations | 100% Sterile PyCharm Project Workspace.

---

## 🛠️ Sprint 2 Architectural Enhancements & Defect Resolutions

### 1. Backend Security Hardening (`app.py` & `product_service.py`)
* **Bug #11 (Whitespace Injections Destroyed):** Implemented strict alphanumeric regular expression engines (`re.compile`) across both Client-side (`static/main.js`) and Backend API Gateways to eliminate raw space injections in Product Names and Image fields.
* **Bug #13 (Payload Security & Malicious Extensions):** Enforced a secure strict filename extension whitelist matching `.png`, `.jpg`, and `.jpeg` only. Any bypass vectors attempting malicious format compilation (e.g., `.exe`, `.sh`) are instantly trapped and rejected with a `400 Bad Request`.
* **Bug #16 (Float Casting Validation Guard):** Isolated parsing routines with a non-disruptive validation abstraction hook (`_is_valid_float`) to intercept non-numeric raw parameters, preventing server crashes (`Status 500`) and enforcing graceful standard error responses.

### 2. UI/UX Synchronization & Modernized Core Framework (`static/main.js`)
* **Binary File Upload Interceptor:** Upgraded the legacy JSON pipeline into a dynamic `FormData` API. Browser executions handle physical image uploads directly to disk storage layers, syncing assets onto the live DOM interface.
* **Dynamic Short Timestamps (HHMM):** Eradicated string duplication memory overload on product row refreshes by locking short 4-digit dynamic clock timestamps (e.g., `1546`), preventing column text padding breakage.
* **DOM Event Binding Compliance:** Removed inline deprecated HTML listeners (`onsubmit`) to align with contemporary DOM standards, migrating triggers to decoupled `addEventListener` declarations.

---

## 🧪 Automated Testing Architecture Matrix

The suite enforces an exhaustive **52 Test Iterations Matrix** across 5 isolated layers:

| Target Layer Module | Component / Logic Under Test | Active Test Volume | Execution Profile |
| :--- | :--- | :---: | :--- |
| `tests/test_product_flow.py` | DB Matrix Constraints, Type Safety & Duplicate Bounds | **28 Tests** | Pytest DB Fixtures |
| `tests/test_product_api.py` | Network Boundaries, Parametrized Form Payloads | **10 Tests** | Flask Test Client |
| `tests/test_browser_forms.py` | UI Interceptors, Alphanumeric Validation Boxes | **6 Tests** | Selenium Headless Chrome |
| `tests/test_browser_navigation.py`| E2E Window Trace Router Navigation and Redirect Links | **5 Tests** | Selenium Wait Conditions |
| `tests/test_product_unit.py` | Isolated Business Logic and Mock Services Channel | **3 Tests** | Unittest Mock Framework |

---

## 💻 Local Testing & Execution Environment

### Prerequisites
Ensure your local workspace satisfies the updated dependencies inside `pyproject.toml`:
* `pytest >= 9.1.1`
* `pytest-html >= 4.2.0`
* `selenium >= 4.0.0`
* `flask >= 3.0.0`
* `pymysql >= 1.1.0`

### Step-by-Step Deployment
1. Fire up the central Flask application engine:
   ```bash
   python app.py
   ```
2. Launch the local automation console matrix using our dynamic dashboard interface file:
   ```bash
   run_all_tests.bat
   ```
3. To trigger local executions select option `1`. To evaluate our custom inline **Jira Xray Pipeline Broadcaster Hub**, choose option `7` to forward bundled payload reports straight to Issue `KAN-14`.
