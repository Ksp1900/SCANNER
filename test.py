import socket
import telnetlib

ip = "192.168.56.101"
port = 2023

def checkTFTP(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(5)
    s.sendto(b'',(ip,port))
    print(s.recvfrom(1024))
    s.close()

checkTFTP(ip,port)