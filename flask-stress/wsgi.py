# -*- coding: utf-8 -*-

import http.client
import json
import os
import time
from urllib.parse import urlparse

import requests
from flask import Blueprint, Flask, Response

import httplib2
import httpx

v1 = Blueprint("v1", __name__, url_prefix="/v1")
url = "http://{}:{}/v1/hello".format(os.environ.get("NGINX_HOST", "127.0.0.1"), os.environ.get("NGINX_PORT", 8089))
u = urlparse(url)
host, port, path = u.hostname, u.port, u.path

requests_session = requests.Session()
httpx_session = httpx.Client()
httplib_session = httplib2.Http()
http_session = http.client.HTTPConnection(host, port)


def jsonify(*args, **kwargs):
    """Response json格式化
    """
    return Response(json.dumps(dict(*args, **kwargs)), mimetype="application/json")


def successful_ret(**kwargs):
    """成功的请求
    """
    return jsonify(success=0, code=0, **kwargs)


@v1.route("/hello")
def hello():
    return "hello"


@v1.route("/hello/json")
def hello_json():
    return successful_ret(msg="hello")


@v1.route("/hello/sleep")
def hello_sleep():
    ts_start = time.time()
    time.sleep(2)
    ts_used = time.time() - ts_start
    return "hello {}".format(ts_used)


@v1.route("/httpx/get")
def httpx_get():
    ts_start = time.time()
    response = httpx_session.get(url)
    ts_used = time.time() - ts_start
    data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": response.text}
    return successful_ret(**data)


@v1.route("/requests/get")
@v1.route("/hello/get")
def requests_get():
    ts_start = time.time()
    response = requests_session.get(url)
    ts_used = time.time() - ts_start
    data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": response.text}
    return successful_ret(**data)


@v1.route("/httplib/get")
def httplib2_get():
    ts_start = time.time()
    response, content = httplib_session.request(url, "GET")
    ts_used = time.time() - ts_start
    data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "content": content.decode("utf-8")}
    return successful_ret(**data)


@v1.route("/http/get")
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
    data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "content": content}
    return successful_ret(**data)


app = Flask(__name__)
app.register_blueprint(v1)

if __name__ == "__main__":
    app.run("0.0.0.0", "8099")
