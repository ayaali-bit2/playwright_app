import { test, expect } from '@playwright/test';

test.describe("todo application", ()=>{

    test.use({
        storageState: "storageState.json"
    })
    test.beforeEach("open the website and login", async({page}) =>{
        await page.goto("https://todo.qacart.com/login");
        
    })


    test("adding item and checkin if checked item or not",async ({page}) => {
        
        await page.locator('[data-testid="add"]').click();

        await page.pause();

        await page.locator('[data-testid="new-todo"]').fill("playwright course");
        await page.locator('[data-testid="submit-newTask"]').click();

        await page.locator('[data-testid="complete-task"]').nth(0).click();

        const item = page.locator('[data-testid="todo-item"]').nth(0);
        await expect(item).toHaveCSS("background-color","rgb(33, 76, 97)");

    })

    test("checking welcome message is displayed or not", async ({page}) =>{

        await page.pause();
        const welcomeMessage = page.locator('[data-testid="welcome"]');
        await expect(welcomeMessage).toBeVisible();
    })


})
    


