# 压力测试

## 环境信息

- Docker: Docker version 19.03.5, build 633a0ea
- CPU: 限制1核
- 内存: 限制1024m

## 结论

| 框架    | normal  | httpx            | requests | httplib            | http                | async  |
| :------ | :------ | :--------------- | :------- | :----------------- | :------------------ | :----- |
| Node    | 2983.82 | 381.80(Axios 库) | -        | -                  | -                   | -      |
| Flask   | 774.53  | 222.58(错误: 4)  | 191.24   | 186.58(错误: 3784) | 492.66(错误: 9802)  | -      |
| Fastapi | 1791.78 | 273.47           | 241.32   | 10.89(错误: 5)     | 538.18(错误: 10345) | -      |
| Tornao  | 870.01  | 226.57           | 222.39   | 300.11             | 313.25              | 219.68 |
| Sanic   | -  | -(aiohttp)  | -        | -                  | -                   | -      |
| Golang  | - | -(Gin 库)   | -        | -                  | -                   | -      |

## 测试工具

### [ab](https://www.petefreitag.com/item/689.cfm)

- 1.安装

MacOSX 自带

- 2.使用

`-c`: 并发数

`-n`: 连接总请求数

```bash
ab -c 100 -n 5000 http://127.0.0.1:8099/v1/hello
```

- 3.结果解读

```text
Server Software:        web服务器名称
Server Hostname:        主机地址
Server Port:            端口号

Document Path:          URL地址
Document Length:        数据长度

Concurrency Level:      并发用户数
Time taken for tests:   所有请求处理完成时间总和
Complete requests:      总请求次数
Failed requests:        失败请求次数
Non-2xx responses:      非2xx状态请求数
Total transferred:      响应数据总长度
HTML transferred:       响应数据正文的数据总和，减去了header头的信息长度
Requests per second:    QPS吞吐率，每秒钟处理请求的数据
Time per request:       用户平均请求等待时间
Time per request:       服务器平均请求处理时间
Transfer rate:          单位时间内响应数据的长度

Connection Times (ms)   每个请求处理时间的分布情况表
```

### [siege](http://www.joedog.org/)

- 1.安装

```bash
brew install siege
```

- 2.使用

`-c`: 并发数

`-n`: 连接总请求数

```bash
siege -c 100 -r 50 -b http://127.0.0.1:8099/v1/hello
```

- 3.结果解读

```text
transactions:   完成的处理次数
availability:   成功率
elapsed_time:   总用时
data_transferred:   总传输数据
response_time:  网络连接速度
transaction_rate:   平均每秒完成的请求数
throughput: 平均每秒传送数据
concurrency:    实际最高并发数
successful_transactions:    成功处理次数
failed_transactions:    失败处理次数
longest_transaction:    每次传输花费最长时间
shortest_transaction:   每次传输花费最短时间
```

### [wrk](https://github.com/wg/wrk)

- 1.安装

```bash
brew install wrk
```

- 2.使用

`-t`: 要使用的线程总数

`-c`: 跟服务器建立并保持 TCP 连接数量，设置压测并发连接数

`-d`: 测试持续时间

wrk 使用异步非阻塞的 io，并不是用线程去模拟并发连接，因此不需要设置很多的线程，一般根据 CPU 的核心数量设置即可。另外 `-c` 参数设置的值必须大于 `-t` 参数的值。

```bash
# 获取CPU核数
python -c "import multiprocessing;print(multiprocessing.cpu_count())"

wrk -t4 -c1000 -d60s -T3s --latency http://127.0.0.1:8099/v1/hello
```

- 3.结果解读

```text
Latency:    响应时间
Req/Sec:    每个线程每秒钟的执行的连接数
Avg:        平均
Max:        最大
Stdev:      标准差
+/- Stdev:  正负一个标准差占比
Requests/sec:   每秒请求数（也就是QPS），等于总请求数/测试总耗时
Latency Distribution:   延迟情况及其分布
Socket errors:      socket 错误的数量
Non-2xx or 3xx responses:   非2xx,3xx状态请求数
```

## 测试方法

```bash
bash ./stress.sh -h
```
