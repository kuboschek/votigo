import { ApiError, FiltersService } from "$lib";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";



export const load: PageLoad = async ({ params: { filter_id } }) => {
    try {
        let filter = await FiltersService.readFilterFilterFilterIdGet(filter_id);

        if(!filter.condition.tree) {
            filter.condition = {
                tree: {
                    type: "AND",
                    parts: []
                }
            }
        }

        return filter
    } catch (e) {
        const apiError = e as ApiError;
        error(apiError.status, apiError.statusText)
    }
}