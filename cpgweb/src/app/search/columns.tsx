"use client";

import { ColumnDef } from "@tanstack/react-table";
import { THit } from "./types";

export const columns: ColumnDef<THit>[] = [
  {
    accessorKey: "objectID",
    header: "Object ID",
    cell: ({ row }) => <div>{row.getValue("objectID")}</div>,
  },
  {
    accessorKey: "project_id",
    header: "Project ID",
    cell: ({ row }) => <div>{row.getValue("project_id")}</div>,
  },
  {
    accessorKey: "Col",
    header: "Col",
    cell: ({ row }) => <div>{row.getValue("Col")}</div>,
  },
  {
    accessorKey: "Assay_Plate_Barcode",
    header: "Assay Plate Barcode",
    cell: ({ row }) => <div>{row.getValue("Assay_Plate_Barcode")}</div>,
  },
  {
    accessorKey: "Name",
    header: "Name",
    cell: ({ row }) => <div>{row.getValue("Name")}</div>,
  },
  {
    accessorKey: "PlateName",
    header: "PlateName",
    cell: ({ row }) => <div>{row.getValue("PlateName")}</div>,
  },
  {
    accessorKey: "Plate_Map_Name",
    header: "Plate Map Name",
    cell: ({ row }) => <div>{row.getValue("Plate_Map_Name")}</div>,
  },
  {
    accessorKey: "PublicID",
    header: "Public ID",
    cell: ({ row }) => <div>{row.getValue("PublicID")}</div>,
  },
  {
    accessorKey: "Row",
    header: "Row",
    cell: ({ row }) => <div>{row.getValue("Row")}</div>,
  },
  {
    accessorKey: "_highlightResult",
    header: "Hightlight Result",
    cell: ({ row }) => {
      const value: any = row.getValue("_highlightResult");

      const keys = Object.keys(value).filter(
        (key) => key !== "objectID" && key !== "project_id"
      );

      return (
        <div>
          {keys.map((key) => {
            return (
              <div key={key} className="flex">
                <div className="text-red-400 w-36">{key}</div>
                <div>{value[key].value}</div>
              </div>
            );
          })}
        </div>
      );
    },
  },
];
