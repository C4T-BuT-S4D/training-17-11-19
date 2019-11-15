const redis = require("redis");
const client = redis.createClient({
  host: "redis",
  password: "9bdfe927ddbf2efc21aa3400a106d8f2" //CHANGE THIS!
});
const { promisify } = require("util");

client.on("error", function(err) {
  console.error("Error " + err);
});

const get = promisify(client.get).bind(client);

module.exports = {
  get
};
