<script lang="ts">
	import { getModalStore } from '@skeletonlabs/skeleton';
	import type { SvelteComponent } from 'svelte';
	const modalStore = getModalStore();

	// Props
	/** Exposes parent props to this component. */
	export let parent: SvelteComponent;

	function onClick(conditionType: string) {
		if ($modalStore[0].response) {
			$modalStore[0].response(conditionType);
		}
		modalStore.close();
	}

	// Base Classes
	const cBase = 'card p-4 w-modal shadow-xl space-y-4';
	const cHeader = 'text-2xl font-bold';
</script>

{#if $modalStore[0]}
	<div class={cBase}>
		<header class={cHeader}>{$modalStore[0].title ?? '(title missing)'}</header>
		<article>{$modalStore[0].body ?? '(body missing)'}</article>

		<footer class="modal-footer {parent.regionFooter} grow">
			<button class="btn {parent.buttonPositive}" on:click={() => onClick('AND')}>and</button>
			<button class="btn {parent.buttonPositive}" on:click={() => onClick('OR')}>or</button>
			<button class="btn {parent.buttonPositive}" on:click={() => onClick('EQ')}>equals</button>
		</footer>
	</div>
{/if}
