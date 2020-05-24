# -*- coding: utf-8 -*-
import http.client
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests

import httplib2
import httpx
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen, httpclient
from tornado.options import define, options
from tornado.web import Finish
from tornado.web import URLSpec as U

define("port", default=8096, help="run on the given port", type=int)
define("debug", default=False, help="start debug mode", type=bool)
SLEEP_TIME = 3
COOKIE_SECRET = "seekplum"

url = "http://{}:{}/v1/hello".format(os.environ.get("NGINX_HOST", "127.0.0.1"), os.environ.get("NGINX_PORT", 8089))
u = urlparse(url)
host, port, path = u.hostname, u.port, u.path

requests_session = requests.Session()
httpx_session = httpx.Client()
httplib_session = httplib2.Http()
http_session = http.client.HTTPConnection(host, port)
# http_client = httpclient.HTTPClient()
http_async_client = httpclient.AsyncHTTPClient()


class BaseRequestHandler(tornado.web.RequestHandler):
    """Base RequestHandler"""

    # thread pool executor
    executor = ThreadPoolExecutor()

    def write_json(self, data):
        self.set_header("Content-Type", "application/json")
        if options.debug:
            self.write(json.dumps(data, indent=2))
        else:
            self.write(json.dumps(data))

    def success_response(self, data=None, message="", finish=True):
        response = {"error_code": 0, "message": message, "data": data}
        self.write_json(response)
        if finish:
            raise Finish


class HelloHandler(BaseRequestHandler):
    """测试使用的handler
    """

    def get(self):
        self.success_response({"msg": "hello"})


class HttpxHandler(BaseRequestHandler):
    def get(self):
        ts_start = time.time()
        response = httpx_session.get(url)
        ts_used = time.time() - ts_start
        data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": response.text}
        self.success_response(data)


class RequetsHandler(BaseRequestHandler):
    def get(self):
        ts_start = time.time()
        response = requests_session.get(url)
        ts_used = time.time() - ts_start
        data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "response": response.text}
        self.success_response(data)


class HttplibHandler(BaseRequestHandler):
    def get(self):
        ts_start = time.time()
        response, content = httplib_session.request(url, "GET")
        ts_used = time.time() - ts_start
        data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "content": content.decode("utf-8")}
        self.success_response(data)


class HttpHandler(BaseRequestHandler):
    def get(self):
        ts_start = time.time()
        http_session.request("GET", path)
        response = http_session.getresponse()
        content = ""
        while True:
            chunk = response.read(1024)
            if chunk:
                content += chunk.decode("utf-8")
            else:
                break
        ts_used = time.time() - ts_start
        data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "content": content}
        self.success_response(data)


class AsyncHTTPClientlibHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        ts_start = time.time()
        response = yield http_async_client.fetch(url)
        ts_used = time.time() - ts_start
        data = {"hello": "world", "ts_used": "{:.2f}s".format(ts_used), "content": response.body.decode("utf-8")}
        self.success_response(data)


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = dict(cookie_secret=COOKIE_SECRET, debug=options.debug)  # 相关API
        handlers = [
            U(r"/v1/hello", HelloHandler),
            U(r"/v1/httpx/get", HttpxHandler),
            U(r"/v1/requests/get", RequetsHandler),
            U(r"/v1/hello/get", RequetsHandler),
            U(r"/v1/httplib/get", HttplibHandler),
            U(r"/v1/http/get", HttpHandler),
            # U(r"/v1/httpclient/get", HTTPClientlibHandler),
            U(r"/v1/asynchttpclient/get", AsyncHTTPClientlibHandler),
        ]

        super(Application, self).__init__(handlers, **app_settings)


def main():
    """tornado入口函数
    """
    tornado.options.parse_command_line()
    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("Server start on port %s" % options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
