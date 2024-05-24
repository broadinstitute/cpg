import * as duckdb from "@duckdb/duckdb-wasm";
import { ListObjectsV2Command, S3Client } from "@aws-sdk/client-s3";

const get_anon_s3_client = (): S3Client => {
  return new S3Client({
    region: "us-east-1",
    signer: { sign: async (req) => req },
  });
};

const get_all_index_files = async (
  s3: S3Client,
): Promise<string[] | undefined> => {
  const command = new ListObjectsV2Command({
    Bucket: "cellpainting-gallery-inventory",
    Prefix: "cellpainting-gallery/index/",
  });
  try {
    let isTruncated: boolean | undefined = true;
    let contents = "";
    while (isTruncated) {
      const { Contents, IsTruncated, NextContinuationToken } =
        await s3.send(command);
      const contentList = Contents?.map((c) => `.${c.Key}`).join("\n");
      contents += contentList + "\n";
      isTruncated = IsTruncated;
      command.input.ContinuationToken = NextContinuationToken;
    }
    console.log(contents);
    return [contents];
  } catch (err) {
    console.log(err);
  }
};

const fetch_all_projects = (db: duckdb.AsyncDuckDB) => {};

export { get_anon_s3_client, get_all_index_files, fetch_all_projects };
