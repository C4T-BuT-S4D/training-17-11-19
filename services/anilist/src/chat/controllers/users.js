const { get } = require("../helpers/redis");
const User = require("../models/user");

const getBySession = async session => {
  if (session === null) {
    return null;
  }
  let user = await get(session);
  if (user === null) {
    return null;
  }
  user = JSON.parse(user);
  return new User(user.username, user.password);
};

module.exports = {
  getBySession
};
