import { index } from "@/src/lib/createAlgoliaSearchClient";

export async function fetchFiles(
  value: string,
  page: number,
  pageSize: number
) {
  const response = await index.search(value, { page, hitsPerPage: pageSize });
  return response;
}
