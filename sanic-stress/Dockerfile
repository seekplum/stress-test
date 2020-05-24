FROM python:3.7-slim

ADD requirements.txt /tmp/requirements.txt
RUN set -xe \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone \
    && pip install -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt
ADD . /code
WORKDIR /code
# CMD ["/bin/bash", "-c", "env && gunicorn -w 2 -t 60 -b :8094 --log-level debug main:app --worker-class sanic.worker.GunicornWorker"]
CMD ["/bin/bash", "-c", "env && python main.py"]
