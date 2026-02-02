import { test, expect } from '@playwright/test';

// Reuse saved authentication state
test.use({ storageState: 'storageState.json' });

// Navigate to the app before each test
test.beforeEach('open the website and login', async ({ page }) => {
  await page.goto('https://todo.qacart.com/login');
});

// Verify that a new todo item can be added successfully
test('should add a new todo item', async ({ page }) => {
  await page.locator('[data-testid="add"]').click();
  const newTodo = 'New Todo Item';
  await page.locator('[data-testid="new-todo"]').fill(newTodo);
  await page.locator('[data-testid="submit-newTask"]').click();

  const addedItem = page.locator('[data-testid="todo-item"]').last();
  await expect(addedItem).toHaveText(newTodo);
  await expect(addedItem).toBeVisible();
});
