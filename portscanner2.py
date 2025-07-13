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

def port_scan(target, start_port, end_port):
    open_ports = []
    print(f"\nScanning {target} from port {start_port} to {end_port}...")
    
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target, port))
                if result == 0:
                    print(f"✅ Port {port}: OPEN")
                    open_ports.append(port)
                else:
                    print(f"❌ Port {port}: Closed")
        except Exception as e:
            print(f"⚠️ Port {port}: Error ({str(e)})")
    
    return open_ports

def save_results(target, open_ports):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scan_results_{target}_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(f"Port Scan Results ({timestamp})\n")
        f.write("="*30 + "\n")
        f.write(f"Target: {target}\n")
        f.write(f"Open Ports: {', '.join(map(str, open_ports))}\n")
    
    print(f"\nResults saved to '{filename}'")

if __name__ == "__main__":
    print("=== Python Port Scanner ===")
    target = input("Enter target IP: ").strip()
    
    if not is_valid_ip(target):
        print("Error: Invalid IP address format!")
        exit()

    while True:
        port_input = input("Enter port or range (e.g. 80 or 79-81): ").strip()
        try:
            if '-' in port_input:
                start_port, end_port = map(int, port_input.split('-'))
            else:
                start_port = end_port = int(port_input)
            
            if 0 <= start_port <= end_port <= 65535:
                break
            print("Error: Ports must be 0-65535 and start <= end")
        except ValueError:
            print("Error: Invalid port format. Use numbers like '80' or '79-81'")

    open_ports = port_scan(target, start_port, end_port)
    save_results(target, open_ports)