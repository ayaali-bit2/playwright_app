import { test, expect } from '@playwright/test';

test.use({ storageState: 'storageState.json' });

test.describe('Todo List - Add Invalid Input Handling', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://todo.qacart.com/login');
  });

  test('should show error when adding an empty todo', async ({ page }) => {
    await page.locator('[data-testid="add"]').click();
    await page.locator('[data-testid="new-todo"]').fill('');
    await page.locator('[data-testid="submit-newTask"]').click();

    const error = page.locator('[data-testid="error-message"]');
    await expect(error).toBeVisible();
    await expect(error).toHaveText('Task cannot be empty');
  });

  test('should show error when adding a too long todo', async ({ page }) => {
    const longText = 'A'.repeat(256);
    await page.locator('[data-testid="add"]').click();
    await page.locator('[data-testid="new-todo"]').fill(longText);
    await page.locator('[data-testid="submit-newTask"]').click();

    const error = page.locator('[data-testid="error-message"]');
    await expect(error).toBeVisible();
    await expect(error).toHaveText('Task cannot exceed 255 characters');
  });
});
