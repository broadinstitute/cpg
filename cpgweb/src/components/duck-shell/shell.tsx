"use client";

import * as duckdb from "@duckdb/duckdb-wasm";
import * as shell from "@duckdb/duckdb-wasm-shell";
import * as rd from "@duckdb/react-duckdb";
import React from "react";
// import styles from "./shell.module.css";

import shell_wasm from "@duckdb/duckdb-wasm-shell/dist/shell_bg.wasm";

interface ShellProps {
  backgroundColor?: string;
  padding?: number[];
  borderRadius?: number[];
}

const Shell: React.FC<ShellProps> = (props: ShellProps) => {
  const [termContainer, setTermContainer] =
    React.useState<HTMLDivElement | null>(null);
  const [added, setAdded] = React.useState(false);
  const db = rd.useDuckDB();
  const resolveDB = rd.useDuckDBResolver();
  const shellDBResolver = React.useRef<
    [(db: duckdb.AsyncDuckDB) => void, (err: any) => void] | null
  >(null);
  const shellStatusUpdater =
    React.useRef<duckdb.InstantiationProgressHandler | null>(null);

  // Launch DuckDB
  React.useEffect(() => {
    if (!db.resolving()) {
      resolveDB();
    }
  }, [db, resolveDB]);

  // Embed the shell into the term container
  React.useEffect(() => {
    (async () => {
      if (termContainer && !added) {
        setAdded(true);
        await shell.embed({
          shellModule: shell_wasm,
          container: termContainer,
          // fontFamily: "monospace",
          resolveDatabase: (p: duckdb.InstantiationProgressHandler) => {
            if (db.error != null) {
              return Promise.reject(db.error);
            }
            if (db.value != null) {
              return Promise.resolve(db.value);
            }
            shellStatusUpdater.current = p;
            const result = new Promise<duckdb.AsyncDuckDB>(
              (resolve, reject) => {
                shellDBResolver.current = [resolve, reject];
              }
            );
            return result;
          },
        });
      }
    })();
  }, [db.error, db.value, termContainer]);

  // Propagate the react state updates to the wasm progress handler
  React.useEffect(() => {
    if (db.value != null) {
      if (shellDBResolver.current != null) {
        const resolve = shellDBResolver.current[0];
        shellDBResolver.current = null;
        resolve(db.value);
      }
    } else if (db.error != null) {
      if (shellDBResolver.current != null) {
        const reject = shellDBResolver.current[1];
        shellDBResolver.current = null;
        reject(db.error);
      }
    } else if (db.progress != null) {
      if (shellStatusUpdater.current) {
        shellStatusUpdater.current(db.progress);
      }
    }
  }, [db]);

  const style: React.CSSProperties = {
    padding: props.padding
      ? `${props.padding.map((p) => `${p}px`).join(" ")}`
      : "0px",
    borderRadius: props.borderRadius
      ? `${props.borderRadius.map((p) => `${p}px`).join(" ")}`
      : "0px",
    backgroundColor: props.backgroundColor || "transparent",
  };
  return (
    <div style={style}>
      <div
        ref={(el) => setTermContainer(el)}
      />
    </div>
  );
};

export default Shell;
