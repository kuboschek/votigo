import { test } from '@playwright/test';

test('index page has expected container', async ({ page }) => {
	await page.goto('/');
	const container = await page.$('.container');
});
