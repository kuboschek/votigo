<script lang="ts">
	import { dev } from "$app/environment";
	import { invalidateAll } from "$app/navigation";
	import { VotesService, type UpdateVote, type Vote, type UpdateOption, OptionsService } from "$lib";
    import type { PageData } from "./$types";

    export let data: PageData;

    let newOptionTitle: string;
    let optionInput: HTMLInputElement;

    async function updateVote(event: Event & { currentTarget: HTMLInputElement }) {
        if(data.vote.title === undefined) return;

        const vote: UpdateVote = {
            title: event.currentTarget?.value
        }; 

        try {
            await VotesService.updateVoteVoteVoteIdPost(data.vote._id, vote);
            data.vote = {
                ...data.vote,
                ...vote
            }
        } catch (error) {
            invalidateAll()
            console.error(error)
        } 
    }

    async function createOption() {
        if(newOptionTitle === undefined || newOptionTitle === "") return;

        const newOption = {
            title: newOptionTitle,
            ordering: Math.max(...data.options.map(option => option.ordering || 0), 0) + 1
        }

        try {
            const response = await OptionsService.addOptionVoteVoteIdOptionPost(data.vote._id, newOption);
            data.options = [
                ...data.options,
                response
            ];
            data.vote.option_ids.push(response._id)

        } catch (error) {
            invalidateAll()
            console.error(error)
        } finally {
            newOptionTitle = ""
            optionInput.focus()
        }
    }

    async function sendOptionChange(optionId: string) {
        const option = data.options.find(option => option._id === optionId);

        if(option === undefined) return;

        // Empty options -> removal
        if(option.title === undefined || option.title === "") {
            try {
                await OptionsService.removeOptionVoteVoteIdOptionOptionIdDelete(data.vote._id, optionId);
                data.options = data.options.filter(option => option._id !== optionId);
                data.vote.option_ids = data.vote.option_ids.filter(id => id !== optionId);
            } catch (error) {
                invalidateAll()
                console.error(error)
            }
            return;
        }

        try {
            await OptionsService.updateOptionOptionOptionIdPut(optionId, {
                title: option.title,
                ordering: option.ordering || 0
            });

            // Update the option in the data
            const index = data.options.findIndex(option => option._id === optionId);
            data.options[index] = {
                ...data.options[index],
                ...option
            }
        } catch (error) {
            invalidateAll()
            console.error(error)
        }
    }
</script>

<svelte:head>
    <title>{data.vote.title || "Votigo"}</title>
</svelte:head>

<div class="container">
    <div class="my-2">
        <input readonly={!data.vote.editable} class="h2 p-2" bind:value={data.vote.title} on:change={updateVote} placeholder="<title>" type="text">
    </div>
    <div>
        <h3 class="h3">Options</h3>
    </div>
    <div class="grid grid-cols-3">
        {#each data.options as option}
        <div>
            <input readonly={!data.vote.editable} class="flex-auto p-2 rounded-full" placeholder="<remove option>" bind:value={option.title} on:change={() => sendOptionChange(option._id)}>
        </div>
        {/each}
        <div>
            <input readonly={!data.vote.editable} class="flex-auto p-2 rounded-full" placeholder="<add option>" bind:this={optionInput} bind:value={newOptionTitle} on:change={(event) => createOption()}>
        </div>
    </div>
</div>

<div class="text-sm">
    {#if dev}
    <pre>{JSON.stringify(data, null, 2)}</pre>
    {/if}
</div>
