import socket
import requests

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 방식
    s.connect((ip, port))
    s.settimeout(2)
    # 서버 응답
    banner = s.recv(1024)
    
    if b"SSH" in banner:
        return True
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
    s.settimeout(5)
    # 서버 응답
    banner = s.recv(1024)
    if(b"\xff\xfd\x18\xff\xfd \xff\xfd#\xff\xfd" in banner): # telnet 서버측에서 연결을 위해 보내는 응답
        return True
    else:
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
        
        return service
    
    except Exception as e:
        if "대상 컴퓨터에서 연결을 거부" in str(e):
            return "port close"
        return e



def main():
    services = []
    ip = "127.0.0.1"
    ports = [21,22,23,80,443,3306]
    
    for port in ports:
        service = tcpBannerGrap(ip, port)
        services.append([port,service])
    
    print(services)
        
main()