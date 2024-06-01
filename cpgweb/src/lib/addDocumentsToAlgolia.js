const algoliasearch = require("algoliasearch");

const client = algoliasearch("PTZBABFEDD", "c53408d80183421b34323607bcbb31bd");
const index = client.initIndex("metadata");

const docs_1 = require("./processed_meta_1.json");
const docs_2 = require("./processed_meta_2.json");

index
  .saveObjects(docs_2, { autoGenerateObjectIDIfNotExist: true })
  .then(({ objectIDs }) => {
    console.log(objectIDs);
  })
  .catch((err) => {
    console.log(err);
  });
