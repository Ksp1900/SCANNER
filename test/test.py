import socket
import ftplib
import datetime

ip = "192.168.229.131"
port = 123

def check_NTP(ip,port):
    print(f"{port} : checking NTP...")
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # NTP PROBE 생성
    pack = b"\xe3\x00\x04\xfa\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"\
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"\
    b"\x00\x00\x00\x00\x00\x00\x00\x00\xc5\x4f\x23\x4b\x71\xb1\x52\xf3"

    s.settimeout(5)
    try:
        s.sendto(pack,(ip,port))
        recv, server = s.recvfrom(1024)
        if recv.__len__() >= 48 and (0 < int(recv[1] < 15)): # 패킷 최소 길이 및 startum(0~15) 값인지 확인
            return True
        return False
    except:
        return False
    finally:
        s.close()

if(check_NTP(ip,port)):
    print('mysql')