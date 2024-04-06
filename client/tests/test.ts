import { expect, test } from '@playwright/test';

test('index page has expected h1', async ({ page }) => {
	await page.goto('/');
	await expect(page.getByRole('button', { name: 'Create Vote' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'Create Filter' })).toBeVisible();
});
