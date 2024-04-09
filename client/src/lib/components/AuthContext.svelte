<script context="module" lang="ts">
	import { dev } from '$app/environment';
	import { env } from '$env/dynamic/public';
	import { OpenAPI } from '$lib';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { UserManager } from 'oidc-client-ts';
	import { onMount, setContext } from 'svelte';
	import { writable } from 'svelte/store';

	const userName = writable<string>('');
	const signedIn = writable(false);

	const userManager = new UserManager({
		authority: env.PUBLIC_OIDC_AUTHORITY,
		client_id: env.PUBLIC_OIDC_CLIENT_ID,
		redirect_uri: env.PUBLIC_BASE_URL + '/auth/callback',
		scope: env.PUBLIC_OIDC_SCOPES
	});

	async function signIn() {
		try {
			const user = await userManager.signinPopup();
			signedIn.set(true);
			userName.set(user.profile.name ?? user.profile.sub);
			OpenAPI.TOKEN = user.id_token;

			if (dev) {
				OpenAPI.USERNAME = undefined;
				OpenAPI.PASSWORD = undefined;
			}

			return user;
		} catch (error) {
			console.error(error);
			throw error;
		}
	}

	async function signOut() {
		try {
			userManager.signoutSilent();
			signedIn.set(false);
			userName.set('');
			OpenAPI.TOKEN = undefined;

			if (dev) {
				OpenAPI.USERNAME = 'fake';
				OpenAPI.PASSWORD = 'fake';
			}
		} catch (error) {
			console.error(error);
			throw error;
		}
	}

	export { signedIn, userName, signIn, signOut };
</script>

<script lang="ts">
	async function handleOnMount() {
		const params = new URLSearchParams(window.location.search);
		if (params.has('code') && params.has('state')) {
			await userManager.signinCallback();
		}
	}
	onMount(handleOnMount);

	setContext('auth', userManager);
</script>

<slot />
