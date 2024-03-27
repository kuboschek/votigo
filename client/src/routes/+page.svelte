<script lang="ts">
    import { VotesService, type ReadFullVote } from '$lib'

    let vote: ReadFullVote

    async function createVote() {
        vote = await VotesService.createVoteVotePost()
        return vote
    }
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<pre>{vote?.vote?._id}</pre>
<button on:click={createVote} type="button" class="btn-icon variant-filled">Create Vote</button>