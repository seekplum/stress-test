# Node压测

## 环境信息

- Docker: Docker version 19.03.5, build 633a0ea
- CPU: 限制1核
- 内存: 限制1024m

## 测试结果

```text

==================================================
normal stress
==================================================
Running 20s test @ http://127.0.0.1:8097/v1/hello
  8 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    68.38ms   33.10ms 421.55ms   81.04%
    Req/Sec   376.68    142.27     0.95k    73.07%
  Latency Distribution
     50%   62.08ms
     75%   83.10ms
     90%  103.05ms
     99%  185.84ms
  59920 requests in 20.08s, 11.89MB read
  Socket errors: connect 0, read 107, write 1, timeout 0
Requests/sec:   2983.82
Transfer/sec:    606.09KB
==================================================
Axios stress
==================================================
Running 20s test @ http://127.0.0.1:8097/v1/hello/get
  8 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   526.69ms  192.73ms   1.49s    80.51%
    Req/Sec    54.47     38.46   237.00     68.30%
  Latency Distribution
     50%  512.79ms
     75%  594.38ms
     90%  705.28ms
     99%    1.41s
  7674 requests in 20.10s, 1.63MB read
  Socket errors: connect 0, read 57, write 6, timeout 0
Requests/sec:    381.80
Transfer/sec:     83.15KB
```
