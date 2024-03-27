<script lang="ts">
	import type { PageData } from "./$types";

    export let data: PageData;
</script>
<h1>{data.vote._modified_on}</h1>