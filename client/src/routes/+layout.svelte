<script>
	import '../app.pcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<a href="/"><h1 class="h1">Votigo</h1></a>
			<svelte:fragment slot="trail">
				
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<div class="container p-4">
		<slot />
	</div>
</AppShell>
