# Python tcp 代理
这是一个指定客户端服务端的代理程序

> 字符处理

### 目的
分析未知协议，篡改应用网络流量，为fuzzer创建测试用例

### 实现
 - 通信数据显示（hexdump）
 - 数据接收（receive_from）
 - 控制流量方向（proxy_handle）
 - 流量监听（server_loop）
 - Request修改（可选）
 - Response修改（可选）


### 流程
request: 本地 client ==> proxy ==> 远程服务remote
response: 远程服务remote ==> proxy ==> 本地client

### 执行
**step 1**

代理 ==> `python3 proxy.py 127.0.0.1 9000 127.0.0.1 9001 True`

**step 2**

web服务 ==> `test_server` 目录下，执行 `python3 -m http.server --bind 127.0.0.1 9001`

**step 3**

代理验证 ==> `curl 127.0.0.1:9000`

### Example:
```
> Received incoming connection from 127.0.0.1:50417
[==>] Received 78 bytes from localhost.
0000    47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a         GET / HTTP/1.1..
0010    48 6f 73 74 3a 20 31 32 37 2e 30 2e 30 2e 31 3a         Host: 127.0.0.1:
0020    39 30 30 30 0d 0a 55 73 65 72 2d 41 67 65 6e 74         9000..User-Agent
0030    3a 20 63 75 72 6c 2f 37 2e 36 38 2e 30 0d 0a 41         : curl/7.68.0..A
0040    63 63 65 70 74 3a 20 2a 2f 2a 0d 0a 0d 0a               ccept: */*....
[==>] Sent to remote.
[<==] Received 78 bytes from remote.
0000    48 54 54 50 2f 31 2e 30 20 32 30 30 20 4f 4b 0d         HTTP/1.0 200 OK.
0010    0a 53 65 72 76 65 72 3a 20 53 69 6d 70 6c 65 48         .Server: SimpleH
0020    54 54 50 2f 30 2e 36 20 50 79 74 68 6f 6e 2f 33         TTP/0.6 Python/3
0030    2e 38 2e 31 30 0d 0a 44 61 74 65 3a 20 54 68 75         .8.10..Date: Thu
0040    2c 20 30 34 20 41 75 67 20 32 30 32 32 20 31 37         , 04 Aug 2022 17
0050    3a 30 30 3a 30 36 20 47 4d 54 0d 0a 43 6f 6e 74         :00:06 GMT..Cont
0060    65 6e 74 2d 74 79 70 65 3a 20 74 65 78 74 2f 68         ent-type: text/h
0070    74 6d 6c 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 65 6e         tml..Content-Len
0080    67 74 68 3a 20 32 31 0d 0a 4c 61 73 74 2d 4d 6f         gth: 21..Last-Mo
0090    64 69 66 69 65 64 3a 20 54 68 75 2c 20 30 34 20         dified: Thu, 04 
00a0    41 75 67 20 32 30 32 32 20 31 36 3a 35 36 3a 31         Aug 2022 16:56:1
00b0    39 20 47 4d 54 0d 0a 0d 0a 3c 70 3e 68 65 6c 6c         9 GMT....<p>hell
00c0    6f 20 73 73 72 65 6d 65 78 3c 2f 70 3e 0a               o ssremex</p>.
[*] No more data. Closing connections
```