# playwright_app

## Project Overview
`playwright_app` is a lightweight Playwright test automation project built with TypeScript that demonstrates how to structure and maintain reliable end-to-end and API test suites using the modern `@playwright/test` tooling.

## Getting Started

### Prerequisites
- Node.js (v14 or newer) with npm installed
- Browsers supported by Playwright (Chromium, Firefox, WebKit); you can install them via Playwright

### Installation
1. Install dependencies:
   ```bash
   npm install
   ```
2. (Optional, but recommended) Install Playwright browsers:
   ```bash
   npx playwright install
   ```

## Running Tests
- Run the full suite:
  ```bash
  npx playwright test
  ```
- Run a specific spec file:
  ```bash
  npx playwright test tests/api.spec.ts
  ```
- Generate and inspect the HTML report:
  ```bash
  npx playwright test --reporter=html
  npx playwright show-report
  ```
- Launch the interactive Playwright Test UI for debugging:
  ```bash
  npx playwright test --ui
  ```

## Repository Layout
- `tests/` – Core Playwright specs covering workflows such as basics, todos, and API validations.
- `tests-examples/` – Additional exploratory specs and demonstrations of Playwright features.
- `utils/global-config.ts` – Shared setup logic invoked before the test suite runs.
- `playwright.config.ts` – Main configuration file that controls retries, reporters, projects, and shared test options.
- `agents.md` – Companion documentation describing the repo conventions and tooling guidance.

## Configuration Highlights
- `testDir` is defined as `./tests`, so all core specs are picked up automatically.
- `globalSetup` points to `./utils/global-config.ts` for shared initialization and fixtures.
- The Chromium project runs with headless mode disabled locally so developers can observe browser behavior, while trace collection (`trace: 'on'`) aids debugging failed runs.
- On CI (`process.env.CI`), retries are enabled (`retries: 2`) and worker count is limited (`workers: 1`) to keep runs stable, while reporting defaults to `html` for easy inspection.

## Tips for Contributors
- Keep tests deterministic by isolating browser contexts with Playwright fixtures and avoiding shared state between specs.
- Use `npx playwright show-report` immediately after failures to review screenshots, trace files, and logs that reveal what went wrong.
- Document any new fixtures or helpers inside `utils/global-config.ts` so the shared test setup remains transparent.
- Place experimental flows or prototype scenarios inside `tests-examples/` before promoting them to the main `tests/` directory.

## Troubleshooting & Further Reading
- Re-run isolated specs via `npx playwright test <path>` when investigating flaky failures.
- Review the `playwright.config.ts` file to understand project definitions, browser options, and environment-specific overrides.
- Playwright’s Trace Viewer can reconstruct step-by-step execution when retries produce trace artifacts ― load them with `npx playwright show-trace <trace.zip>`.

## Contributing
Open issues or submit pull requests to expand coverage, integrate new workflows, or add automation helpers. Playwright’s configuration and fixture system makes it easy to extend the harness while keeping it maintainable and readable.