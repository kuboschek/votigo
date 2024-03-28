// place files you want to import through the `$lib` alias in this folder.
import { dev } from '$app/environment';
import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { OpenAPI } from './client';

OpenAPI.BASE = PUBLIC_API_BASE_URL;

if (dev) {
    OpenAPI.USERNAME = 'fake';
    OpenAPI.PASSWORD = 'fake';
}

export * from './client';