#!/bin/sh

function print_msg() {
    echo "=================================================="
    echo $1
    echo "=================================================="
}

function deploy() {
    docker-compose --compatibility stop $1; docker-compose --compatibility rm -f $1;
    docker-compose --compatibility up -d $1;
}

function stress() {
    deploy $1
    print_msg "$1 stress"
    # wrk -t8 -c200 -d20s -T20s --latency http://127.0.0.1:$2$3
    wrk -t1 -c2 -d2s -T2s --latency http://127.0.0.1:$2$3
}

function combination() {
    stress $1 $2 /v1/hello
    stress $1 $2 /v1/hello/get
}

function print_help() {
    echo "Usage: bash $0 {all|nginx|flask|fastapi|node|tornado|gin|deploy_blog|sanic}"
    echo "e.g: $0 all"
    echo "e.g: $0 flask"
}

case "$1" in
  nginx)
    deploy nginx
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
  all)
    combination flask 8099
    combination fastapi 8098
    combination node 8097
    combination tornado 8096
    combination gin 8095
    combination sanic 8094
    ;;
  "")
  # -h|--help)
        print_help  # 参数为空时执行
        ;;
  *)  # 匹配都失败执行
        print_help
esac
