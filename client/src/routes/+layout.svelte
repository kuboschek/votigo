<script>
	import '../app.pcss';
	import { AppShell, AppBar, initializeStores, Toast } from '@skeletonlabs/skeleton';

	initializeStores();
</script>

<Toast />

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<a href="/"><h1 class="h1">Votigo</h1></a>
			<svelte:fragment slot="trail">
				
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
</AppShell>
