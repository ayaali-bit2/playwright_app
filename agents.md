# agents.md

## Project Description

`playwright_app` is a sample automated testing project built with Playwright and TypeScript. It demonstrates end-to-end and API testing techniques against web applications.

**Package name:** `playwrite_project`  
**Playwright version:** ^1.54.2

## Project Structure

```
.
├── .gitignore
├── package.json
├── package-lock.json
├── README.md
├── playwright.config.ts
├── utils
│   └── global-cofig.ts
├── tests
│   ├── basics.spec.ts
│   ├── todos.spec.ts
│   └── api.spec.ts
└── tests-examples
    └── demo-todo-app.spec.ts
```

## Usage Instructions

### Prerequisites

- Node.js (>=14.x)
- NPM (>=6.x)

### Installation

```bash
npm install
```

### Running Tests

Run all tests:
```bash
npx playwright test
```

Generate and view the HTML report:
```bash
npx playwright test --reporter=html
npx playwright show-report
```

Run a specific test file:
```bash
npx playwright test tests/api.spec.ts
```

### Configuration

Tests are configured via `playwright.config.ts`. The test directory is `tests`, with additional examples in `tests-examples`. Global setup is defined in `utils/global-cofig.ts`.
