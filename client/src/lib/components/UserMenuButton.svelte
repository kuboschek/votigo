<script lang="ts">
	import type { IconSource } from '@steeze-ui/heroicons';
	import { Icon } from 'svelte-hero-icons';

	export let iconSrc: IconSource;
	export let hoverColorClass: string = '';
</script>

<button on:click type="button" class="group">
	<span><slot /></span>
	<span><Icon src={iconSrc} class={'group-hover:' + hoverColorClass + ' h-6 w-6'} /></span>
</button>
