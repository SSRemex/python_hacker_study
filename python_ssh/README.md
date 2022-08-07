# SSH通信
`pip install paramiko`

`paramiko`基于`pycrypto`开发的第三方库


# ssh_cmd.py ssh命令执行client
## 流程
- `paramiko`编写SSH server 和 client
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

