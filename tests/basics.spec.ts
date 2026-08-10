import { test, expect } from '@playwright/test';

const BASE_URL = process.env.APP_BASE_URL ?? 'https://todo.qacart.com';
const TEST_EMAIL = process.env.APP_TEST_EMAIL ?? 'ayaali20@gmail.com';
const TEST_PASSWORD = process.env.APP_TEST_PASSWORD ?? 'Aya123ali@';

test.describe("loging", () =>
{
    test.beforeEach("open the website", async({page}) =>{
        await page.goto(`${BASE_URL}/login`);
    })

    test("should have the correct title", async({page}) => {

        const title = await page.title();
        console.log(title);

        await expect(page).toHaveTitle("QAcart Todo App - Login page");
    });

    test("should have the correct URL", async ({page}) => {

        const url = page.url();
        console.log(url);

        await expect(page).toHaveURL(`${BASE_URL}/`);

    })

        test("should have the correct header", async ({page}) => {

        const header =  page.locator(".header");
        //console.log(header);

        await expect(header).toHaveText("Login to Application");

    })

    test("fill the email by using ID", async ({page}) => {

        const emailField =  page.locator("#email");
        await emailField.fill(TEST_EMAIL);
        await expect(emailField).toHaveValue(TEST_EMAIL);

    })

    test("fill the password by using css", async ({page}) => {

        const passwordfield =  page.locator('[type="password"]');
        await passwordfield.fill(TEST_PASSWORD);
        // await page.pause();
        await expect(passwordfield).toHaveValue(TEST_PASSWORD);
    })


    test("fill the password by using xpath", async ({page}) => {

        const passwordfield =  page.locator('//input[@name="password"]');
        await passwordfield.fill(TEST_PASSWORD);
        // await page.pause();
        await expect(passwordfield).toHaveValue(TEST_PASSWORD);
    })

    test("click on login button", async ({page}) => {

        await page.locator("#email").fill(TEST_EMAIL);
        await page.locator('[type="password"]').fill(TEST_PASSWORD);
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
