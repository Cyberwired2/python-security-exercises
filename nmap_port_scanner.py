import nmap

scanner = nmap.PortScanner()

ip_addr = input("Enter the IP address to scan: ")
print("The IP you entered is: ", ip_addr)

scan_type = input("""\nSelect scan type:
                1) SYN ACK Scan
                2) UDP Scan
                3) Comprehensive Scan
                Enter your choice: """)

if scan_type == '1':
    print("Performing SYN ACK scan...")
    scanner.scan(ip_addr, '1-1024', '-v -sS')
elif scan_type == '2':
    print("Performing UDP scan...")
    scanner.scan(ip_addr, '1-1024', '-v -sU')
elif scan_type == '3':
    print("Performing comprehensive scan...")
    scanner.scan(ip_addr, '1-1024', '-v -sS -sV -sC -A -O')
else:
    print("Invalid option")

print("Command executed:", scanner.command_line())
print("Scan info:", scanner.scaninfo())

if scanner.all_hosts():
    print("Host is up:", scanner[ip_addr].state())
    print("Open ports:", scanner[ip_addr]['tcp'].keys())