<script lang="ts">
	import { FiltersService, type UpdateFilter } from '$lib';
	import Condition from '$lib/filter/condition.svelte';
	import type { PageData } from './$types';
	export let data: PageData;

	async function updateFilterCondition(event: CustomEvent<{ subtree: any }>) {
		data.condition.tree = event.detail.subtree;
		await updateFilter()
	}

	async function updateFilter() {
		const filter: UpdateFilter = {
			title: data.title || '',
			condition: data.condition || {}
		};

		try {
			await FiltersService.updateFilterFilterFilterIdPost(data._id, filter);
			data = {
				...data,
				...filter
			};
		} catch (error) {
			console.error(error);
		}
	}
</script>

<svelte:head>
	<title>{data.title || 'Votigo'}</title>
</svelte:head>

<div class="container mx-auto flex justify-between p-4">
	<section>
		<h2 class="h2">Edit Filter</h2>
	</section>
</div>

<div class="container mx-auto space-y-10 p-4 lg:grid lg:grid-cols-2 lg:gap-4 lg:space-y-0">
	<section class="space-y-2">
		<label for="filter_title" class="h3">Title</label>
		<input
			id="filter_title"
			class="h4 w-full rounded-md p-2 read-only:cursor-not-allowed"
			bind:value={data.title}
			on:change={updateFilter}
			placeholder="Approved Members Only"
			type="text"
		/>
	</section>
	<section class="space-y-2">
		<h3 class="h3">Criteria</h3>
		<div class="mx-auto">
			<Condition conditionTree={data.condition.tree} on:subtreeUpdate={updateFilterCondition}/>
		</div>
	</section>
</div>

<div class="container mx-auto flex justify-between p-4">
	<section>
		<pre>{JSON.stringify(data, null, 2)}</pre>
	</section>
</div>
