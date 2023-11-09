import socket
import os
import struct
import time

# UDP 패킷 생성 함수
def create_udp_packet(target_ip, port, timeout=1):
    # UDP 헤더 생성
    header = struct.pack("HHHH", os.getpid() & 0xFFFF, 0, port, port)
    header += struct.pack("!I", timeout)
    # 데이터 부분 생성
    data = b""
    # 패킷 생성
    packet = header + data
    return packet

# UDP 패킷 전송 함수
def send_udp_packet(target_ip, port, timeout=1):
    try:
        # raw socket 생성
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        raise

    # UDP 패킷 전송
    print(f"UDP 패킷 전송: IP {target_ip}, 포트 {port}")
    my_socket.sendto(create_udp_packet(target_ip, port, timeout), (target_ip, port))

    # 타임아웃 설정
    my_socket.settimeout(timeout)

    # 응답 수신
    try:
        response = my_socket.recv(1024)
        print(f"응답 수신: {response}")
    except socket.timeout:
        # 응답이 없으면 포트가 열려 있는 것으로 판단
        print(f"포트 {port} 응답 없음")
        return True
    except ConnectionResetError:
        # 원격 호스트가 연결을 끊었을 경우, 포트가 닫혀 있는 것으로 판단
        print(f"포트 {port} 연결 끊김")
        return False
    else:
        # 응답이 있으면 포트가 닫혀 있는 것으로 판단
        print(f"포트 {port} 응답 있음")
        return False

# UDP 스캔 함수
def udp_scan(target_ip):
    # 타겟 호스트 대신 IP 주소를 직접 입력받도록 수정
    target_ip

    open_udp_port = []

    for port in range(52,54):  # 포트 수색 범위를 1900부터 2100까지로 한정
        print(f"포트 {port} 스캔 시작")
        # 둘다 보내서 둘다 포트가 열려있다라고 나오는 경우만 open_udp_port 배열에 추가
        try:
            if send_udp_packet(target_ip, port) and send_udp_packet(target_ip, port, timeout=5):
                open_udp_port.append(port)
        except Exception as e:
            print(f"포트 {port} 스캔 중 오류가 발생했습니다: {e}")

    return open_udp_port

