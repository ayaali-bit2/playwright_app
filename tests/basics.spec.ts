import { test, expect } from '@playwright/test';
import { TIMEOUT } from 'dns';
import { text } from 'stream/consumers';

test.describe("loging", () =>
{
    test.beforeEach("open the website", async({page}) =>{
        await page.goto("https://todo.qacart.com/login");
    })

    test("should have the correct title", async({page}) => {
        
        const title = await page.title();
        console.log(title);

        await expect(page).toHaveTitle("QAcart Todo App - Login page");
    });

    test("should have the correct URL", async ({page}) => {

        const url = page.url();
        console.log(url);

        await expect(page).toHaveURL("https://todo.qacart.com/");

    })

        test("should have the correct header", async ({page}) => {

        const header =  page.locator(".header");
        //console.log(header);

        await expect(header).toHaveText("Login to Application");

    })

    test("fill the email by using ID", async ({page}) => {

        const emailField =  page.locator("#email");
        await emailField.fill("ayaali@gmail.com");
        await expect(emailField).toHaveValue("ayaali@gmail.com");

    })

    test("fill the password by using css", async ({page}) => {

        const passwordfield =  page.locator('[type="password"]');
        await passwordfield.fill("12345");
        // await page.pause();
        await expect(passwordfield).toHaveValue("12345");
    })

    
    test("fill the password by using xpath", async ({page}) => {

        const passwordfield =  page.locator('//input[@name="password"]');
        await passwordfield.fill("12345");
        // await page.pause();
        await expect(passwordfield).toHaveValue("12345");
    })

    test("click on login button", async ({page}) => {

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

