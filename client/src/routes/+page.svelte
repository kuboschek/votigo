<script lang="ts">
	import { goto } from '$app/navigation';
    import { VotesService, type ReadFullVote } from '$lib'

    let vote: ReadFullVote

    async function createVote() {
        vote = await VotesService.createVoteVotePost()

        if(vote) {
            goto(`/vote/${vote.vote._id}`)
        }
        return vote
    }
</script>

<svelte:head>
    <title>Votigo</title>
</svelte:head>

<button on:click={createVote} type="button" class="btn-icon variant-filled">Create Vote</button>