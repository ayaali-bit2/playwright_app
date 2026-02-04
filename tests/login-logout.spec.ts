import { test, expect } from '@playwright/test';

const BASE_URL = 'https://todo.qacart.com';
const LOGIN_URL = `${BASE_URL}/login`;
const TODO_APP_URL = BASE_URL;
const USER_EMAIL = 'ayaali20@gmail.com';
const USER_PASSWORD = 'Aya123ali@';

test.describe('Login and Logout Tests', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto(LOGIN_URL);
    await page.locator('#email').fill(USER_EMAIL);
    await page.locator('[type="password"]').fill(USER_PASSWORD);
    const loginButton = page.locator('button:has-text("Login")');
    await loginButton.waitFor({ state: 'visible', timeout: 90000 });
    await loginButton.click();
    await expect(page).toHaveTitle('QAcart Todo App - Todos page');
    await expect(page.locator('[data-testid="welcome"]')).toBeVisible();
  });

  test.use({ storageState: 'storageState.json' });

  test('should logout and redirect to login page', async ({ page }) => {
    await page.goto(TODO_APP_URL);
    const logoutButton = page.locator('button:has-text("Logout")');
    await expect(logoutButton).toBeVisible();
    await logoutButton.click();
    await expect(page).toHaveURL(LOGIN_URL);
  });
});
