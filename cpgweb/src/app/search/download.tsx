import React from "react";
import { Button } from "@/src/components/ui/button";
import { Download, Loader2 } from "lucide-react";
import { QueryClient } from "@tanstack/react-query";
import { fetchFiles } from "./services";

export type TDownloadSearchResultProps = {
  searchValue: string;
};

const queryClient = new QueryClient();

queryClient.fetchQuery({
  queryKey: [""],
  queryFn: () => fetchFiles("", 0, 10),
  retry: 3,
});

export function DownloadProjectFacetResult(props: TDownloadSearchResultProps) {
  const [isDownloading, setIsDownloading] = React.useState(false);
  const { searchValue } = props;

  async function download() {
    setIsDownloading(true);
    const pageSize = 100;
    const pageIndex = 0;

    const { hits, nbPages } = await queryClient.fetchQuery({
      queryKey: [searchValue, pageIndex, pageSize],
      queryFn: () => fetchFiles(searchValue, pageIndex, pageSize),
      retry: 3,
    });


  }

}

export function DownloadSearchResult(props: TDownloadSearchResultProps) {
  const [isDownloading, setIsDownloading] = React.useState(false);
  const { searchValue } = props;

  async function download() {
    setIsDownloading(true);
    const pageSize = 100;
    const pageIndex = 0;

    const { hits, nbPages } = await queryClient.fetchQuery({
      queryKey: [searchValue, pageIndex, pageSize],
      queryFn: () => fetchFiles(searchValue, pageIndex, pageSize),
      retry: 3,
    });

    try {
      const promises = [];
      if (nbPages > 1) {
        for (let i = 1; i < nbPages; i++) {
          promises.push(
            queryClient.fetchQuery({
              queryKey: [searchValue, i, pageSize],
              queryFn: () => fetchFiles(searchValue, i, pageSize),
              retry: 3,
            })
          );
        }

        const results = await Promise.all(promises);
        for (const result of results) {
          hits.push(...result.hits);
        }
      }
    } catch (error) {
      console.error("Error while downloading search results", error);
    }

    const dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(hits, null, 2));
    const downloadAnchorNode = document.createElement("a");
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", `${searchValue}_search.json`);
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();

    setIsDownloading(false);
  }

  if (isDownloading) {
    return (
      <Button disabled>
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        Please wait
      </Button>
    );
  }

  return (
    <Button onClick={download}>
      <Download className="mr-2 h-4 w-4" /> Download
    </Button>
  );
}
