import socket
import ftplib
import datetime

ip = "218.50.136.184"
port = 23

def check_DNS(ip, port):
    print(f"{port} : checking DNS...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    sock.settimeout(3)
    try:
        data = sock.recv(1024)
        print(data)
        return True
    except Exception as e:
        return False
    finally:
        sock.close()


if(check_DNS(ip,port)):
    print('mysql')