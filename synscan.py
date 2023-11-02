from scapy.layers.inet import ICMP, IP, TCP, sr1
import socket
from datetime import datetime



def icmp_probe(ip):
    icmp_packet = IP(dst=ip) / ICMP()
    resp_packet = sr1(icmp_packet, timeout=10)
    return resp_packet is not None

def syn_scan(ip, ports):
    for port in ports:
        syn_packet = IP(dst=ip) / TCP(dport=port, flags='S')
        resp_packet = sr1(syn_packet, timeout=10)
        if resp_packet is not None:
            if resp_packet.getlayer('TCP').flags & 0x12 != 0:
                print(f'{ip}:{port} is open/{resp_packet.sprintf("%TCP.sport%")}')


if __name__ == '__main__':
    start = datetime.now()
    ends = datetime.now()
    name = input('Hostname / IP: ')
    ip = socket.gethostbyname(name)
    ports = [i for i in range(65535)]
    try:
        if icmp_probe(ip):
            syn_ack_packet = syn_scan(ip, ports)
            syn_ack_packet.show()
        else:
            print('Failed to send ICMP packet')
    except AttributeError:
        print('Scan completed!')
        print('<Time:{}>'.format(ends - start))