/** @format */
const express = require("express");
const app = express();
const Axios = require("axios");
const requests = Axios.create();

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

app.get("/v1/hello", (req, res, next) => {
  res.send("hello");
});
app.get("/v1/hello/json", (req, res, next) => {
  res.json({ hello: "hello" });
});
app.get("/v1/hello/sleep", async (req, res, next) => {
  await sleep(2000);
  res.send("hello");
});
app.get("/v1/hello/get", async (req, res, next) => {
  const nginx_host = process.env.NGINX_HOST || "127.0.0.1";
  const nginx_port = process.env.NGINX_PORT || "8089";
  const url = `http://${nginx_host}:${nginx_port}/v1/hello`;
  console.log("nginx_host:", nginx_host, "nginx_port:", nginx_port);
  await requests.get(url).then((response) => {
    res.send(response.data);
  });
});

app.listen(8097, () => {
  console.log("Server running on port 8097");
});
