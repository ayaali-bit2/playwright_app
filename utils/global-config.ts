import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.resolve(__dirname, "../.env") });

import { request } from "@playwright/test";

async function globalSetup() {

    // const browser = await chromium.launch();
    // const page = await browser.newPage();

    // await page.goto("https://todo.qacart.com/login");

    // await page.locator('[data-testid="email"]').fill("ayaali20@gmail.com");
    // await page.locator('[type="password"]').fill("Aya123ali@");
    // const loginButton =  page.locator('button:has-text("Login")');
    // await loginButton.click();

    // const welcomeMessage = page.locator('[data-testid="welcome"]');
    // await expect(welcomeMessage).toBeVisible();

    // await page.context().storageState({ 
    //     path : "storageState.json"
    // })

    const requestContext = await request.newContext();
    await requestContext.post("https://todo.qacart.com/api/v1/users/login",{
        data:{
            email: process.env.USER_EMAIL,
            password: process.env.USER_PASSWORD
        }
    })

    await requestContext.storageState({
        path: path.resolve(__dirname, "../tests/storageState.json"),
    })
}

export default globalSetup;