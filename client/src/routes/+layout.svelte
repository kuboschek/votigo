<script>
	import '../app.pcss';
	import { AppShell, AppBar, initializeStores, Toast, Modal } from '@skeletonlabs/skeleton';

	initializeStores();
</script>

<Toast />
<Modal />

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
