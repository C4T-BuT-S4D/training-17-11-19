const MongoClient = require("mongodb").MongoClient;
const { promisify } = require("util");

const user = process.env.MONGO_INITDB_ROOT_USERNAME;
const password = process.env.MONGO_INITDB_ROOT_PASSWORD;

const url = `mongodb://${user}:${password}@mongo:27017`;

const client = new MongoClient(url);

const getDB = () => client.db("chat_db");

module.exports = {
  client,
  getDB
};
