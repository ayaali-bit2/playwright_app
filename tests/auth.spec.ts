import { test, expect } from '@playwright/test';

const API_BASE = process.env.APP_API_BASE ?? 'http://127.0.0.1:5000/api';
const CREDENTIALS = { username: 'demo', password: 'demo123' };

// Authentication API contract tests covering login, status checks, and logout behavior.
test.describe('authentication API', () => {
  test('allows login with valid credentials and returns the user payload', async ({ request }) => {
    // Send a login request with known credentials and assert the success payload.
    const response = await request.post(`${API_BASE}/auth/login`, { data: CREDENTIALS });

    expect(response.status()).toBe(200);
    const payload = await response.json();
    expect(payload).toMatchObject({
      message: 'Login successful.',
    });
    expect(payload.user).toMatchObject({
      username: 'demo',
      display_name: 'Demo User',
    });
  });

  test('returns 401 status if no session exists when checking auth status', async ({ request }) => {
    // Request the status endpoint without an authenticated session to ensure it rejects.
    const response = await request.get(`${API_BASE}/auth/status`);

    expect(response.status()).toBe(401);
    const payload = await response.json();
    expect(payload).toMatchObject({
      authenticated: false,
    });
  });

  test('enforces logout by clearing the existing session', async ({ request }) => {
    // Use a dedicated context to log in, verify status, log out, and then assert the session is cleared.
    const context = await request.newContext();

    const loginResponse = await context.post(`${API_BASE}/auth/login`, { data: CREDENTIALS });
    expect(loginResponse.status()).toBe(200);

    const statusBefore = await context.get(`${API_BASE}/auth/status`);
    expect(statusBefore.status()).toBe(200);

    const logoutResponse = await context.post(`${API_BASE}/auth/logout`);
    expect(logoutResponse.status()).toBe(200);

    const statusAfter = await context.get(`${API_BASE}/auth/status`);
    expect(statusAfter.status()).toBe(401);
    const payload = await statusAfter.json();
    expect(payload).toMatchObject({ authenticated: false });
  });
});
