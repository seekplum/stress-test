FROM python:3.7-slim

ADD requirements.txt /tmp/requirements.txt
RUN set -xe \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone \
    && pip install -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && rm -f /tmp/requirements.txt
ADD . /code
WORKDIR /code
CMD ["/bin/bash", "-c", "env && uvicorn main:app --host 0.0.0.0 --port 8098 --reload"]
