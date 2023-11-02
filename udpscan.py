import socket

# UDP 스캔 함수
def udp_scan(ip):
    open_ports_udp = []
    # 포트 목록을 순회하며 UDP 스캔 수행
    for port in range(68, 70):
        try:
            # UDP 소켓을 생성하고 타임아웃을 설정합니다.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)

            # 빈 UDP 패킷을 보냅니다.
            s.sendto(b'', (ip, port))

            # 1초 동안 응답을 기다립니다.
            try:
                data, _ = s.recvfrom(1024)
                if data:
                    # 응답이 있으면 해당 포트가 열려 있습니다.
                    open_ports_udp.append(port)
            except socket.timeout:
                # 1초 동안 응답이 없으면 해당 포트가 닫혀 있습니다.
                pass

            s.close()
        except Exception as e:
            # 예외가 발생하면 해당 포트 스캔을 실패로 간주합니다.
            print(f"UDP 포트 {port} 스캔 중 오류 발생: {e}")

    # 열린 UDP 포트 목록을 반환합니다.
    return open_ports_udp

# 메인 함수
def main():
    # 대상 IP 주소를 입력받습니다.
    target_ip = input("대상 IP 주소를 입력하세요: ")

    # UDP 스캔을 수행합니다.
    open_ports_udp = udp_scan(target_ip)

    # 열린 UDP 포트 목록을 배열로 출력합니다.
    for port in open_ports_udp:
        print(f"open_ports_udp: {port}")

if __name__ == "__main__":
    main()