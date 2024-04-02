<script lang="ts">
	import type { AndCondition_Input, EqCondition, OrCondition_Input } from '$lib';
	import { getModalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import { createEventDispatcher } from 'svelte';
	import { Icon, Plus, Trash } from 'svelte-hero-icons';
	import { fields } from './fields';

	export let conditionTree: AndCondition_Input | OrCondition_Input | EqCondition;

	$: targetValue =
		typeof conditionTree.target_value === 'number'
			? conditionTree.target_value
			: `"${conditionTree.target_value}"`;
	$: resolvedPointer = fields[conditionTree.pointer] || conditionTree.pointer;

	const modal = getModalStore();
	const dispatch = createEventDispatcher();

	function maybeCastToNumber() {
		if (!conditionTree.target_value) return;
		if (!conditionTree.type === 'EQ') return;

		if (!isNaN(Number(conditionTree.target_value))) {
			conditionTree.target_value = Number(conditionTree.target_value);
		}

		sendSubtreeUpdate();
	}

	function sendSubtreeUpdate() {
		dispatch('subtreeUpdate', { subtree: conditionTree });
	}

	function handleSubtreeUpdate(event: CustomEvent<{ subtree: any }>, partIndex: number) {
		conditionTree.parts[partIndex] = event.detail.subtree;

		sendSubtreeUpdate();
	}

	function removePart(partIndex: number) {
		conditionTree.parts.splice(partIndex, 1);
		sendSubtreeUpdate();
	}

	function chooseConditionType() {
		const typeModal: ModalSettings = {
			title: 'Add Condition',
			body: 'Which type of condition would you like to add?',
			type: 'component',
			component: 'addFilterCondition',
			response(r) {
				switch (r) {
					case 'AND':
						conditionTree.parts = [...conditionTree.parts, { type: 'AND', parts: [] }];
						break;
					case 'OR':
						conditionTree.parts = [...conditionTree.parts, { type: 'OR', parts: [] }];
						break;
					case 'EQ':
						conditionTree.parts = [
							...conditionTree.parts,
							{ type: 'EQ', pointer: '', target_value: '' }
						];
						break;
				}

				// Only send the update if the user actually added a condition
				// Modal will respond with undefined if the user clicks outside of it
				if (r) {
					sendSubtreeUpdate();
				}
			}
		};

		modal.trigger(typeModal);
	}
</script>

<!-- Base Case, for now only the equals check-->
{#if conditionTree.type === 'EQ'}
	<div class="h4 flex items-center gap-2">
		<select
			class="select inline font-mono"
			bind:value={conditionTree.pointer}
			on:change={sendSubtreeUpdate}
		>
			{#each Object.entries(fields) as [pointer, label]}
				<option value={pointer}>{label}</option>
			{/each}
			{#if !fields[conditionTree.pointer]}
				<option value={conditionTree.pointer}>{conditionTree.pointer}</option>
			{/if}
		</select>
		<span>is</span>
		<input
			class="input rounded-md p-2 read-only:cursor-not-allowed"
			type="text"
			bind:value={conditionTree.target_value}
			on:change={maybeCastToNumber}
		/>
	</div>

	<!-- Recursive Case, for the AND and OR conditions -->
{:else}
	<div
		class="card flex flex-col space-y-2 border border-slate-500 p-4 {conditionTree.type !== 'EQ'
			? 'border border-slate-500'
			: ''}"
	>
		{#if conditionTree.parts}
			{#each conditionTree.parts as conditionPart, i}
				<div class="flex items-center space-x-2">
					<div class="grow">
						<svelte:self
							class="grow"
							conditionTree={conditionPart}
							on:subtreeUpdate={(event) => handleSubtreeUpdate(event, i)}
						/>
					</div>
					<button class="btn-icon hover:variant-primary group" on:click={() => removePart(i)}>
						<Icon
							src={Trash}
							class="h-6 w-6 cursor-pointer transition-colors group-hover:text-red-500"
						/>
					</button>
				</div>
				<h4 class="h4 text-surface-500 self-center">
					{conditionTree.type === 'AND' ? 'and' : 'or'}
				</h4>
			{/each}
			<button class="btn variant-filled" on:click={chooseConditionType}>
				<span> <Icon src={Plus} class="h-4 w-4" /></span>
				<span>Add Condition</span>
			</button>
		{/if}
	</div>
{/if}
