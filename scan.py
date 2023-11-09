import udpscan
import synscan
import servicescan

print("\
███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ \n\
██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗\n\
███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝\n\
╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗\n\
███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║\n\
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝\n")
print("1.(TCP_SYN SCAN) 2.(UDP SCAN)\n")
while True:  
    num = input(">>")
    if num == "1" or num == "2":
        break
    else:
        print("please type 1 or 2")


ip = input("IP : ")
    

while True:
    if num == "1": # TCP_SYN 스캔
        tcp_ports = synscan.scan(ip)
        tcp_services = servicescan.serviceScan(ip,tcp_ports)
        for tcp_service in tcp_services:
            print(f"PORT : {tcp_service[0]} SERVICE : {tcp_service[1]}\n")
        break
    # if num == "2" : # UDP 스캔
    #     udp_ports = udpscan.udp_scan(ip)
    #     udp_services = ServiceScan.serviceScan(ip,udp_ports)
    #     for udp_service in udp_services:
    #         print(f"PORT : {udp_service[0]} SERVICE : {udp_service[1]}")
    #     break