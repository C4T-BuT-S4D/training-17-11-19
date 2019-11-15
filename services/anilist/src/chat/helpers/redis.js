const redis = require("redis");
const client = redis.createClient();
const { promisify } = require("util");

client.on("error", function(err) {
  console.error("Error " + err);
});

const get = promisify(client.get).bind(client);

module.exports = {
  get
};
