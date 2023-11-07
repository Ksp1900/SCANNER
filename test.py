import socket
from impacket import smb
from impacket.smbconnection import SMBConnection

ip = "159.138.20.30"
port = 445

def checkSMB(ip,port):
    #SMB PROBE 생성
    pack = b"\x00\x00\x00\x45\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x01\xc8" \
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00" \
        b"\x00\x00\x00\x00\x00\x22\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e" \
        b"\x31\x32\x00\x02\x53\x4d\x42\x20\x32\x2e\x30\x30\x32\x00\x02\x53" \
        b"\x4d\x42\x20\x32\x2e\x3f\x3f\x3f\x00"
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((ip,port))
    sock.send(pack)
    
    recv = sock.recv(1024)
    if b'SMB' in recv:
        print(recv)
        return True
    else:
        return False

checkSMB(ip,port)
