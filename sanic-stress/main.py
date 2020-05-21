import os

import aiohttp
from sanic import Sanic
from sanic.response import json, text

url = "http://{}:{}/v1/hello".format(os.environ.get("NGINX_HOST", "127.0.0.1"), os.environ.get("NGINX_PORT", 8089))


app = Sanic(__name__)
sem = None


@app.listener("before_server_start")
def init(app, loop):
    # global sem
    # concurrency_per_worker = 4
    # sem = asyncio.Semaphore(concurrency_per_worker, loop=loop)
    print("before_server_start")


@app.listener("after_server_stop")
def finish(app, loop):
    print("after_server_stop")
    loop.close()


@app.route("/v1/hello")
async def hello(request):
    return json({"msg": "hello"})


@app.route("/v1/hello/get")
async def hello_get(request):
    async with aiohttp.ClientSession() as session:
        # async with sem, session.get(url) as response:
        async with session.get(url) as response:
            content = await response.text()
            return text(content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8094, workers=2)
