const express = require("express");
const cookieParser = require("cookie-parser");
const app = express();
const mongo = require("./helpers/mongo");

app.use(cookieParser());
app.use(express.json());

routes = require("./views/routes");

app.use("/api/chat/", routes.router);

const port = 9000;

mongo.client.connect(function(err) {
  if (err === null) {
    app.emit("ready");
  } else {
    console.error("Error" + err);
  }
});

app.on("ready", function() {
  app.listen(port, () => console.log(`Chat listening on port ${port}!`));
});
