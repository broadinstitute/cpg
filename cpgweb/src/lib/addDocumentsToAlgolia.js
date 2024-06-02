const algoliasearch = require("algoliasearch");

const client = algoliasearch("PTZBABFEDD", "c53408d80183421b34323607bcbb31bd");
const index = client.initIndex("metadata");

const docs = require("./processed_meta.json");

index
  .saveObjects(docs, { autoGenerateObjectIDIfNotExist: true })
  .then(({ objectIDs }) => {
    console.log(objectIDs);
  })
  .catch((err) => {
    console.log(err);
  });
