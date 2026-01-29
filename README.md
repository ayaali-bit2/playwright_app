# playwright_app

## Description

A Playwright-based end-to-end testing application demonstrating automated browser and API tests for a sample Todo application.

## Purpose

The purpose of this repository is to provide example Playwright tests showcasing how to configure and run browser-based and API tests using `@playwright/test`.

## Project Structure

```plaintext
.
├── README.md
├── package.json
├── package-lock.json
├── playwright.config.ts
├── utils
│   └── global-cofig.ts
├── tests-examples
│   └── demo-todo-app.spec.ts
└── tests
    ├── api.spec.ts
    ├── basics.spec.ts
    └── todos.spec.ts
```

- **README.md**: Project overview and instructions.
- **package.json / package-lock.json**: Node.js project and dependency configuration.
- **playwright.config.ts**: Playwright test configuration file.
- **utils/global-cofig.ts**: Global setup script for Playwright tests.
- **tests-examples/**: Example Playwright script for a demo Todo app.
- **tests/**: Test suite containing various spec files for functionality, API, and scenarios.

## How to Run

1. Install dependencies:

   ```bash
   npm install
   ```

2. (Optional) Install Playwright browsers:

   ```bash
   npx playwright install
   ```

3. Run tests:

   ```bash
   npx playwright test
   ```

4. View HTML report:

   ```bash
   npx playwright show-report
   ```