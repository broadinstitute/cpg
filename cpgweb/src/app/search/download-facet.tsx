import React from "react";
import { Button } from "@/src/components/ui/button";
import { Download, Loader2 } from "lucide-react";
import { QueryClient } from "@tanstack/react-query";
import { fetchFacetValues } from "./services";

export type TDownloadSearchResultProps = {
  searchValue: string;
};

const queryClient = new QueryClient();

export function DownloadFacet(props: TDownloadSearchResultProps) {
  const [isDownloading, setIsDownloading] = React.useState(false);
  const { searchValue } = props;

  async function download() {
    setIsDownloading(true);
    const pageSize = 100;
    const pageIndex = 0;

    const { facets } = await queryClient.fetchQuery({
      queryKey: [searchValue, pageIndex, pageSize],
      queryFn: () => fetchFacetValues(searchValue, pageIndex, pageSize),
      retry: 3,
    });

    const dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(facets, null, 2));
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
