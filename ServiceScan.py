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

def checkMySQL(banner):
    if b"mysql" in banner:
        return True
    else:
        return False
    
def checkSSH(banner):
    if b"SSH" in banner:
        return True
    else:
        return False

def checkFTP(banner):
    if (b"FTP" in banner) or ("FileZilla".encode() in banner):
        return True
    else:
        return False
    
def checkTelnet(banner):
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
        
        # 소켓 생성 및 연결
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 방식
        s.connect((ip, port))
        s.settimeout(5)
        # 서버 응답
        banner = s.recv(1024)
        service = banner
        note = banner
        
        if(checkMySQL(banner)):
            service = "mysql"
        elif(checkSSH(banner)):
            service = "ssh"
        elif(checkFTP(banner)):
            service = "ftp"
        elif(checkTelnet(banner)):
            service = 'telnet'
        
        s.close()
        return service, note
    
    except Exception as e:
        if "대상 컴퓨터에서 연결을 거부" in str(e):
            return "port close", None
        return e, None



def main():
    services = []
    ip = "192.168.56.101"
    ports = [23]
    note = ""
    
    for port in ports:
        service, note = tcpBannerGrap(ip, port)
        services.append([port, service, note]) # 포트, 서비스, 버전을 비롯한 추가 내용
    
    print(services)
        
main()