import socket
import ftplib
import datetime

ip = "192.168.229.131"
port = 45557

def check_DNS(ip, port):
    print(f"{port} : checking DNS...")
    message = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(message,(ip, port))
        data, _ = sock.recvfrom(512)
        return True
    except Exception as e:
        return False
    finally:
        sock.close()


if(check_DNS(ip,port)):
    print('mysql')