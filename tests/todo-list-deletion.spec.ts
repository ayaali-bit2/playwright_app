import { test, expect } from '@playwright/test';

test.use({ storageState: 'storageState.json' });

test.describe('Todo List - Deletion', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('https://todo.qacart.com/login');
    });

    test('should delete a todo item', async ({ page }) => {
        await page.locator('[data-testid="add"]').click();
        await page.locator('[data-testid="new-todo"]').fill('Item to delete');
        await page.locator('[data-testid="submit-newTask"]').click();

        const item = page.locator('[data-testid="todo-item"]').last();
        await expect(item).toBeVisible();

        await item.locator('[data-testid="delete-task"]').click(); // Modify accordingly to your delete button locator

        await expect(item).not.toBeVisible();
    });
});
