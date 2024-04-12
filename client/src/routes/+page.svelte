<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;
</script>

<svelte:head>
	<title>Votigo</title>
</svelte:head>

<div class="container mx-auto p-4">
	{#each data.votes as vote}
		<div class="card p-4">
			<h1 class="text-2xl font-bold">{vote.title}</h1>
		</div>
	{/each}
</div>

<pre>
	{JSON.stringify(data, null, 2)}
</pre>
