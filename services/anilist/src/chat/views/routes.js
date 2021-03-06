const express = require("express");

router = express.Router();

const usersCtrl = require("../controllers/users");
const { getDB } = require("../helpers/mongo");

router.post("/enter/", async (req, res) => {
  const { session = null } = req.cookies;
  const user = await usersCtrl.getBySession(session);
  if (user === null) {
    res.status(400);
    res.json({ error: "no auth" });
    return;
  }
  const db = getDB();
  const users = db.collection("users");
  const me = await users.findOne({
    name: user.name.replace(/[ \x00-\x1f!@#$%^&*()]/g, "")
  });
  if (me === null) {
    users.insertOne({ name: user.name });
  }
  res.json({ result: "ok" });
});

router.get("/users/", async (req, res) => {
  const { session = null } = req.cookies;
  const user = await usersCtrl.getBySession(session);
  if (user === null) {
    res.status(400);
    res.json({ error: "no auth" });
    return;
  }
  const db = getDB();
  const usersC = db.collection("users");
  const users = await usersC.find({}).toArray();
  res.json({ result: users });
});

router.post("/get_messages/", async (req, res) => {
  const { session = null } = req.cookies;
  const user = await usersCtrl.getBySession(session);
  if (user === null) {
    res.status(400);
    res.json({ error: "no auth" });
    return;
  }
  const db = getDB();
  const users = db.collection("users");
  const me = await users.findOne({ name: user.name });
  if (me === null) {
    res.status(400);
    res.json({ error: "no chat entered" });
    return;
  }
  const from = user.name.replace(/[ \x00-\x1f!@#$%^&*()]/g, "");
  let body = req.body;
  if (body.to === undefined) {
    res.status(400);
    res.json({ error: "no name provided" });
    return;
  } else {
    body.to = body.to.replace(/[ \x00-\x1f!@#$%^&*()]/g, "");
  }

  const messagesC = db.collection("messages");

  const messages = await messagesC
    .find({ from, ...body })
    .sort({ time: 1 })
    .toArray();

  res.json({ result: messages });
});

router.post("/send_message/", async (req, res) => {
  const { session = null } = req.cookies;
  const user = await usersCtrl.getBySession(session);
  if (user === null) {
    res.status(400);
    res.json({ error: "no auth" });
    return;
  }
  const db = getDB();
  const users = db.collection("users");
  const me = await users.findOne({ name: user.name });
  if (me === null) {
    res.status(400);
    res.json({ error: "no chat entered" });
    return;
  }
  const from = user.name.replace(/[ \x00-\x1f!@#$%^&*()]/g, "");
  let body = req.body;
  if (body.to === undefined) {
    res.status(400);
    res.json({ error: "no name provided" });
    return;
  } else {
    body.to = body.to.replace(/[ \x00-\x1f!@#$%^&*()]/g, "");
  }

  if (body.message === undefined) {
    res.status(400);
    res.json({ error: "no message provided" });
    return;
  }

  const messages = db.collection("messages");

  const time = new Date();

  messages.insertOne({ time, from: from, to: body.to, message: body.message });
  messages.insertOne({ time, from: body.to, to: from, message: body.message });

  res.json({ result: "ok" });
});

module.exports = {
  router
};
