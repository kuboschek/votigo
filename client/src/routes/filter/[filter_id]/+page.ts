import { ApiError, FiltersService } from "$lib";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";



export const load: PageLoad = async ({ params: { filter_id } }) => {
    try {
        return await FiltersService.readFilterFilterFilterIdGet(filter_id);
    } catch (e) {
        const apiError = e as ApiError;
        error(apiError.status, apiError.statusText)
    }
}