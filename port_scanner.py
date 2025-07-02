import socket
from datetime import datetime

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or (len(part) > 1 and part[0] == '0'):
            return False
        if not 0 <= int(part) <= 255:
            return False
    return True

def port_scan(target, ports):
    print(f"\nScanning {target}...")
    for port in range(ports[0], ports[1] + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target, port))
                if result == 0:
                    print(f"✅ Port {port}: OPEN")
                else:
                    print(f"❌ Port {port}: Closed")
        except Exception as e:
            print(f"⚠️ Port {port}: Error ({str(e)})")

if __name__ == "__main__":
    target = input("Enter target IP: ")
    if not is_valid_ip(target):
        print("Invalid IP address!")
        exit()
    
    port_input = input("Enter port range (e.g. 80-100): ")
    if '-' in port_input:
        start, end = map(int, port_input.split('-'))
    else:
        start = end = int(port_input)
    
    port_scan(target, (start, end))