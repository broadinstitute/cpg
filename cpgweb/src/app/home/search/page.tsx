"use client";

import React from "react";
import Search from "../../../../components/ui/search/search";
import { fetchFiles } from "./services";
import ResultList from "../../../../components/ui/search/result-list";
import { useQuery } from "@tanstack/react-query";
import Pagination from "@/components/ui/search/pagination";

export default function SearchPage() {
  const [searchVal, setSearchVal] = React.useState("");
  const [searchPage, setSearchPage] = React.useState(0);

  const { data, isFetching } = useQuery({
    queryKey: [searchVal, searchPage],
    queryFn: () => fetchFiles(searchVal, searchPage),
  });

  console.log(data);

  const onSearch = React.useCallback((value: string) => {
    // Fetch results from the server
    setSearchVal(value);
  }, []);

  return (
    <div className="p-4">
      <Search value={""} onSearch={onSearch} />
      {!isFetching && data && data.hits.length > 0 && (
        <ResultList results={data?.hits} />
      )}
      {!isFetching && data?.hits.length === 0 && (
        <div className="mt-4">No results found.</div>
      )}
      {isFetching && <div className="mt-4">Loading...</div>}
      {data && data.nbPages > 0 && (
        <Pagination
          onChange={(p) => setSearchPage(p)}
          totalPages={data.nbPages}
        />
      )}
    </div>
  );
}
