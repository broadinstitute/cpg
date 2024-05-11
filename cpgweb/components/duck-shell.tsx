"use client"

import dynamic from "next/dynamic";


export default function DuckHome() {
  const DuckApp = dynamic((
    () => import("../src/app/duckdb/duckApp")
  ), { ssr: false })
  return <DuckApp />
}
