import { test, expect } from '@playwright/test';

test.use({ storageState: 'storageState.json' });

test('adding item and checking if checked item or not', async ({ page }) => {
    await page.locator('[data-testid="add"]').click();
    await page.locator('[data-testid="new-todo"]').fill('New Todo Item');
    await page.locator('[data-testid="submit-newTask"]').click();

    const item = page.locator('[data-testid="todo-item"]').last();
    await expect(item).toBeVisible();
    await item.locator('[data-testid="complete-task"]').click();
    await expect(item).toHaveCSS('background-color', 'rgb(33, 76, 97)');
});
