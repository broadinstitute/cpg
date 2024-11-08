import { index } from "@/src/lib/createAlgoliaSearchClient";

export async function fetchFacetValues(
  value: string,
  page: number,
  pageSize: number
) {
  // const response = await index.searchForFacetValues("project_id", value, {
  //   page,
  //   hitsPerPage: pageSize,
  // });

  const response = await index.search(value, {
    page,
    hitsPerPage: pageSize,
    facets: ["project_id"],
    distinct: true,
  });

  return response;
}

export async function fetchProjectFiles(
  value: string,
  projectId: string,
  page: number,
  pageSize: number
) {
  const response = await index.search(value, {
    page,
    hitsPerPage: pageSize,
    facets: ["key"],
    facetFilters: [`project_id:${projectId}`],
    distinct: true,
  });

  return response;
}
