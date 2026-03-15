import { test, expect } from '@playwright/test';
import { TIMEOUT } from 'dns';
import { text } from 'stream/consumers';

// Smoke tests for QA Cart login page verifying critical layout and input behaviors.
test.describe("loging", () =>
{
    // Always navigate to the login page at the start of each test for consistency.
    test.beforeEach("open the website", async({page}) =>{
        await page.goto("https://todo.qacart.com/login");
    })

    test("should have the correct title", async({page}) => {
        // Expect the browser tab to reflect the login experience.
        const title = await page.title();
        console.log(title);

        await expect(page).toHaveTitle("QAcart Todo App - Login page");
    });

    test("should have the correct URL", async ({page}) => {
        // Verify the page resolves to the canonical login URL.
        const url = page.url();
        console.log(url);

        await expect(page).toHaveURL("https://todo.qacart.com/");

    })

    test("should have the correct header", async ({page}) => {
        // Confirm the header text explicitly states the page purpose.
        const header =  page.locator(".header");
        //console.log(header);

        await expect(header).toHaveText("Login to Application");

    })

    test("fill the email by using ID", async ({page}) => {
        // Ensure the email input can be targeted by its ID and accepts typing.
        const emailField =  page.locator("#email");
        await emailField.fill("ayaali@gmail.com");
        await expect(emailField).toHaveValue("ayaali@gmail.com");

    })

    test("fill the password by using css", async ({page}) => {
        // Validate filling the password input when selecting via CSS attribute selectors.
        const passwordfield =  page.locator('[type="password"]');
        await passwordfield.fill("12345");
        // await page.pause();
        await expect(passwordfield).toHaveValue("12345");
    })

    
    test("fill the password by using xpath", async ({page}) => {
        // Assert the same password field can be located through XPath expressions.
        const passwordfield =  page.locator('//input[@name="password"]');
        await passwordfield.fill("12345");
        // await page.pause();
        await expect(passwordfield).toHaveValue("12345");
    })

    test("click on login button", async ({page}) => {
        // Execute the login flow and confirm navigation to the todos page.
        await page.locator("#email").fill("ayaali20@gmail.com");
        await page.locator('[type="password"]').fill("Aya123ali@");
        const loginButton =  page.locator('button:has-text("Login")');
        await loginButton.waitFor({
            state:"visible",
            timeout: 90000
        });
        loginButton.click();
        // await page.pause();
        await expect(page).toHaveTitle("QAcart Todo App - Todos page");
    })

});
