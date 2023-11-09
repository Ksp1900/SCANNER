import socket
import ftplib
import synscan

ip = "192.168.229.131"
port = 2121

def checkMySQL(ip, port):
    # 소켓 생성 및 연결
    print(f"{port} : checking mysql...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.settimeout(2)
        banner = s.recv(1024)
        packet_Len = int.from_bytes(banner[0:2], 'little') # packet Length[3 Bytes]
        packet_Number = banner[3] # packet Number[1 Bytes]
        proto = int(banner[4]) # MySQL Protocol[1Bytes] 일반적인 경우 0xA Block된 경우 0xFF

        if packet_Len == (int(banner.__len__()) - 4) and packet_Number == 0: # packet 길이와 packet 번호가 mysql 프로토콜에 일반적인 값인지 확인
            if(proto == 255): #Blocked된 경우 MySQL Protocol
                return True
            elif(proto == 10): #일반적인 MySQL Protocol
                packet = str(banner[4:])
                ver = packet[4:packet.find("\\x00")] # 버전 식별
                print(ver)
                return True
            else:
                a = open("checkLog.txt",'a') # mysql 패킷헤더는 일치하나 프로토콜 검증 실패 시
                a.write(f"{ip} : {port} : {banner}\n")
                return False
        return False
    except Exception as e:
        return False

def checkFTP(ip,port):
    print(f"{port} : checking ftp...")
    try:
        ftp = ftplib.FTP()
        recv = ftp.connect(ip, port,timeout=5)
        if recv is not None:
            ver = recv.split("\n")[0] # 버전 식별
        else:
            return False
        print(recv)
        a = ftp.login('a','a')
        return True
    except (ftplib.error_perm) as e: # 로그인 에러 리턴시 
        if '530' in str(e):
            return True
        return False
    except Exception as e:
        print(e)
        return False

def checkRPC(ip, port):
    # 소켓 생성 및 연결
    print(f"{port} : checking rpc...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.settimeout(2)
        banner = s.recv(1024)
        print(banner)
    except Exception as e:
        print(e)
        return False

if(checkFTP(ip,port)):
    print('mysql')