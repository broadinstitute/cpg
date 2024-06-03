import { useQuery } from "@tanstack/react-query";
import { fetchProjectFiles } from "./services";
import React from "react";
import { columns } from "./columns";
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
import { DataTableViewOptions } from "./view";
import { DownloadSearchResult } from "./download";
import Search from "@/src/components/ui/search/search";
import { DataTablePagination } from "./pagination";

export type TProjectTableProps = {
  projectId: string;
  value?: string;
};

export default function ProjectTable(props: TProjectTableProps) {
  const { projectId, value } = props;
  const [search, setSearch] = React.useState(value != null ? value : "");
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
    queryKey: [search, projectId, pagination.pageIndex, pagination.pageSize],
    queryFn: () =>
      fetchProjectFiles(
        search,
        projectId,
        pagination.pageIndex,
        pagination.pageSize
      ),
  });

  const facets = React.useMemo(() => {
    if (!data || !data.facets) return [];
    return Object.keys(data?.facets?.key).map((key) => ({
      value: key,
    }));
  }, [data]);

  const table = useReactTable({
    data: facets,
    columns: columns as any,
    getCoreRowModel: getCoreRowModel(),
    enableRowSelection: true,
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    rowCount: facets.length || 0,
    state: {
      pagination,
      columnVisibility,
    },
    manualPagination: true,
  });

  return (
    <div className="w-full p-4">
      <div className="flex flex-wrap items-center justify-between py-4">
        <Search value={search} onSearch={onSearch} />
        <div className="py-2">
          <DataTableViewOptions table={table} />
          <DownloadSearchResult projectId={projectId} searchValue={search} />
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
