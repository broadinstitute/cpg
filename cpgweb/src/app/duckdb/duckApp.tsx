"use client";

import * as React from "react";

import * as duckdb from "@duckdb/duckdb-wasm";
import duckdb_wasm from "@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm";
import duckdb_wasm_eh from "@duckdb/duckdb-wasm/dist/duckdb-eh.wasm";
import duckdb_wasm_coi from "@duckdb/duckdb-wasm/dist/duckdb-coi.wasm";

import "bootstrap/dist/css/bootstrap.min.css";
import "xterm/css/xterm.css";

import {
  DuckDBConnectionProvider,
  DuckDBPlatform,
  DuckDBProvider,
} from "@duckdb/react-duckdb";
import { Shell } from "./shell";


const DUCKDB_BUNDLES: duckdb.DuckDBBundles = {
  mvp: {
    mainModule: duckdb_wasm,
    mainWorker: new URL(
      "@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js",
      import.meta.url
    ).toString(),
  },
  eh: {
    mainModule: duckdb_wasm_eh,
    mainWorker: new URL(
      "@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js",
      import.meta.url
    ).toString(),
  },
  coi: {
    mainModule: duckdb_wasm_coi,
    mainWorker: new URL(
      "@duckdb/duckdb-wasm/dist/duckdb-browser-coi.worker.js",
      import.meta.url
    ).toString(),
    pthreadWorker: new URL(
      "@duckdb/duckdb-wasm/dist/duckdb-browser-coi.pthread.worker.js",
      import.meta.url
    ).toString(),
  },
};
const logger = new duckdb.ConsoleLogger(duckdb.LogLevel.WARNING);

export default function DuckApp() {
  return (
    <DuckDBPlatform logger={logger} bundles={DUCKDB_BUNDLES}>
      <DuckDBProvider>
        <DuckDBConnectionProvider>
          <Shell padding={[16, 0, 0, 20]} backgroundColor="#333" />
        </DuckDBConnectionProvider>
      </DuckDBProvider>
    </DuckDBPlatform>
  );
}

