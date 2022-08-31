import argparse
import socket
# shlex shell 语法分析器
import shlex
import subprocess
import sys
import textwrap
import threading


# 命令执行函数
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    try:
        output = subprocess.check_output(shlex.split(cmd))
    except Exception as e:
        return str(e)
    try:
        out = output.decode()
    except UnicodeDecodeError:
        out = output.decode("gbk")
    else:
        out = str(Exception)

    return out


# 参数接收函数
def arg_get():
    parser = argparse.ArgumentParser(
        description="fake python NC",
        # 自定义帮助文档
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""Example:
        python3 netcat.py -t 127.0.0.1 -p 5555 -l -c # command shell
        python3 netcat.py -t 127.0.0.1 -p 5555 -l -u=test.txt # upload to file
        python3 netcat.py -t 127.0.0.1 -p 5555 -l -e="cat /etc/passwd" # command shell
        echo "ABC" | python3 netcat.py -t 127.0.0.1 -p 135 # echo text to server port 135
        python3 netcat.py -t 127.0.0.1 -p 5555 # connect to server
        """)
    )

    parser.add_argument("-c", "--command", action="store_true", help="command shell")
    # parser.add_argument("-e", "--execute", help="execute specified command")
    parser.add_argument("-l", "--listen", action="store_true", help="listen")
    parser.add_argument("-p", "--port", type=int, default=5555, help="specified port")
    parser.add_argument("-t", "--target", default="0.0.0.0", help="specified ip")
    parser.add_argument("-u", "--upload", help="upload file")

    args = parser.parse_args()
    return args


class NetCat:
    def __init__(self, args):
        self.args = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        try:
            while True:
                buffer = input(">> ")
                buffer += "\n"
                self.socket.send(buffer.encode())
                data = self.socket.recv(8192)
                response = data.decode()
                print(response)
                if buffer.strip() == "exit":
                    sys.exit()

        except KeyboardInterrupt:
            print("Bye")
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        print(f"Listening on {self.args.target} {self.args.port}")
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            print(f"Connection received on {_[0]} {_[1]}")
            client_thread = threading.Thread(
                target=self.handle,
                args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        if self.args.upload:
            file_buffer = b""
            while True:
                data = client_socket.recv(8192)
                if data:
                    file_buffer += data

                else:
                    break

            with open(self.args.upload, "wb") as f:
                f.write(file_buffer)

            message = f"upload [{self.args.upload}] successful!"
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b""
            while True:
                try:
                    while "\n" not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(1024)
                    cmd = cmd_buffer.decode()
                    print(f"cmd ==> {cmd}")
                    if cmd.strip() == "exit":
                        print("killed!")
                        client_socket.send("killed!".encode())
                        self.socket.close()
                    response = execute(cmd)
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b""

                except Exception as e:
                    cmd_buffer = b""
        else:
            out = client_socket.recv(2048)
            print(out.decode())


if __name__ == '__main__':
    args = arg_get()

    nc = NetCat(args)
    nc.run()
