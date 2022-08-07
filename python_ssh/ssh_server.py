import os
import paramiko
import socket
import sys
import threading


CWD = os.path.dirname(os.path.realpath(__file__))
HOST_KEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        
    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username: str, password: str) -> int:
        if (username == "ssr") and (password == "ssr"):
            return paramiko.AUTH_SUCCESSFUL
        

if __name__ == "__main__":
    server = "127.0.0.1"
    ssh_port = 2222
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+] Listening for connection ...")
        client, addr = sock.accept()
    
    except Exception as e:
        print("[-] Listen fail : " + str(e))
        sys.exit(1)
    
    session = paramiko.Transport(client)
    session.add_server_key(HOST_KEY)
    
    server = Server()
    
    session.start_server(server=server)
    
    chan = session.accept(20)
    
    if chan is None:
        print("*** No channel.")
        sys.exit(1)
    
    print("[+] Authenticated!")
    print(chan.recv(1024))
    chan.send("Welcome to ssh")
    try:
        while True:
            command = input("Enter command:")
            if command != "exit":
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send("exit")
                print("exting")
                session.close()
                break
    except KeyboardInterrupt:
        session.close()
    
    
    