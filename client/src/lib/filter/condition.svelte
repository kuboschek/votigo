<script lang="ts">
	import type { AndCondition_Input, EqCondition, OrCondition_Input } from '$lib';
	import { getModalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import { createEventDispatcher } from 'svelte';
	import { Icon, Plus } from 'svelte-hero-icons';
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

        sendSubtreeUpdate()
	}

    function sendSubtreeUpdate() {
        dispatch('subtreeUpdate', { subtree: conditionTree });
    }

    function handleSubtreeUpdate(event: CustomEvent<{ subtree: any }>, partIndex: number) {
        conditionTree.parts[partIndex] = event.detail.subtree;

        sendSubtreeUpdate()
    }

	function chooseConditionType() {
		const typeModal: ModalSettings = {
			title: 'Add Criterium',
			body: 'Which type of condition do you want to add?',
			type: 'component',
			component: 'addFilterCondition',
			response(r) {
				switch (r) {
					case 'AND':
						conditionTree.parts = [
                            ...conditionTree.parts,
                            { type: 'AND', parts: [] }
                        ]
						break;
                    case 'OR':
                        conditionTree.parts = [
                            ...conditionTree.parts,
                            { type: 'OR', parts: [] }
                        ]
                        break;
                    case 'EQ':
                        conditionTree.parts = [
                            ...conditionTree.parts,
                            { type: 'EQ', pointer: '', target_value: '' }
                        ]
                        break;
				}
                sendSubtreeUpdate();
			}
		};

		modal.trigger(typeModal);
	}
</script>

<!-- Base Case, for now only the equals check-->
{#if conditionTree.type === 'EQ'}
	<div class="h4 flex items-center gap-2">
		<select class="select inline font-mono focus-within:grow" bind:value={conditionTree.pointer} on:change={sendSubtreeUpdate}>
			{#each Object.entries(fields) as [pointer, label]}
				<option value={pointer}>{label}</option>
			{/each}
			{#if !fields[conditionTree.pointer]}
				<option value={conditionTree.pointer}>{conditionTree.pointer}</option>
			{/if}
		</select>
		is
		<input
			class="input inline font-mono"
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
				<svelte:self conditionTree={conditionPart} on:subtreeUpdate={(event) => handleSubtreeUpdate(event, i)} />
				<h4 class="h4 text-surface-500 self-center">
					{conditionTree.type === 'AND' ? 'and' : 'or'}
				</h4>
			{/each}
			<button class="btn variant-filled" on:click={chooseConditionType}>
				<span> <Icon src={Plus} class="h-4 w-4" /></span>
				<span>Add Criterium</span>
			</button>
		{/if}
	</div>
{/if}
