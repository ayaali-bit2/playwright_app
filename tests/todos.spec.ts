import { test, expect } from '@playwright/test';

 test.describe("todo application", ()=>{

    test.use({
        storageState: "storageState.json"
    })

    test.beforeEach("open the website and login", async ({ page }) => {
        await page.goto("https://todo.qacart.com/login");
    })

    test("checking welcome message is displayed or not", async ({ page }) => {
        await page.pause();
        const welcomeMessage = page.locator('[data-testid="welcome"]');
        await expect(welcomeMessage).toBeVisible();
    })

    test("should update an existing todo item", async ({ page }) => {
        // Add a new todo item to edit
        await page.locator('[data-testid="add"]').click();
        await page.locator('[data-testid="new-todo"]').fill('task to update');
        await page.locator('[data-testid="submit-newTask"]').click();

        const todoItems = page.getByTestId('todo-item');
        const firstTodo = todoItems.nth(0);
        // Enter edit mode
        await firstTodo.dblclick();
        // Fill new value and save
        await firstTodo.getByRole('textbox', { name: 'Edit' }).fill('updated task');
        await firstTodo.getByRole('textbox', { name: 'Edit' }).press('Enter');

        // Assert the updated text is displayed
        await expect(firstTodo).toHaveText('updated task');
    })

});
