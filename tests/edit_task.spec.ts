import { test, expect } from '@playwright/test';

const NEW_TASK_TITLE = 'Editable task title';
const UPDATED_TASK_TITLE = 'Updated task title';

test.use({ storageState: 'storageState.json' });

test.describe('Edit task operation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://todo.qacart.com/login');
  });

  test('should allow updating a task title inline', async ({ page }) => {
    await page.locator('[data-testid="add"]').click();
    await page.locator('[data-testid="new-todo"]').fill(NEW_TASK_TITLE);
    await page.locator('[data-testid="submit-newTask"]').click();

    const taskItems = page.locator('[data-testid="todo-item"]');
    const taskToEdit = taskItems.last();
    await expect(taskToEdit).toBeVisible();

    await taskToEdit.dblclick();
    const editField = taskToEdit.getByRole('textbox', { name: 'Edit' });
    await expect(editField).toHaveValue(NEW_TASK_TITLE);

    await editField.fill(UPDATED_TASK_TITLE);
    await editField.press('Enter');

    await expect(taskToEdit).toContainText(UPDATED_TASK_TITLE);
    await expect(taskToEdit).not.toContainText(NEW_TASK_TITLE);
  });
});
