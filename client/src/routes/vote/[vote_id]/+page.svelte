<script lang="ts">
	import { dev } from '$app/environment';
	import { ApiError, VotesService } from '$lib';
	import { getModalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import { ArrowRight, ExclamationTriangle, Icon } from 'svelte-hero-icons';
	import type { PageData } from '../$types';
	import { goto } from '$app/navigation';

	export let data: PageData;
	$: canBeVotedOn = !data.vote.editable && data.vote.started && !data.vote.stopped;

	let selectedOptionId: string;

	const modalStore = getModalStore();

	async function selectOption(optionId: string) {
		console.log(optionId);
		selectedOptionId = optionId;
	}

	async function handleVoteButton() {
		try {
			await VotesService.voteVoteVoteIdVotePost(data.vote._id, selectedOptionId);
            const successModal: ModalSettings = {
                type: 'alert',
                title: 'Success',
                body: 'Your vote has been counted!',
                modalClasses: '!bg-success-500 !text-white',
                buttonTextCancel: 'Close',

                response(r) {
                    goto('/');
                }
            };

            modalStore.trigger(successModal);
		} catch (error) {
			const apiError = error as ApiError;

			const errorModal: ModalSettings = {
				type: 'alert',
				title: 'Error',
				body: apiError.body.detail || apiError.statusText || 'An error occurred',
				modalClasses: '!bg-error-500 !text-white'
			};

			modalStore.trigger(errorModal);
		}
	}
</script>

<svelte:head>
	<title>{data.vote.title || 'Votigo'}</title>
</svelte:head>

<div class="container mx-auto p-4 flex justify-between">
	<section>
		<h2 class="h2">{data.vote.title}</h2>
		<p class="text-gray-500">{data.vote.prompt}</p>
	</section>
    {#if !canBeVotedOn}
    <section>
        <div class="card p-4 bg-warning-500 border border-warning-400 shadow flex gap-2">
            <span>
                <Icon src={ExclamationTriangle} class="h-6 w-6" />
            </span>
            <span>
                This vote is not open yet.
            </span>
        </div>
    </section>
    {/if}
</div>

<div class="container mx-auto grid grid-cols-1 gap-2 p-4 sm:grid-cols-2 md:grid-cols-3">
	{#each data.options as option}
		<button
			class:variant-filled-primary={option._id === selectedOptionId}
			class="card flex flex-auto items-center gap-2 rounded-md transition-colors"
			on:click={() => selectOption(option._id)}
		>
			<span class="w-full rounded-md p-2">{option.title}</span>
		</button>
	{/each}
</div>

<div class="container mx-auto flex justify-end p-4">
	<button
		disabled={!selectedOptionId || !canBeVotedOn}
		class="button btn variant-filled"
		on:click={handleVoteButton}
	>
		<span>Confirm</span>
		<span><Icon src={ArrowRight} class="h-6 w-6" /></span>
	</button>
</div>

{#if dev}
	<div class="container mx-auto p-4">
		<pre>{JSON.stringify(data, null, 2)}</pre>
	</div>
{/if}
