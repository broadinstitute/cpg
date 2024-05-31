import { index } from "@/src/lib/createAlgoliaSearchClient";

export async function fetchFiles(
  value: string,
  page: number,
  pageSize: number
) {
  const projectFacet = await index.searchForFacetValues('project_id', value);
  console.log(projectFacet);
  const response = await index.search(value, { page, hitsPerPage: pageSize });
  return response;
}
