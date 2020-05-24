#!/bin/sh

function print_msg() {
    echo "=================================================="
    echo $1
    echo "=================================================="
}

function deploy() {
    docker-compose stop $1 >/dev/null 2>&1; docker-compose rm -f $1 >/dev/null 2>&1; echo "rm $1"
    docker-compose up -d $1 >/dev/null 2>&1; echo "up $1"
}

function stress() {
    deploy $1
    print_msg "$1 stress"
    sleep 2
    echo "stress url: http://127.0.0.1:$2$3"
    # wrk -t8 -c200 -d20s -T20s --latency http://127.0.0.1:$2$3
    curl http://127.0.0.1:$2$3
    echo ""
    sleep 1
}

function combination() {
    stress $1 $2 /v1/hello
    stress $1 $2 /v1/hello/get
}

function print_help() {
    echo "Usage: bash $0 {all|deploy|flask|fastapi|node|tornado|gin|deploy_blog|sanic|openresty}"
    echo "e.g: $0 all"
    echo "e.g: $0 deploy"
}

case "$1" in
  deploy)
    deploy nginx statsd cadvisor prometheus grafana
    ;;
  compose)
    docker-compose --compatibility ${@:2}
    ;;
  flask)
    combination flask 8099
    ;;
  fastapi)
    combination fastapi 8098
    ;;
  node)
    combination node 8097
    ;;
  tornado)
    combination tornado 8096
    ;;
  gin)
    combination gin 8095
    ;;
  sanic)
    combination sanic 8094
    ;;
  openresty)
    combination openresty 8093
    ;;
  all)
    deploy nginx
    combination flask 8099
    combination fastapi 8098
    combination node 8097
    combination tornado 8096
    combination gin 8095
    combination sanic 8094
    combination openresty 8093
    ;;
  "")
  # -h|--help)
        print_help  # 参数为空时执行
        ;;
  *)  # 匹配都失败执行
        print_help
        ;;
esac
