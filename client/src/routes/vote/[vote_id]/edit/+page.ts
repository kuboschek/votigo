import { error } from '@sveltejs/kit';
import { ApiError, VotesService } from '$lib';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params: { vote_id } }) => {
    try {
        return await VotesService.readVoteVoteVoteIdGet(vote_id);
    } catch (e) {
        const apiError = e as ApiError;
        error(apiError.status, apiError.statusText)
    }
}