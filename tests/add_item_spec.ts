import { test, expect } from '@playwright/test';

// Verifies adding a todo item and marking it as complete behaves as expected.
test.use({ storageState: 'storageState.json' });

test('adding item and checking if checked item or not', async ({ page }) => {
    // Open the form that lets users add a new task.
    await page.locator('[data-testid="add"]').click();
    await page.locator('[data-testid="new-todo"]').fill('New Todo Item');
    await page.locator('[data-testid="submit-newTask"]').click();

    const item = page.locator('[data-testid="todo-item"]').last();
    await expect(item).toBeVisible();
    // Mark the newly created task as complete and assert the visual styling.
    await item.locator('[data-testid="complete-task"]').click();
    await expect(item).toHaveCSS('background-color', 'rgb(33, 76, 97)');
});
