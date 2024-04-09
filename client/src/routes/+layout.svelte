<script lang="ts">
	import AuthContext from '$lib/components/AuthContext.svelte';
	import UserMenu from '$lib/components/UserMenu.svelte';
	import AddConditionModal from '$lib/filter/add-condition-modal.svelte';
	import {
		AppBar,
		AppShell,
		Modal,
		Toast,
		initializeStores,
		type ModalComponent
	} from '@skeletonlabs/skeleton';
	import '../app.pcss';

	initializeStores();

	const modalRegistry: Record<string, ModalComponent> = {
		addFilterCondition: { ref: AddConditionModal }
	};
</script>

<Toast />
<Modal components={modalRegistry} />

<AuthContext>
	<AppShell>
		<svelte:fragment slot="header">
			<AppBar>
				<svelte:fragment slot="lead">
					<a href="/"><h1 class="h1">Votigo</h1></a>
				</svelte:fragment>
				<svelte:fragment slot="trail">
					<UserMenu />
				</svelte:fragment>
			</AppBar>
		</svelte:fragment>
		<slot />
	</AppShell>
</AuthContext>
