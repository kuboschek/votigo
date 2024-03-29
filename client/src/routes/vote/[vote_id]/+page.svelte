<script lang="ts">
	import { dev } from '$app/environment';
	import { invalidateAll } from '$app/navigation';
	import {
		VotesService,
		type UpdateVote,
		type Vote,
		type UpdateOption,
		OptionsService
	} from '$lib';
	import type { PageData } from './$types';

	export let data: PageData;

	let newOptionTitle: string;
	let optionInput: HTMLInputElement;

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

	async function sendOptionChange(optionId: string) {
		const option = data.options.find((option) => option._id === optionId);

		if (option === undefined) return;

		// Empty options -> removal
		if (option.title === undefined || option.title === '') {
			try {
				await OptionsService.removeOptionVoteVoteIdOptionOptionIdDelete(data.vote._id, optionId);
				data.options = data.options.filter((option) => option._id !== optionId);
				data.vote.option_ids = data.vote.option_ids.filter((id) => id !== optionId);
			} catch (error) {
				invalidateAll();
				console.error(error);
			}
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
</script>

<svelte:head>
	<title>{data.vote.title || 'Votigo'}</title>
</svelte:head>

<div class="container mx-auto p-4">
	<h2 class="h2">Edit</h2>
</div>

<div class="container mx-auto space-y-10 p-4 lg:grid lg:grid-cols-2 lg:gap-4 lg:space-y-0">
	<section class="space-y-2">
		<label for="vote_title" class="h3">Title</label>
		<input
			id="vote_title"
			readonly={!data.vote.editable}
			class="h4 w-full rounded-md p-2"
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
			class="w-full rounded-md p-2"
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
				<div class="flex-auto">
					<input
						readonly={!data.vote.editable}
						class="w-full rounded-md p-2"
						placeholder=""
						bind:value={option.title}
						on:change={() => sendOptionChange(option._id)}
					/>
				</div>
			{/each}
			<div class="flex-auto">
				<input
					readonly={!data.vote.editable}
					class="w-full rounded-md p-2"
					placeholder="Dr. John Watson"
					bind:this={optionInput}
					bind:value={newOptionTitle}
					on:change={createOption}
				/>
			</div>
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
