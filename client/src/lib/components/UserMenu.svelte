<script lang="ts">
	import {
		ArrowRightEndOnRectangle,
		ArrowRightStartOnRectangle,
		Bars3,
		Cog,
		Icon,
		Plus
	} from 'svelte-hero-icons';

	import { goto } from '$app/navigation';
	import { FiltersService, VotesService } from '$lib';
	import { signIn, signOut, signedIn, userName } from '$lib/components/AuthContext.svelte';

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
		<button class="btn" on:click={toggleMenu}>
			<span>{$userName}</span>
			<span><Icon src={Bars3} class="h-6 w-6" /></span>
		</button>
	{:else}
		<button class="btn" on:click={signIn}>
			<span>Log In</span>
			<span><Icon src={ArrowRightEndOnRectangle} class="h-6 w-6" /></span>
		</button>
	{/if}
	{#if menuOpen}
		<div
			class="btn-group-vertical variant-filled absolute right-0 top-full z-10 flex items-end rounded-md p-2"
			on:click={toggleMenu}
			on:keypress={checkMenuKey}
			role="menu"
			tabindex="0"
		>
			<button on:click={createVote} type="button" class="group">
				<span>Create Vote</span>
				<span><Icon src={Plus} class="group-hover:text-success-500 h-6 w-6" /></span>
			</button>
			<button on:click={createFilter} type="button" class="group">
				<span>Create Filter</span>
				<span><Icon src={Plus} class="group-hover:text-success-500 h-6 w-6" /></span>
			</button>
			<button on:click={toggleMenu} type="button" class="group">
				<span>Settings</span>
				<span><Icon src={Cog} class="group-hover:text-primary-500 h-6 w-6" /></span>
			</button>
			<button on:click={signOut} on:click={toggleMenu} type="button" class="group">
				<span>Log Out</span>
				<span
					><Icon
						src={ArrowRightStartOnRectangle}
						class="group-hover:text-error-500 h-6 w-6"
					/></span
				>
			</button>
		</div>
	{/if}
</div>
