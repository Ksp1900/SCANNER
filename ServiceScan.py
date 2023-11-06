import socket
import requests
import smtplib
import paramiko
import ssl
import sys


# 변경점
# 1 : HTTP 배너그래빙의 기능을 변경하여 HTTP와 HTTPS 구별 기능 추가
#TEST

def http_banner_grabbing(target_host, target_port): # 변수 설정 대로 대입하는 과정
    try:
        target_url = f"http://{target_host}:{target_port}" #f 는 변수에 따라 달라지는 문자열을 반영하기 위한 함수
        response = requests.get(target_url, timeout=5) #HTTP 요청을 받는 함수
        return response.url[0:5] # http: or https 리턴
    except Exception as e:
        return False

def checkMySQL(ip, port):
    # 소켓 생성 및 연결
    check_list = [b'caching_sha2', b'mysql'] # 체크리스트

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
                ver = packet[4:packet.find("\\x00")] # Version 추출 필요할 경우 version 까지 리턴
                return True
            else:
                a = open("checkLog.txt",'a') #문자열은 매칭하나 추가 검증 실패시 로그
                a.write(f"{ip} : {port} : {banner}\n")
                return False
    
    return False
    
def checkSSH(ip, port):
    # 소켓 생성 및 연결
    banner = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 방식
        s.settimeout(5)
        s.connect((ip, port))
        # 서버 응답
        banner = s.recv(1024).decode(errors='ignore')
        s.close()
        if "SSH" in banner:
            print(f"Port {port}: 소켓에 배너가 확인 되었습니다.: {banner}")
            return True
    except (socket.timeout, socket.error):
        print(f"Port{port}에서 SSH 배너를 확인하지 못했습니다. paramiko로 더 정교하게 스캔하겠습니다.")

    if not banner:
        try:
            transport = paramiko.Transport((ip, port))
            transport.start_client()
            paramiko_banner = transport.remote_version
            transport.close()

            if paramiko_banner:
                print(f"Port{port}:에서 SSH 배너를 확인했습니다. 파라미코 :{paramiko_banner}")
            else:
                print(f"Port {port}:에서 SSH 배너를 확인하지 못했습니다.")
                return False
        except paramiko.SSHException as e:
            print(f"Port {port}: SSH 에러: {str(e)}")
            return False
        except Exception as e:
            print(f"Port {port}: 연결중 에러가 발생했습니다.: {str(e)}")
            return False
        
    else:
        return False

def checkFTP(ip, port):
    # 소켓 생성 및 연결
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 방식
    s.connect((ip, port))
    s.settimeout(2)
    # 서버 응답
    banner = s.recv(1024)
    
    if (b"FTP" in banner) or ("FileZilla".encode() in banner):
        return True
    else:
        return False
    
def checkTelnet(ip, port):
    # 소켓 생성 및 연결
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 방식
    s.connect((ip, port))
    s.settimeout(8)
    # 서버 응답
    banner = s.recv(1024)
    if(b"\xff\xfd\x18\xff\xfd \xff\xfd#\xff\xfd" in banner): # telnet 서버측에서 연결을 위해 보내는 응답
        return True
    else:
        return False

def check_SMTP(ip, port):
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
    

def tcpBannerGrap(ip, port):
    try:
        # HTTP 소켓 통신시 오류 발생하므로 우선 체크 추후 변경
        httpCheck = http_banner_grabbing(ip,port)
        if httpCheck == "http:":
            return "http"
        elif httpCheck == "https":
            return "https"
        
        service = None
        
        if(checkMySQL(ip, port)):
            service = "mysql"
            print(f"{ip} : {port} : {service}")
        elif(checkSSH(ip, port)):
            service = "ssh"
            print(f"{ip} : {port} : {service}")
        elif(checkFTP(ip, port)):
            service = "ftp"
            print(f"{ip} : {port} : {service}")
        elif(checkTelnet(ip, port)):
            service = 'telnet'
            print(f"{ip} : {port} : {service}")
        elif(check_SMTP(ip, port)):
            service = 'smtp'
            print(f"{ip} : {port} : {service}")
        
        return service
    
    except Exception as e:
        if "대상 컴퓨터에서 연결을 거부" in str(e):
            return "port close"
        return e



def main():
    services = []
    ip = "192.168.56.101"
    ports = [21,22,23,80,443,3306,2023]
    
    for port in ports:
        service = tcpBannerGrap(ip, port)
        services.append([port,service])
    
    print(services)
        
main()