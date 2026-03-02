import { test, expect } from '@playwright/test';

const LOGIN_URL = 'https://todo.qacart.com/login';
const APP_URL = 'https://todo.qacart.com/';

test.describe('Login scenario', () => {
  test('authenticates via the UI and lands on the todos page', async ({ page }) => {
    await page.goto(LOGIN_URL);

    await page.locator('#email').fill('ayaali20@gmail.com');
    await page.locator('[type="password"]').fill('Aya123ali@');
    const loginButton = page.getByRole('button', { name: /login/i });

    await Promise.all([
      page.waitForURL(APP_URL),
      loginButton.click(),
    ]);

    await expect(page).toHaveTitle('QAcart Todo App - Todos page');
    await expect(page.getByTestId('welcome')).toBeVisible();
  });
});

test.describe('Logout scenario', () => {
  test.use({ storageState: 'storageState.json' });

  test('logs out and returns to the login screen', async ({ page }) => {
    await page.goto(APP_URL);
    const logoutButton = page.getByRole('button', { name: /logout/i });
    await expect(logoutButton).toBeVisible();

    await Promise.all([
      page.waitForURL(/\/login/),
      logoutButton.click(),
    ]);

    await expect(page.getByRole('heading', { name: 'Login to Application' })).toBeVisible();
    await expect(page.locator('#email')).toBeVisible();
  });
});
