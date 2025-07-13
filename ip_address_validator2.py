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

def port_scan(target, port_range):
    open_ports = []  # Stores open ports
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\nScan started at: {timestamp}")
    print(f"Scanning {target}...\n")
    
    for port in range(port_range[0], port_range[1] + 1):
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
    
    save_results(target, open_ports, timestamp)

def save_results(target, open_ports, timestamp):
    filename = f"portscan_{target.replace('.', '_')}.txt"
    with open(filename, "w") as file:
        file.write(f"Port Scan Results\n{'=' * 20}\n")
        file.write(f"Target: {target}\n")
        file.write(f"Time: {timestamp}\n\n")
        file.write("OPEN PORTS:\n")
        for port in open_ports:
            file.write(f"- {port}\n")
        file.write(f"\nTotal: {len(open_ports)} open ports.")
    
    print(f"\nResults saved to '{filename}'")

if __name__ == "__main__":
    target = input("Enter target IP: ")
    if not is_valid_ip(target):
        print("Error: Invalid IP address!")
        exit()
    
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))
    port_scan(target, (start_port, end_port))