import socket
import pymysql

ip = "127.0.0.1"   
port = 3306
check_list = [b'caching_sha2', b'mysql'] # 체크리스트

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.settimeout(2)
banner = s.recv(1024)
pack = banner[4:] # packet Length, Number 제외
code = int(pack[0]) # 일반적인 경우 0xA Block된 경우 0xFF

for check in check_list:
    if check in banner:
        if(code == 255):
            print("blocked")
            break
        else:
            pack = str(pack)
            pack = pack[4:pack.find("\\x00")] # Version 추출
            print(pack)
            break


# s.send(request.encode())
# print(s.recv(1024))

# s.close()