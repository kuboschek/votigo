<script lang="ts">
	import { goto } from '$app/navigation';
    import { VotesService, type ReadFullVote } from '$lib'
	import { Icon, Plus } from 'svelte-hero-icons';

    let vote: ReadFullVote

    async function createVote() {
        vote = await VotesService.createVoteVotePost()

        if(vote) {
            goto(`/vote/${vote.vote._id}/edit`)
        }
        return vote
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
</div>
