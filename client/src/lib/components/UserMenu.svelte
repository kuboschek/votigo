<script lang="ts">
	import { Icon, UserCircle } from 'svelte-hero-icons';

	import { signIn, signOut, signedIn, userName } from '$lib/components/AuthContext.svelte';

	async function handleUserMenuButtonClick() {
		if ($signedIn) {
			await signOut();
		} else {
			await signIn();
		}
	}
</script>

<button class="btn" on:click={handleUserMenuButtonClick}>
	<span><Icon src={UserCircle} class="h-6 w-6" /></span>
	{#if $signedIn}
		<span>{$userName}</span>
	{:else}
		<span>Sign In</span>
	{/if}
</button>
