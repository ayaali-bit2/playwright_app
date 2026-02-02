import { test, expect } from '@playwright/test';

test.describe("todo application", ()=>{

    test.use({
        storageState: "storageState.json"
    })
    test.beforeEach("open the website and login", async({page}) =>{
        await page.goto("https://todo.qacart.com/login");
        
    })



    test("checking welcome message is displayed or not", async ({page}) =>{

        await page.pause();
        const welcomeMessage = page.locator('[data-testid="welcome"]');
        await expect(welcomeMessage).toBeVisible();
    })


})
    


