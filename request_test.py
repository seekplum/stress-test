# -*- coding: utf-8 -*-

import json
import time
from urllib.parse import urljoin

import requests


def json2it(data):
    if isinstance(data, list):
        return json.dumps(data)
    elif isinstance(data, dict):
        for k, v in data.items():
            data[k] = json2it(v)
        return data
    elif isinstance(data, (int, float)):
        return str(data)
    return data


def generate_requests_form_data_type(data):
    """把正常数据转成from_data需要的格式"""
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = None, json2it(v)
        return data
    return None, json2it(data)


def get(base):
    params = {"get": time.time()}
    response = requests.get(urljoin(base, "/v1/hello"), params=params)
    print(response.status_code, response.text)


def post(base):
    params = {"post": time.time()}
    data = {"post": time.time()}
    response = requests.post(urljoin(base, "/v1/hello"), params=params, json=data)
    print(response.status_code, response.text)


def post_form(base):
    params = {"post_form": time.time()}
    data = {"post_form": time.time()}
    response = requests.post(urljoin(base, "/v1/hello"), params=params, data=generate_requests_form_data_type(data),)
    print(response.status_code, response.text)


def main():
    host = "127.0.0.1"
    port = 8099
    base = "http://{}:{}".format(host, port)
    get(base)
    post(base)
    post_form(base)


if __name__ == "__main__":
    main()
