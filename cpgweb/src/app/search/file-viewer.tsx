import { Button } from "@/src/components/ui/button";
import {
  DataSheetGrid,
  textColumn,
  keyColumn,
} from 'react-datasheet-grid';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/src/components/ui/dialog";
import { DSVRowArray, csvParse, tsvParse } from "d3-dsv";
import { get_key_file } from "@/src/lib/cpg_ops";
import { Eye, Loader2 } from "lucide-react";
import React from "react";
import Image from "next/image";

interface DSVRendererProps {
  data: DSVRowArray
}
const DSVRenderer = (props: DSVRendererProps) => {
  const { data } = props;
  // const [data, setData] = React.useState([
  //   { active: true, firstName: 'Elon', lastName: 'Musk' },
  //   { active: false, firstName: 'Jeff', lastName: 'Bezos' },
  // ])
  const columns = data.columns.map((col) => { return { ...keyColumn(col, textColumn), title: col, disabled: true } })
  return (
    <DataSheetGrid
      value={data}
      columns={columns}
      addRowsComponent={false}
    />
  )

}

interface FileViewerProps {
  fileName: string;
}

export function FileViewer(props: FileViewerProps) {
  const { fileName } = props;
  const [viewContent, setViewContent] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(true);

  async function fetchData() {
    if (fileName.endsWith(".xslx")) {
      setViewContent("Please download to view this file.")
      setIsLoading(false);
      return;
    }
    const encoding = fileName.endsWith(".png") ? "base64" : "utf-8";
    const data = await get_key_file(fileName, { toString: { encoding } });

    if (data && typeof data === "string") {
      if (fileName.endsWith(".png")) {
        setViewContent(`data:image/png;base64,${data}`);
      } else {
        // Only showing the first 100 characters
        setViewContent(data);
      }
    } else {
      console.log("Failed to load file.", data);
    }

    setIsLoading(false);
  }

  const loading = isLoading;
  const failedToLoad = !isLoading && !viewContent;
  const loaded = !isLoading && viewContent;
  const isImage = fileName.endsWith(".png");
  const isCSV = fileName.endsWith(".csv");
  const isTSV = fileName.endsWith(".tsv");

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" onClick={fetchData}>
          <Eye className="mr-2 h-4 w-4" /> View
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{fileName.split("/").pop()}</DialogTitle>
        </DialogHeader>
        {loading && (
          <div className="p-4 flex justify-center items-center">
            <Loader2 className="mr-2 h-6 w-6 animate-spin" />
          </div>
        )}

        {failedToLoad && <div>Failed to load.</div>}
        {loaded && isCSV && <div> <DSVRenderer data={csvParse(viewContent)} /></div>}
        {loaded && isTSV && <div> <DSVRenderer data={tsvParse(viewContent)} /></div>}
        {loaded && isImage && (
          <div className="flex justify-center">
            <Image
              objectFit="contain"
              objectPosition="center"
              // className="w-full"
              height={1600}
              width={1600}
              src={viewContent}
              alt={fileName}
            />
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
