<script lang="ts">
	import { goto } from '$app/navigation';
    import { VotesService, type ReadFullVote, FiltersService } from '$lib'
	import { Icon, Plus } from 'svelte-hero-icons';

    async function createVote() {
        const vote = await VotesService.createVoteVotePost()

        if(vote) {
            goto(`/vote/${vote.vote._id}/edit`)
        }
        return vote
    }

    async function createFilter() {
        const filter = await FiltersService.createFilterFilterPost()

        if(filter) {
            goto(`/filter/${filter._id}`)
        }
        return filter
    }
</script>

<svelte:head>
    <title>Votigo</title>
</svelte:head>

<div class="container mx-auto p-4">
    <button on:click={createVote} type="button" class="btn variant-filled">
        <span>Create Vote</span>
        <span><Icon src={Plus} class="w-6 h-6"/></span>
    </button>
    <button on:click={createFilter} type="button" class="btn variant-filled">
        <span>Create Filter</span>
        <span><Icon src={Plus} class="w-6 h-6"/></span>
</div>
