from scapy.all import *
from scapy.layers.inet import ICMP, IP, TCP, sr1, UDP

target_ip = "192.168.229.131"  # 대상 IP 주소를 설정합니다
ports = [53, 11]  # 스캔할 포트 리스트입니다

# UDP 포트 스캔 함수
def udp_scan(ip, port_list):
    # 스캔 결과를 저장할 리스트
    open_ports = []

    # 포트 리스트를 반복하면서 스캔 실행
    for port in port_list:
        # UDP 패킷 생성 (IP/UDP 레이어)
        udp_packet = IP(dst=ip)/UDP(dport=port)
        # 패킷 전송 및 응답 수신
        response = sr1(udp_packet, timeout=1, verbose=0)
        
        # 응답 패킷이 없거나 ICMP Port Unreachable 에러를 수신했을 경우
        if response is None:
            open_ports.append(port)  # 응답이 없는 포트는 열려있을 가능성이 있습니다
        elif response.haslayer(ICMP):
            if int(response.getlayer(ICMP).type) == 3 and int(response.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                print(str(int(response.getlayer(ICMP).type)))
                # ICMP Type 3(Code 1,2,3,9,10,13)은 Port Unreachable을 의미합니다 (즉, 포트가 닫혀있습니다)
                pass

    return open_ports

# 스캔 실행
open_ports = udp_scan(target_ip, ports)

# 결과 출력
print(f"Open or filtered UDP ports on {target_ip}: {open_ports}")