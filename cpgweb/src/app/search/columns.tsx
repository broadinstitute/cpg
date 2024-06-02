"use client";

import { ColumnDef } from "@tanstack/react-table";
import { TFacets, THit } from "./types";
import { AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "../../components/ui/button";
import { Download, Eye, Loader2 } from "lucide-react";
import { get_key_file } from "../../lib/cpg_ops";
import React from "react";

// export const columns: ColumnDef<THit>[] = [
//   {
//     accessorKey: "objectID",
//     header: "Object ID",
//     cell: ({ row }) => <div>{row.getValue("objectID")}</div>,
//   },
//   {
//     accessorKey: "project_id",
//     header: "Project ID",
//     cell: ({ row }) => <div>{row.getValue("project_id")}</div>,
//   },
//   {
//     accessorKey: "Col",
//     header: "Col",
//     cell: ({ row }) => <div>{row.getValue("Col")}</div>,
//   },
//   {
//     accessorKey: "Assay_Plate_Barcode",
//     header: "Assay Plate Barcode",
//     cell: ({ row }) => <div>{row.getValue("Assay_Plate_Barcode")}</div>,
//   },
//   {
//     accessorKey: "Name",
//     header: "Name",
//     cell: ({ row }) => <div>{row.getValue("Name")}</div>,
//   },
//   {
//     accessorKey: "PlateName",
//     header: "PlateName",
//     cell: ({ row }) => <div>{row.getValue("PlateName")}</div>,
//   },
//   {
//     accessorKey: "Plate_Map_Name",
//     header: "Plate Map Name",
//     cell: ({ row }) => <div>{row.getValue("Plate_Map_Name")}</div>,
//   },
//   {
//     accessorKey: "PublicID",
//     header: "Public ID",
//     cell: ({ row }) => <div>{row.getValue("PublicID")}</div>,
//   },
//   {
//     accessorKey: "Row",
//     header: "Row",
//     cell: ({ row }) => <div>{row.getValue("Row")}</div>,
//   },
//   {
//     accessorKey: "key",
//     header: "Key",
//     cell: ({ row }) => <div>{row.getValue("key")}</div>,
//   },
//   {
//     accessorKey: "_highlightResult",
//     header: "Hightlight Result",
//     cell: ({ row }) => {
//       const value: any = row.getValue("_highlightResult");

//       const keys = Object.keys(value).filter(
//         (key) => key !== "objectID" && key !== "project_id"
//       );

//       return (
//         <div>
//           {keys.map((key) => {
//             return (
//               <div key={key} className="flex">
//                 <div className="text-red-400 w-36">{key}</div>
//                 <div>{value[key].value}</div>
//               </div>
//             );
//           })}
//         </div>
//       );
//     },
//   },
// ];

export const columns: ColumnDef<THit>[] = [
  {
    accessorKey: "value",
    header: "Key",
    cell: ({ row }) => <div>{row.getValue("value")}</div>,
  },
  {
    accessorKey: "count",
    header: "Count",
    cell: ({ row }) => <div>{row.getValue("count")}</div>,
  },
  {
    accessorKey: "",
    header: "Actions",
    cell: ({ row }) => <ProjectKeyActions filename={row.getValue("value")} />,
  },
];

type TProjectKeyActions = {
  filename: string;
};

function ProjectKeyActions(props: TProjectKeyActions) {
  const { filename } = props;
  const [isDownloadLoading, setIsDownloadLoading] = React.useState(false);

  function downloadData(data: Uint8Array) {
    let type = "application/";

    if (filename.endsWith(".txt")) {
      type += "txt";
    } else if (filename.endsWith(".xlsx")) {
      type += "xlsx";
    } else if (filename.endsWith(".csv")) {
      type += "csv";
    } else if (filename.endsWith(".tsv")) {
      type += "tsv";
    } else if (filename.endsWith(".png")) {
      type = "image/png";
    }

    const blob = new Blob([data], { type });
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    setIsDownloadLoading(false);
  }

  async function fetchData() {
    const data = await get_key_file(filename);
    return data || "";
  }

  return (
    <div>
      <Button variant="ghost">
        <Eye className="mr-2 h-4 w-4" /> View
      </Button>
      <Button
        variant="ghost"
        disabled={isDownloadLoading}
        onClick={async () => {
          setIsDownloadLoading(true);
          const data = await fetchData();
          if (!data) {
            setIsDownloadLoading(false);
            return;
          }
          downloadData(data);
        }}
      >
        {isDownloadLoading && (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Downloading...
          </>
        )}
        {!isDownloadLoading && (
          <>
            <Download className="mr-2 h-4 w-4" /> Download
          </>
        )}
      </Button>
    </div>
  );
}

export const facetColumns: ColumnDef<TFacets>[] = [
  {
    accessorKey: "value",
    header: "Project ID",
    cell: ({ row }) => <div>{row.getValue("value")}</div>,
  },
  {
    accessorKey: "count",
    header: "Hits",
    cell: ({ row }) => <div>{row.getValue("count")}</div>,
  },
  {
    header: "View",
    cell: ({ row }) => {
      return (
        <AccordionItem className="border-0 hover:no-underline" value={row.id}>
          <AccordionTrigger className="p-0 no-underline hover:no-underline"></AccordionTrigger>
        </AccordionItem>
      );
    },
  },
];
