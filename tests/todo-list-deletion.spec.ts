import { test, expect } from '@playwright/test';

// Ensures the delete action removes a todo item from the list as expected.
test.use({ storageState: 'storageState.json' });

test.describe('Todo List - Deletion', () => {
    test.beforeEach(async ({ page }) => {
        // Reach the login screen so the saved session is applied reliably.
        await page.goto('https://todo.qacart.com/login');
    });

    test('should delete a todo item', async ({ page }) => {
        // Create a todo to delete.
        await page.locator('[data-testid="add"]').click();
        await page.locator('[data-testid="new-todo"]').fill('Item to delete');
        await page.locator('[data-testid="submit-newTask"]').click();

        const item = page.locator('[data-testid="todo-item"]').last();
        await expect(item).toBeVisible();

        await item.locator('[data-testid="delete-task"]').click();

        await expect(item).not.toBeVisible();
    });
});
