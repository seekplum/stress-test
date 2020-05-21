import asyncio
import http.client
import os
import time
from urllib.parse import urlparse

import requests

import httplib2
import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI()
url = "http://{}:{}/v1/hello".format(os.environ.get("NGINX_HOST", "127.0.0.1"), os.environ.get("NGINX_PORT", 8089))
u = urlparse(url)
host, port, path = u.hostname, u.port, u.path

requests_session = requests.Session()
httpx_session = httpx.AsyncClient()
httplib_session = httplib2.Http()
http_session = http.client.HTTPConnection(host, port)


@app.get("/v1/hello")
def hello():
    return "hello"


@app.get("/v1/hello/json")
def hello_json():
    return {"hello": "world"}


@app.get("/v1/hello/sleep")
async def hello_sleep():
    await asyncio.sleep(2)
    return "hello"


@app.get("/v1/httpx/get")
async def httpx_get():
    ts_start = time.time()
    response = await httpx_session.get(url)
    ts_used = time.time() - ts_start
    return {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": response.text}


@app.get("/v1/requests/get")
def requests_get():
    ts_start = time.time()
    response = requests_session.get(url)
    ts_used = time.time() - ts_start
    return {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": response.text}


@app.get("/v1/httplib/get")
@app.get("/v1/hello/get")
def httplib2_get():
    ts_start = time.time()
    response, content = httplib_session.request(url, "GET")
    content = content.decode("utf-8")
    ts_used = time.time() - ts_start
    return {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": content}


@app.get("/v1/http/get")
def http_get():
    ts_start = time.time()
    http_session.request("GET", path)
    response = http_session.getresponse()
    content = ""
    while True:
        chunk = response.read(200)
        if chunk:
            content += chunk.decode("utf-8")
        else:
            break
    ts_used = time.time() - ts_start
    return {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "content": content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8098)
