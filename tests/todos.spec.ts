import { test, expect } from '@playwright/test';

// Tests focused on authenticated todo interactions using the persisted storage state.
test.describe("todo application", ()=>{

    test.use({
        storageState: "storageState.json"
    })
    // Ensure the storage state takes effect by visiting the login page before each test.
    test.beforeEach("open the website and login", async({page}) =>{
        await page.goto("https://todo.qacart.com/login");
        
    })


    test("checking welcome message is displayed or not", async ({page}) =>{
        // Validate that the welcome banner is visible for authenticated users.
        await page.pause();
        const welcomeMessage = page.locator('[data-testid="welcome"]');
        await expect(welcomeMessage).toBeVisible();
    })


})
    


