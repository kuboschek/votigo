import { ApiError, VotesService } from '$lib';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
	try {
		return {
			votes: await VotesService.listVotesVoteGet()
		};
	} catch (e) {
		const apiError = e as ApiError;
		error(apiError.status, apiError.statusText);
	}
};
