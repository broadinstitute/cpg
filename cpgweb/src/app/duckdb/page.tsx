"use client";

// import dynamic from "next/dynamic";
import DuckApp from "./duckApp";


export default function DuckHome() {
  // const DuckApp = dynamic((
  //   () => import("./duckApp")
  // ), { ssr: false })
  return <DuckApp />
}
