<script lang="ts">
	import {
		ArrowRightEndOnRectangle,
		ArrowRightStartOnRectangle,
		Bars3,
		Cog,
		Icon,
		Plus,
		XMark
	} from 'svelte-hero-icons';

	import { goto } from '$app/navigation';
	import { FiltersService, VotesService } from '$lib';
	import { signIn, signOut, signedIn, userName } from '$lib/components/AuthContext.svelte';
	import UserMenuButton from './UserMenuButton.svelte';

	let menuOpen = false;

	async function toggleMenu() {
		menuOpen = !menuOpen;
	}

	async function checkMenuKey(event: KeyboardEvent) {
		if (event.key === 'Space') {
			menuOpen = false;
		}
	}

	async function createVote() {
		const vote = await VotesService.createVoteVotePost();

		if (vote) {
			goto(`/vote/${vote.vote._id}/edit`);
		}
		return vote;
	}

	async function createFilter() {
		const filter = await FiltersService.createFilterFilterPost();

		if (filter) {
			goto(`/filter/${filter._id}`);
		}
		return filter;
	}
</script>

<div class="relative">
	{#if $signedIn}
		{#if menuOpen}
			<button class="btn" on:click={toggleMenu}>
				<span>Close Menu</span>
				<span><Icon src={XMark} class="h-6 w-6" /></span>
			</button>
		{:else}
			<button class="btn" on:click={toggleMenu}>
				<span>{$userName}</span>
				<span><Icon src={Bars3} class="h-6 w-6" /></span>
			</button>
		{/if}
	{:else}
		<button class="btn" on:click={signIn}>
			<span>Log In</span>
			<span><Icon src={ArrowRightEndOnRectangle} class="h-6 w-6" /></span>
		</button>
	{/if}
	{#if menuOpen}
		<div
			class="btn-group-vertical variant-filled absolute right-0 top-full z-10 flex items-end rounded-md py-2"
			on:click={toggleMenu}
			on:keypress={checkMenuKey}
			role="menu"
			tabindex="0"
		>
			<UserMenuButton iconSrc={Plus} hoverColorClass="text-success-500" on:click={createVote}>
				Create Vote
			</UserMenuButton>
			<UserMenuButton iconSrc={Plus} hoverColorClass="text-success-500" on:click={createFilter}>
				Create Filter
			</UserMenuButton>
			<UserMenuButton iconSrc={Cog} hoverColorClass="text-primary-500" on:click={toggleMenu}>
				Settings
			</UserMenuButton>
			<UserMenuButton
				iconSrc={ArrowRightStartOnRectangle}
				hoverColorClass="text-error-500"
				on:click={signOut}
			>
				Log Out
			</UserMenuButton>
		</div>
	{/if}
</div>
