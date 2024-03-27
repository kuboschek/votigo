// place files you want to import through the `$lib` alias in this folder.
import { PUBLIC_API_BASE_URL } from '$env/static/public';
import { OpenAPI } from './client';

OpenAPI.BASE = PUBLIC_API_BASE_URL;
OpenAPI.USERNAME = 'fake';
OpenAPI.PASSWORD = 'fake';

export * from './client';