"use client";

import * as React from "react";
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";

import { Accordion } from "@/components/ui/accordion";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/src/components/ui/table";
import Search from "@/src/components/ui/search/search";
import { useQuery } from "@tanstack/react-query";
import { fetchFacetValues } from "./services";
import { facetColumns } from "./columns";
import { DataTableViewOptions } from "./view";
import FacetTableRow from "./facet-table-row";
import { DownloadFacet } from "./download-facet";

export default function DataTable() {
  const [search, setSearch] = React.useState("");
  const [rowSelection, setRowSelection] = React.useState({});
  const [pagination, setPagination] = React.useState({
    pageIndex: 0, //initial page index
    pageSize: 10, //default page size
  });

  const onSearch = React.useCallback((value: string) => {
    setSearch(value);
    setPagination((prev) => ({
      ...prev,
      pageIndex: 0,
    }));
  }, []);

  const { data, isFetching } = useQuery({
    queryKey: [search, pagination.pageIndex, pagination.pageSize],
    queryFn: () =>
      fetchFacetValues(search, pagination.pageIndex, pagination.pageSize),
  });

  const facets = React.useMemo(() => {
    if (!data || !data.facets) return [];
    const d = data?.facets?.project_id;
    const facets = Object.keys(data?.facets?.project_id).map((project) => ({
      value: project,
      count: d[project],
    }));

    return facets;
  }, [data]);

  const table = useReactTable({
    data: facets,
    columns: facetColumns as any,
    getCoreRowModel: getCoreRowModel(),
    enableRowSelection: true,
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onPaginationChange: setPagination,
    rowCount: facets.length || 0,
    state: {
      pagination,
    },
    manualPagination: true,
  });

  return (
    <div className="w-full p-4">
      <div>
        <p className="text-sm text-muted-foreground py-2">
          Search for genes, compounds and other metadata across the Cell Painting
          Gallery. Searches through all metadata files in the Gallery and returns
          the metadata files that contain the search term. See Cell Painting Gallery
          documentation for information on file organization and download.
        </p>
      </div>
      <div className="flex flex-wrap items-center justify-between py-4">
        <Search value={search} onSearch={onSearch} />
        <div className="py-2">
          <DataTableViewOptions table={table} />
          <DownloadFacet searchValue={search} />
        </div>
      </div>
      <div className="rounded-md border">
        <Accordion type="multiple">
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    return (
                      <TableHead key={header.id}>
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                      </TableHead>
                    );
                  })}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows?.length ? (
                table
                  .getRowModel()
                  .rows.map((row) => <FacetTableRow key={row.id} row={row} search={search} />)
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={facetColumns.length}
                    className="h-24 text-center"
                  >
                    {isFetching ? "Loading..." : "No results"}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Accordion>
      </div>
    </div>
  );
}
