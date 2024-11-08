const fs = require("fs");
const { mkdir } = require("fs/promises");
const { Readable } = require("stream");
const { finished } = require("stream/promises");
const path = require("path");

const DOWNLOAD_PATH = path.join(__dirname, "..", "public", "duckdb-wasm");
// TODO:  Change to stable
const VERSION = "1.28.1-dev106.0";
const BASE_URL = `https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@${VERSION}/dist`;

const downloadFile = async (url, fileName) => {
  const res = await fetch(url);
  if (!fs.existsSync(DOWNLOAD_PATH)) await mkdir(DOWNLOAD_PATH);
  const destination = path.resolve(DOWNLOAD_PATH, fileName);
  const fileStream = fs.createWriteStream(destination, { flags: "wx" });
  await finished(Readable.fromWeb(res.body).pipe(fileStream));
};

// MVP main worker
downloadFile(
  `${BASE_URL}/duckdb-browser-mvp.worker.js`,
  "duckdb-browser-mvp.worker.js",
);

// EH Main Worker
downloadFile(
  `${BASE_URL}/duckdb-browser-eh.worker.js`,
  "duckdb-browser-eh.worker.js",
);

// COI Main Worker
downloadFile(
  `${BASE_URL}/duckdb-browser-coi.worker.js`,
  "duckdb-browser-coi.worker.js",
);

// COI PThread Worker
downloadFile(
  `${BASE_URL}/duckdb-browser-coi.pthread.worker.js`,
  "duckdb-browser-coi.pthread.worker.js",
);
