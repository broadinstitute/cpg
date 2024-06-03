import { Button } from "@/src/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/src/components/ui/dialog"
import { get_key_file } from "@/src/lib/cpg_ops";
import { Eye } from "lucide-react"
import React from "react";

interface FileViewerProps {
  fileName: string,

}

export function FileViewer(props: FileViewerProps) {
  const { fileName } = props;
  const [viewContent, setViewContent] = React.useState("");

  async function fetchData() {
    const data = await get_key_file(fileName);
    return data || "";
  }
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" onClick={async () => { const data = await fetchData(); setViewContent(data.toString()) }}>
          <Eye className="mr-2 h-4 w-4" /> View
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{fileName.split("/").pop()}</DialogTitle>
          <DialogDescription>
            {fileName}
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {viewContent}
        </div>
      </DialogContent>
    </Dialog>
  )
}
