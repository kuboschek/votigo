<script lang="ts">
	import type { AndCondition_Input, EqCondition, OrCondition_Input } from '$lib';

	export let conditionTree: AndCondition_Input | OrCondition_Input | EqCondition;
	export let level = 0;
	export let prefix = '';

    $: targetValue = typeof conditionTree.target_value === 'number' ? conditionTree.target_value : `"${conditionTree.target_value}"`;
</script>

{#if conditionTree.type === 'EQ'}
	<h4 class="h4">
		<pre class="inline">{conditionTree.pointer}</pre>
		is
        <pre class="inline">{targetValue}</pre>
	</h4>
{:else}
	<div
		class="card space-y-2 border border-slate-500 p-4 {conditionTree.type !== 'EQ'
			? 'border border-slate-500'
			: ''}"
	>
        {#if conditionTree.parts}
            {#each conditionTree.parts as conditionPart, i}
                <svelte:self
                    conditionTree={conditionPart}
                    level={level + 1}
                    prefix={prefix + (i + 1) + '.'}
                />
                {#if i < conditionTree.parts.length - 1}
                <h4 class="h4 self-center text-green-500">
                    {conditionTree.type === 'AND' ? 'and' : 'or'}
                </h4>
                {/if}
                <!--<pre>{JSON.stringify(conditionPart, null, 2)}</pre>-->
            {/each}
        {/if}
	</div>
{/if}
