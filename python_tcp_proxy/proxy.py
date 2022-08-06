import sys
import socket
import threading

# 可见字符
HEX_FILTER = "".join(
    [(len(repr(chr(i))) == 3) and chr(i) or "." for i in range(256)]
)


# print(HEX_FILTER)
# 格式化输出 16进制
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    result = []
    for i in range(0, len(src), length):
        word = str(src[i: i+length])

        printable = word.translate(HEX_FILTER)
        hex_a = " ".join([f"{ord(c):02x}" for c in word])
        hex_width = length * 3
        result.append(f"{i:04x}\t{hex_a:<{hex_width}}\t{printable}")

    if show:
        for line in result:
            print(line)

    else:
        return result


def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer


# 用于修改request
def request_handler(buffer):
    return buffer


# 用于修改response
def response_handler(buffer):
    return buffer


# 代理引擎
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # client_socket 本地端
    # remote_socket 指向远程服务端
    # receive_first 由本地先发出还是由服务端先发出
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)
            
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")
            
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            line = "[<==] Received %d bytes from remote." % len(local_buffer)
            print(line)
            hexdump(remote_buffer)
            
            local_buffer = response_handler(remote_buffer)
            client_socket.send(local_buffer)
            
        if not len(remote_buffer) and not len(local_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections")
            break
    

# 服务函数
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("problem on bind: %r" % e)
        
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: python3 proxy.py [localhost] [localport]", end="")
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: python3 proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    receive_first = sys.argv[5]
    
    if "True" in receive_first:
        receive_first = True
    
    else:
        receive_first = False
        
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)
            
            
if __name__ == "__main__":
    main()