import { index } from "@/lib/createAlgoliaSearchClient";

export async function fetchFiles(value: string, page: number) {
  const response = await index.search(value, { page });
  return response;
}
