const redis = require("redis");
const client = redis.createClient({
  host: "redis",
  password: process.env.REDIS_PASSWORD
});
const { promisify } = require("util");

client.on("error", function(err) {
  console.error("Error " + err);
});

const get = promisify(client.get).bind(client);

module.exports = {
  get
};
