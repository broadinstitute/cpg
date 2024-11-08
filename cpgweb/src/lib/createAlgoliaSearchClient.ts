import algoliasearch from "algoliasearch";

const client = algoliasearch("PTZBABFEDD", "e764d4f4ac72739260d49020c48b8f2f");
const index = client.initIndex("metadata");

export { index };
