import { test, expect, type Page } from '@playwright/test';

const TODO_ITEMS = [
  'buy some cheese',
  'feed the cat',
  'book a doctors appointment',
] as const;

test.beforeEach(async ({ page }) => {
  await page.goto('https://demo.playwright.dev/todomvc');
});

test.describe('Locator and keyboard examples', () => {
  test('filters todo items with a locator and verifies the visible count', async ({ page }) => {
    await createDefaultTodos(page);

    const todoItems = page.getByTestId('todo-item');
    await todoItems.nth(1).getByRole('checkbox').check();

    await page.getByRole('link', { name: 'Active' }).click();

    const activeItems = page.getByTestId('todo-item');
    await expect(activeItems).toHaveCount(2);
    await expect(activeItems).toHaveText([
      TODO_ITEMS[0],
      TODO_ITEMS[2],
    ]);
    await expect(activeItems.filter({ hasText: TODO_ITEMS[1] })).toHaveCount(0);
  });

  test('creates a todo using keyboard interaction', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');

    await newTodo.pressSequentially('learn keyboard shortcuts');
    await newTodo.press('Enter');

    const todoItem = page.getByTestId('todo-item').last();
    await expect(todoItem).toHaveText('learn keyboard shortcuts');
    await expect(newTodo).toBeEmpty();
  });
});

test.describe('Accessibility and validation examples', () => {
  test('exposes the expected todo controls through accessible roles', async ({ page }) => {
    await createDefaultTodos(page);

    const firstTodo = page.getByTestId('todo-item').first();
    await expect(firstTodo.getByRole('checkbox')).toBeVisible();
    await expect(firstTodo.getByRole('checkbox')).not.toBeChecked();
    await expect(firstTodo.getByRole('button', { name: 'Delete' })).toBeVisible();
    await expect(page.getByRole('main')).toBeVisible();
  });

  test('does not create a todo from whitespace-only input', async ({ page }) => {
    const newTodo = page.getByPlaceholder('What needs to be done?');

    await newTodo.fill('   ');
    await newTodo.press('Enter');

    await expect(page.getByTestId('todo-item')).toHaveCount(0);
    await expect(newTodo).toBeEmpty();
  });
});

test.describe('Completed-item workflow examples', () => {
  test('clears completed items and preserves active items', async ({ page }) => {
    await createDefaultTodos(page);

    const todoItems = page.getByTestId('todo-item');
    await todoItems.nth(1).getByRole('checkbox').check();

    await page.getByRole('button', { name: 'Clear completed' }).click();

    await expect(page.getByTestId('todo-item')).toHaveCount(2);
    await expect(page.getByTestId('todo-title')).toHaveText([
      TODO_ITEMS[0],
      TODO_ITEMS[2],
    ]);
    await expect(page.getByRole('button', { name: 'Clear completed' })).toBeHidden();
  });
});

async function createDefaultTodos(page: Page) {
  const newTodo = page.getByPlaceholder('What needs to be done?');

  for (const item of TODO_ITEMS) {
    await newTodo.fill(item);
    await newTodo.press('Enter');
  }
}
