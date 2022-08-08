import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client =  paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    
    _, stdout, strerr = client.exec_command(cmd)
    output = stdout.readlines() + strerr.readlines()
    if output:
        print("----OUTPUT----")
        for line in output:
            print(line)
    

if __name__ == "__main__":
    import getpass
    user = input("Username:")
    password = getpass.getpass()
    ip = input("Entry server ip:")
    port = int(input("Enter port:"))
    cmd = input("Entry command:")
    ssh_command(ip=ip, port=port, user=user, passwd=password, cmd=cmd)
        