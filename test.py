import socket
import requests #HTTP를 위한.. 함수..

def check_http(ip, port):
    try:
        response = requests.get(f"http://{ip}:{port}", timeout=3)
        return True, f"HTTP {response.status_code}"
    except requests.RequestException:
        return False, "Not HTTP"

def grab_banner(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=5) as s:
            banner = s.recv(1024).decode(errors='ignore')
            return True, banner
    except socket.error:
        return False, "Connection refused or timed out"

def read_tested_ports(file_path):
    with open(file_path, 'r') as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]


def main():
    ip = "192.168.56.101"
    open_ports = [21,22,23,80,443]
    print(f"Open ports: {open_ports}")
    
    for port in open_ports:
        is_http, http_result = check_http(ip, port)
        if is_http:
            print(f"Port {port}: {http_result}")
        else:
            is_service, banner_result = grab_banner(ip, port)
            if is_service:
                print(f"Port {port}: {banner_result}")
            else:
                print(f"Port {port}: {banner_result}")

if __name__ == "__main__":
    main()