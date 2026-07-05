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

test.describe("todo application", () => {

    test.use({
        storageState: "storageState.json"
    });

    test.beforeEach("open the website", async ({ page }) => {
        await openLoginPage(page);
    });

    test("checking welcome message is displayed or not", async ({ page }) => {
        await page.pause();
        await verifyWelcomeMessage(page);
    });

});
