const MongoClient = require("mongodb").MongoClient;
const { promisify } = require("util");

const url = "mongodb://mongo:27017";

const client = new MongoClient(url, {
  useUnifiedTopology: true
});

const getDB = () => client.db("chat_db");

module.exports = {
  client,
  getDB
};
