"use client";
import { Metadata } from "next"
import Link from "next/link"

import { cn } from "@/lib/utils"
import { Announcement } from "@/components/announcement"
import { WidgetsNav } from "@/components/widgets-nav"
import {
  PageActions,
  PageHeader,
  PageHeaderDescription,
  PageHeaderHeading,
} from "@/components/page-header"
import { buttonVariants } from "@/registry/new-york/ui/button"

// export const metadata: Metadata = {
//   title: "CPG Web",
//   description: "Explore Cellpainting Gallery.",
// }

interface HomeLayoutProps {
  children: React.ReactNode
}

export default function WidgetsLayout({ children }: HomeLayoutProps) {
  return (
    <div className="bg-white container relative">
      <PageHeader>
        <Announcement />
        <PageHeaderHeading className="hidden md:block">
          CellPainting Gallery
        </PageHeaderHeading>
        <PageHeaderHeading className="md:hidden">
          CellPainting Gallery
        </PageHeaderHeading>
        <PageHeaderDescription>
          The Cell Painting Gallery is a collection of image datasets created using the Cell Painting assay.
          The images of cells are captured by microscopy imaging, and reveal the response of various labeled cell components
          to whatever treatments are tested, which can include genetic perturbations, chemicals or drugs, or different cell
          types.
        </PageHeaderDescription>
        <PageActions>
          <Link href="/docs" className={cn(buttonVariants(), "rounded-[6px]")}>
            Docs
          </Link>
          <Link
            href="/examples"
            className={cn(
              buttonVariants({ variant: "outline" }),
              "rounded-[6px]"
            )}
          >
            Examples
          </Link>
        </PageActions>
      </PageHeader>
      <WidgetsNav className="[&>a:first-child]:text-primary" />
      <section>
        <div className="overflow-hidden rounded-[0.5rem] border bg-background">
          {children}
        </div>
      </section>
    </div>
  )
}
