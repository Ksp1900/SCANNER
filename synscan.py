from scapy.layers.inet import ICMP, IP, TCP, sr1
import socket
from datetime import datetime

start = datetime.now()

def icmp_probe(ip):
    icmp_packet = IP(dst=ip) / ICMP()
    resp_packet = sr1(icmp_packet, timeout=10)
    return resp_packet is not None

def syn_scan(ip, ports):
    for port in ports:
        syn_packet = IP(dst=ip) / TCP(dport=port, flags='S')
        resp_packet = sr1(syn_packet, timeout=10)
        if resp_packet is not None:
            if resp_packet.haslayer(TCP) and (resp_packet[TCP].flags & 0x12 == 0x12):
                print(f'{ip}:{port} is open/{resp_packet.sport}')
            else:
                print(f'{ip}:{port} is closed')
        else:
            print(f'{ip}:{port} is filtered or no response')

ends = datetime.now()

if __name__ == '__main__':
    name = input('Hostname / IP: ')
    ip = socket.gethostbyname(name)
    ports = [20, 21, 22, 23, 25, 43, 53, 80, 2023, 2024]

try:
    if icmp_probe(ip):
        syn_scan(ip, ports)
    else:
        print('Failed to send ICMP packet')
except Exception as e:
    print('Scan completed!')
    print(f'Time: {ends - start}')