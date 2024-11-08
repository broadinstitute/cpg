import { flexRender, Row } from "@tanstack/react-table";

import { TableCell, TableRow } from "@/src/components/ui/table";
import { AccordionContent, AccordionItem } from "@/components/ui/accordion";
import ProjectTable from "./project-table";
import { facetColumns } from "./columns";

export type TFaceTableRowProps = {
  row: Row<unknown>;
  search: string;
};

export default function FacetTableRow(props: TFaceTableRowProps) {
  const { row, search } = props;

  return (
    <>
      <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
        {row.getVisibleCells().map((cell) => (
          <TableCell key={cell.id}>
            {flexRender(cell.column.columnDef.cell, cell.getContext())}
          </TableCell>
        ))}
      </TableRow>
      <TableRow>
        <TableCell colSpan={facetColumns.length} className="border-none p-0">
          <AccordionItem value={row.id} className="border-0 no-underline">
            <AccordionContent>
              <ProjectTable projectId={row.getValue("value")} value={search} />
            </AccordionContent>
          </AccordionItem>
        </TableCell>
      </TableRow>
    </>
  );
}
