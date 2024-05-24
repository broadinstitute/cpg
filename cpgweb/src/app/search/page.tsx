"use client";

import * as React from "react";
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  VisibilityState,
} from "@tanstack/react-table";

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
import { fetchFiles } from "./services";
import { columns } from "./columns";
import { DataTablePagination } from "./pagination";
import { DownloadSearchResult } from "./download";
import { DataTableViewOptions } from "./view";

export default function DataTable() {
  const [search, setSearch] = React.useState("");
  const [rowSelection, setRowSelection] = React.useState({});
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({
      Gene: false,
      Plate_Map_Name: false,
      Col: false,
      Row: false,
      PlateName: false,
      Name: false,
      PublicID: false,
      _highlightResult: false,
    });
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
      fetchFiles(search, pagination.pageIndex, pagination.pageSize),
  });

  const table = useReactTable({
    data: data?.hits || [],
    columns: columns as any,
    getCoreRowModel: getCoreRowModel(),
    onRowSelectionChange: setRowSelection,
    enableRowSelection: true,
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    rowCount: (data?.nbPages || 0) * (data?.hitsPerPage || 0),
    state: {
      pagination,
      rowSelection,
      columnVisibility,
    },
    manualPagination: true,
  });

  return (
    <div className="w-full p-4">
      <div>
        <p className="text-sm text-muted-foreground py-2">
          Search for genes, compounds and other metadata across the CellPainting Gallery.
        </p>
      </div>
      <div className="flex flex-wrap items-center justify-between py-4">
        <Search value={search} onSearch={onSearch} />
        <div className="py-2">
          <DataTableViewOptions table={table} />
          <DownloadSearchResult searchValue={search} />
        </div>
      </div>
      <div className="rounded-md border">
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
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  {isFetching ? "Loading..." : "No results"}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      {!isFetching && <DataTablePagination table={table} />}
    </div>
  );
}
