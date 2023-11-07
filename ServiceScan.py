import socket
import requests
import smtplib
import paramiko
import ftplib
import telnetlib
import ssl
import sys


# 변경점
# 1 : HTTP 배너그래빙의 기능을 변경하여 HTTP와 HTTPS 구별 기능 추가
#TEST

## TCP SERVICE ##
def http_banner_grabbing(ip, port): # https 요청까지 하기 위해 변수를 수정했습니다.
    print(f"{port} : checking http...")
    try:
        target_url = f"http://{ip}:{port}" 
        response = requests.get(target_url, timeout=5) 
        return response.url[0:5] # http: or https 리턴
    except requests.exceptions.RequestException as e: # http 요청 실패 시 https 요청
        try: #HTTPS 인증서를 확인하여 임의 추정 가능
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with socket.create_connection((ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    print(f"ip {ip}, port {port}에 연결합니다.")
                    cert = ssock.getpeercert()
                    print("Server certificate:")
                    for key, value in cert.items():
                        print(f"{key}: {value}")
            return False
        except ssl.SSLError as e:
            return False
        except Exception as e:
            return False
    except Exception as e:
        return False

def checkMySQL(ip, port):
    # 소켓 생성 및 연결
    print(f"{port} : checking mysql...")
    check_list = [b'caching_sha2', b'mysql', b'MySQL', b'MariaDB'] # 체크리스트
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.settimeout(2)
        banner = s.recv(1024)
        packet = banner[4:] # packet Length, Number 제외
        code = int(packet[0]) # 일반적인 경우 0xA Block된 경우 0xFF

        for check in check_list:
            if check in banner:
                if(code == 255): #Blocked된 경우
                    return True
                elif(code == 10): #일반적인 mysql 프로토콜 번호
                    packet = str(packet)
                    ver = packet[4:packet.find("\\x00")] # 버전 식별
                    return True
                else:
                    a = open("checkLog.txt",'a') #문자열은 매칭하나 추가 검증 실패시 로그
                    a.write(f"{ip} : {port} : {banner}\n")
                    return False
        
        return False
    except Exception as e:
        return False
    
def checkSSH(ip, port):
    # 소켓 생성 및 연결
    print(f"{port} : checking ssh...")
    banner = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 방식
        s.settimeout(5)
        s.connect((ip, port))
        # 서버 응답
        banner = s.recv(1024).decode(errors='ignore')
        s.close()
        if "SSH" in banner:
            return True
    except (socket.timeout, socket.error):
        try:
            transport = paramiko.Transport((ip, port))
            transport.start_client()
            paramiko_banner = transport.remote_version
            transport.close()

            if paramiko_banner:
                return True
                
        except paramiko.SSHException as e:
            return False
        except Exception as e:
            return False
    
    
def checkFTP(ip,port):
    print(f"{port} : checking ftp...")
    try:
        ftp = ftplib.FTP()
        recv = ftp.connect(ip, port,timeout=5)
        if recv is not None:
            ver = ver.decode().split("\n")[0] # 버전 식별
        else:
            return False
        ftp.login()
        return True
    except (ftplib.error_temp, ftplib.error_perm, ftplib.error_reply,ftplib.error_proto) as e:
        print(e)
        return True
    except Exception as e:
        return False
    
def checkTelnet(ip, port):
    print(f"{port} : checking telnet...")
    try:
        tel = telnetlib.Telnet(ip,port,timeout=5)
        recv = tel.read_until(b"login",timeout=5)
        if recv is not None:
            ver = ver.decode().split("\n")[0] # 버전 식별
        else:
            return False
    except Exception as e:
        return False

def check_SMTP(ip, port):
    print(f"{port} : checking smtp...")
    try:
        with smtplib.SMTP(ip, port, timeout=5) as server:
            banner = server.ehlo()
            if not banner:
                banner = server.helo()
            print("SMTP server banner:", banner)
            server.quit()
            return True
    except smtplib.SMTPException as e:
        print(f"SMTP error on port {port}: {str(e)}")
        return False
    except Exception as e:
        print(f"General error on port {port}: {str(e)}")
        return False
    
def checkSMB(ip,port):
    print(f"{port} : checking smb...")
    #SMB PROBE 생성
    pack = b"\x00\x00\x00\x45\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x01\xc8" \
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00" \
        b"\x00\x00\x00\x00\x00\x22\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e" \
        b"\x31\x32\x00\x02\x53\x4d\x42\x20\x32\x2e\x30\x30\x32\x00\x02\x53" \
        b"\x4d\x42\x20\x32\x2e\x3f\x3f\x3f\x00"
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip,port))
        sock.send(pack)
        
        recv = sock.recv(1024)
        if b'SMB' in recv:
            return True
        else:
            return False
    except Exception as e:
        return False

## UDP SERVICE ##
def checkNTP(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # NTP PROBE 생성
    pack = b"\xe3\x00\x04\xfa\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    pack2 = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    pack3 = b"\x00\x00\x00\x00\x00\x00\x00\x00\xc5\x4f\x23\x4b\x71\xb1\x52\xf3"

    pack = pack + pack2 + pack3

    s.settimeout(5)
    s.sendto(pack,(ip,port))
    recv, server = s.recvfrom(1024)
    
    if recv is not None:
        return True
    
    s.close()
    
def check_DNS(ip, port):
    message = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    try:
        sock.sendto(message,(ip, port))
        data, _ = sock.recvfrom(512)
        return True
    except Exception as e:
        return False
    finally:
        sock.close()

def check_SIP(ip, port):
    try:
        sip_options_msg = \
        'OPTIONS sip:{} SIP/2.0\r\n' \
        'Via: SIP/2.0/UDP {}:5060;branch=z9hG4bK-524287-1---0000000000000000\r\n' \
        'Max-Forwards: 70\r\n' \
        'Contact: <sip:{}>\r\n' \
        'To: <sip:{}>\r\n' \
        'From: anonymous<sip:anonymous@anonymous.invalid>;tag=0000000000000000\r\n' \
        'Call-ID: 00000000000000000000000000000000@anonymous.invalid\r\n' \
        'CSeq: 1 OPTIONS\r\n' \
        'Accept: application/sdp\r\n' \
        'Content-Length: 0\r\n\r\n'.format(ip, ip, ip, ip)
        # UDP 소켓 생성 및 SIP 서버로 메시지 전송
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        sock.sendto(sip_options_msg.encode(), (ip, port)) 
        data, addr = sock.recvfrom(4096) #최대로 받을 양 4096 바이트(버퍼크기)
        return True
        
    except Exception as e:
        return False
    finally:
        sock.close() #리소스 해제

def tcpBannerGrap(ip, port):
    try:
        # HTTP 소켓 통신시 오류 발생하므로 우선 체크 추후 변경
        httpCheck = http_banner_grabbing(ip,port)
        if httpCheck == "http:":
            return "http"
        elif httpCheck == "https":
            return "https"
        
        service = None
        
        # 서비스 체크
        if(checkMySQL(ip, port)):
            service = "mysql"
        elif(checkSSH(ip, port)):
            service = "ssh"
        elif(checkFTP(ip, port)):
            service = "ftp"
        elif(checkTelnet(ip, port)):
            service = 'telnet'
        elif(check_SMTP(ip, port)):
            service = 'smtp'
        elif(checkSMB(ip,port)):
            service = 'smb'
        return service
    
    except Exception as e:
        if "대상 컴퓨터에서 연결을 거부" in str(e):
            return "port close"
        return e



def main():
    services = []
    ip = "152.70.185.32"
    ports = [22,445,80,465]
    
    for port in ports:
        service = tcpBannerGrap(ip, port)
        services.append([port,service])
    
    print(services)
        
main()