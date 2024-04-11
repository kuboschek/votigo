<script lang="ts">
	import type { IconSource } from '@steeze-ui/heroicons';
	import { Icon } from 'svelte-hero-icons';

	export let iconSrc: IconSource;
	export let hoverColorClass: string = '';

	$: iconClass = `group-hover:${hoverColorClass} h-6 w-6` ?? 'h-6 w-6';
</script>

<button on:click type="button" class="group">
	<span><slot /></span>
	<span><Icon src={iconSrc} class={iconClass} /></span>
</button>
