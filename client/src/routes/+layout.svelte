<script lang="ts">
	import AddConditionModal from '$lib/filter/add-condition-modal.svelte';
	import '../app.pcss';
	import { AppShell, AppBar, initializeStores, Toast, Modal, type ModalComponent } from '@skeletonlabs/skeleton';

	initializeStores();

	const modalRegistry: Record<string, ModalComponent> = {
		addFilterCondition: { ref: AddConditionModal}
	}
</script>

<Toast />
<Modal components={modalRegistry} />

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
