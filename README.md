# playwright_app

A full-stack test project that combines:

- **Playwright** end-to-end tests (TypeScript)
- A lightweight **Flask backend** (Python) with auth + todo APIs
- A simple **frontend** (`frontend/index.html`)
- Backend API tests with **pytest**

This repo is useful as a playground for UI/API automation and authenticated test flows.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [1) Backend Setup (Python)](#1-backend-setup-python)
  - [2) Playwright Setup (Node.js)](#2-playwright-setup-nodejs)
- [Running the Project](#running-the-project)
  - [Run Backend API](#run-backend-api)
  - [Run Playwright Tests](#run-playwright-tests)
  - [Run Backend Pytest Suite](#run-backend-pytest-suite)
- [Configuration Notes](#configuration-notes)
- [Test Organization](#test-organization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Project Overview

The repository contains two complementary testing surfaces:

1. **Browser E2E tests** in `tests/` using Playwright.
2. **Backend API tests** in `backend/tests/` using pytest.

Authentication and todo operations are handled by the Flask backend, while Playwright tests validate browser-level behavior and user flows.

---

## Repository Structure

```text
playwright_app/
├── backend/
│   ├── app.py                      # Flask app, todo/session endpoints
│   ├── requirements.txt            # Python dependencies
│   ├── todos.json                  # Persisted todo data store
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── controller.py           # Auth/user logic
│   │   └── routes.py               # Auth routes (register/login/logout/status)
│   └── tests/
│       └── test_auth_endpoints.py  # pytest API tests for auth
├── frontend/
│   └── index.html                  # Simple frontend page
├── tests/                          # Playwright test suite
│   ├── basics.spec.ts
│   ├── auth.spec.ts
│   ├── api.spec.ts
│   ├── add_item_spec.ts
│   ├── todos.spec.ts
│   ├── todo-list-deletion.spec.ts
│   └── storageState.json
├── tests-examples/
│   └── demo-todo-app.spec.ts       # Example Playwright tests
├── utils/
│   └── global-config.ts            # Playwright global setup
└── playwright.config.ts            # Playwright configuration
```

---

## Tech Stack

- **Frontend testing:** Playwright (`@playwright/test`)
- **Backend:** Flask + CORS
- **Backend testing:** pytest
- **Language mix:** TypeScript + Python

---

## Prerequisites

- **Node.js** 18+ (recommended)
- **Python** 3.10+ (recommended)
- npm (or compatible JS package manager)
- pip / virtualenv

---

## Setup

### 1) Backend Setup (Python)

From repository root:

```bash
cd backend
python -m venv .venv
```

Activate virtual environment:

- macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```
- Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 2) Playwright Setup (Node.js)

From repository root, install Playwright project dependencies (if not already installed in your environment), then install browser binaries:

```bash
npx playwright install
```

> If your environment uses a package manager lockfile, run your project’s dependency install first (for example `npm install`) before `npx playwright install`.

---

## Running the Project

### Run Backend API

From `backend/`:

```bash
python app.py
```

If your environment prefers Flask CLI:

```bash
flask --app app run
```

The API should start locally and be available for UI/API test workflows.

---

### Run Playwright Tests

From repo root:

```bash
npx playwright test
```

Open HTML report:

```bash
npx playwright show-report
```

Run a single spec:

```bash
npx playwright test tests/auth.spec.ts
```

Run with headed browser (useful for debugging):

```bash
npx playwright test --headed
```

---

### Run Backend Pytest Suite

From `backend/`:

```bash
pytest
```

Run a specific file:

```bash
pytest tests/test_auth_endpoints.py
```

---

## Configuration Notes

Playwright is configured in `playwright.config.ts` with:

- `testDir: './tests'`
- `globalSetup: './utils/global-config.ts'`
- HTML reporter
- Chromium project enabled
- Trace collection enabled (`trace: 'on'`)
- `headless: false` currently set for Chromium

If you want CI-friendly behavior, consider enabling headless mode for CI runs.

---

## Test Organization

### Playwright (`tests/`)
- UI basics and auth scenarios
- API-oriented checks from test layer
- Todo creation/deletion flows
- Shared auth/session state via `storageState.json` and global setup

### Pytest (`backend/tests/`)
- Auth endpoint validation:
  - required fields
  - invalid credentials
  - duplicate usernames
  - password boundaries
  - successful register/login behavior

---

## Troubleshooting

- **Backend not reachable from tests**
  - Ensure Flask app is running before executing tests that depend on API availability.
- **Playwright browser missing**
  - Run `npx playwright install`.
- **Auth/session-related failures**
  - Re-run tests after clearing old state files if your local session data is stale.
- **Port conflicts**
  - Stop the process using the backend port or run backend on a different port and align test configuration.

---

## Contributing

1. Create a feature branch.
2. Make focused changes (tests, backend, or config).
3. Run:
   - Playwright tests (root)
   - pytest suite (`backend/`)
4. Open a PR with clear description and test evidence.

---

If you’d like, I can also add:
- a **Quick Start** section with copy/paste commands only,
- a **CI example** (GitHub Actions),
- and an **API endpoints table** directly in this README.
