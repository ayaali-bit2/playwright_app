import { test, expect, Page } from '@playwright/test';

// Helper Functions
async function openLoginPage(page: Page) {
    await page.goto("https://todo.qacart.com/login");
}

async function getWelcomeMessage(page: Page) {
    return page.locator('[data-testid="welcome"]');
}

async function verifyWelcomeMessage(page: Page) {
    const welcomeMessage = await getWelcomeMessage(page);
    await expect(welcomeMessage).toBeVisible();
}

// Create a new todo
async function createTodo(page: Page, item: string) {
    await page.locator('[data-testid="add"]').fill(item);
    await page.locator('[data-testid="submit-newTask"]').click();
}

// Verify a todo exists
async function verifyTodoExists(page: Page, item: string) {
    await expect(page.locator(`text=${item}`)).toBeVisible();
}

test.describe("todo application", () => {

    test.use({
        storageState: "storageState.json"
    });

    test.beforeEach("open the website", async ({ page }) => {
        await openLoginPage(page);
    });

    test("checking welcome message is displayed or not", async ({ page }) => {
        await verifyWelcomeMessage(page);
    });

    test("should create a new todo", async ({ page }) => {
        const todo = "Learn Playwright";

        await createTodo(page, todo);
        await verifyTodoExists(page, todo);
    });

});
