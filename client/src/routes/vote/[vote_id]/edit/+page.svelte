<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { OptionsService, VotesService, type UpdateVote } from '$lib';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { ArrowRight, CheckCircle, Icon, Play, Stop } from 'svelte-hero-icons';
	import type { PageData } from '../$types';

	export let data: PageData;

	let newOptionTitle: string;
	$: optionButtonActive = newOptionTitle !== undefined && newOptionTitle !== '';
	let optionInput: HTMLInputElement;

	const modalStore = getModalStore();

	async function updateVote() {
		const vote: UpdateVote = {
			title: data.vote.title || '',
			prompt: data.vote.prompt || ''
		};

		try {
			await VotesService.updateVoteVoteVoteIdPost(data.vote._id, vote);
			data.vote = {
				...data.vote,
				...vote
			};
		} catch (error) {
			invalidateAll();
			console.error(error);
		}
	}

	async function createOption() {
		if (newOptionTitle === undefined || newOptionTitle === '') return;

		const newOption = {
			title: newOptionTitle,
			ordering: Math.max(...data.options.map((option) => option.ordering || 0), 0) + 1
		};

		try {
			const response = await OptionsService.addOptionVoteVoteIdOptionPost(data.vote._id, newOption);
			data.options = [...data.options, response];
			data.vote.option_ids.push(response._id);
		} catch (error) {
			invalidateAll();
			console.error(error);
		} finally {
			newOptionTitle = '';
			optionInput.focus();
		}
	}

	async function removeOption(optionId: string) {
		try {
			await OptionsService.removeOptionVoteVoteIdOptionOptionIdDelete(data.vote._id, optionId);
			data.options = data.options.filter((option) => option._id !== optionId);
			data.vote.option_ids = data.vote.option_ids.filter((id) => id !== optionId);
		} catch (error) {
			invalidateAll();
			console.error(error);
		}
	}

	async function sendOptionChange(optionId: string) {
		const option = data.options.find((option) => option._id === optionId);

		if (option === undefined) return;

		// Empty options -> removal
		if (option.title === undefined || option.title === '') {
			await removeOption(optionId);
			return;
		}

		try {
			await OptionsService.updateOptionOptionOptionIdPut(optionId, {
				title: option.title,
				ordering: option.ordering || 0
			});

			// Update the option in the data
			const index = data.options.findIndex((option) => option._id === optionId);
			data.options[index] = {
				...data.options[index],
				...option
			};
		} catch (error) {
			invalidateAll();
			console.error(error);
		}
	}

	async function handleStatusButton() {
		if (!data.vote.started) {
			return confirmStartVote();
		}

		if (!data.vote.stopped) {
			return confirmStopVote();
		}

		// If the vote is stopped, redirect to the results page
		goto(`/vote/${data.vote._id}/results`);
	}

	async function confirmStartVote() {
		modalStore.trigger({
			type: 'confirm',
			title: 'Start Vote',
			body: "You won't be able to make any changes after this.",
			buttonTextConfirm: 'Start Voting',
			buttonTextCancel: 'Cancel',
			response(r) {
				if (r) {
					startVote();
				}
			}
		});
	}

	async function confirmStopVote() {
		modalStore.trigger({
			type: 'confirm',
			title: 'Stop Vote',
			body: 'Users will no longer be able to vote on this.',
			buttonTextConfirm: 'Stop Voting',
			buttonTextCancel: 'Cancel',
			response(r) {
				if (r) {
					stopVote();
				}
			}
		});
	}

	async function startVote() {
		// This function both locks and opens the vote right away.
		// It's more intuitive to the user to lock and open the vote in one go.
		// In the future, if time-based starting and stopping become available,
		// this functionality may be split up.
		try {
			await VotesService.lockVoteVoteVoteIdLockPost(data.vote._id);
			data.vote.editable = false;
			data.options = data.options.map((option) => {
				option.editable = false;
				return option;
			});
			await VotesService.openVoteVoteVoteIdOpenPost(data.vote._id);
			data.vote.started = true;
		} catch (error) {
			invalidateAll();
			console.error(error);
		}
	}

	async function stopVote() {
		try {
			await VotesService.closeVoteVoteVoteIdClosePost(data.vote._id);
			data.vote.stopped = true;
		} catch (error) {
			invalidateAll();
			console.error(error);
		}
	}
</script>

<svelte:head>
	<title>{data.vote.title || 'Votigo'}</title>
</svelte:head>

<div class="container mx-auto flex justify-between p-4">
	<section>
		<h2 class="h2">Edit</h2>
	</section>
	<section>
		<button class="button variant-filled btn" on:click={handleStatusButton}>
			{#if !data.vote.started}
				<span>Start Vote</span>
				<span><Icon src={Play} class="h-6 w-6" /></span>
			{:else if !data.vote.stopped}
				<span>Stop Vote</span>
				<span><Icon src={Stop} class="h-6 w-6" /></span>
			{:else}
				<span>Show Results</span>
				<span><Icon src={ArrowRight} class="h-6 w-6" /></span>
			{/if}
		</button>
	</section>
</div>

<div class="container mx-auto space-y-10 p-4 lg:grid lg:grid-cols-2 lg:gap-4 lg:space-y-0">
	<section class="space-y-2">
		<label for="vote_title" class="h3">Title</label>
		<input
			id="vote_title"
			readonly={!data.vote.editable}
			class="h4 w-full rounded-md p-2 read-only:cursor-not-allowed"
			bind:value={data.vote.title}
			on:change={updateVote}
			placeholder="Auditor 1989"
			type="text"
		/>
	</section>
	<section class="space-y-2">
		<label for="vote_prompt" class="h3">Prompt</label>
		<input
			id="vote_prompt"
			readonly={!data.vote.editable}
			class="w-full rounded-md p-2 read-only:cursor-not-allowed"
			bind:value={data.vote.prompt}
			on:change={updateVote}
			placeholder="Who do you choose as auditor?"
			type="text"
		/>
	</section>
	<section class="space-y-2">
		<h3 class="h3">Choices</h3>
		<div class="grid grid-cols-1 gap-2 sm:grid-cols-2 md:grid-cols-3">
			{#each data.options as option}
				<div class="flex flex-auto items-center gap-2 rounded-md">
					<input
						readonly={!data.vote.editable}
						class="w-full rounded-md p-2 read-only:cursor-not-allowed"
						placeholder=""
						bind:value={option.title}
						on:change={() => sendOptionChange(option._id)}
					/>
				</div>
			{/each}
			{#if data.vote.editable}
				<div class="flex flex-auto items-center gap-2 rounded-md">
					<input
						readonly={!data.vote.editable}
						class="grow rounded-md bg-none p-2 read-only:cursor-not-allowed"
						placeholder="Dr. John Watson"
						bind:this={optionInput}
						bind:value={newOptionTitle}
						on:change={createOption}
					/>
					{#if optionButtonActive}
						<Icon on:click={createOption} src={CheckCircle} class="h-6 w-6 cursor-pointer" />
					{/if}
				</div>
			{/if}
		</div>
	</section>
	<section class="space-y-2">
		<h3 class="h3">Eligibility</h3>
		<pre>TODO Add filter picker / editor</pre>
	</section>
</div>

<!--
<div class="text-sm">
    {#if dev}
    <pre>{JSON.stringify(data, null, 2)}</pre>
    {/if}
</div>
-->
