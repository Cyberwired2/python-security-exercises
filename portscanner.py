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
    if not is_valid_ip(target):
        print(f"Error: {target} is not a valid IPv4 address!")
        return

    open_ports = []
    print(f"\nScanning {target}...")
    
    for port in range(ports[0], ports[1] + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"✅ Port {port}: OPEN")
                open_ports.append(port)
            else:
                print(f"❌ Port {port}: Closed")
            s.close()
        except Exception as e:
            print(f"⚠️ Port {port}: Error ({str(e)})")

    # Save results to file
    save_results(target, open_ports)

def save_results(target, open_ports):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"scan_results_{target}.txt"
    
    with open(filename, "w") as file:
        file.write(f"Port Scan Results for {target}\n")
        file.write(f"Scan completed at: {timestamp}\n\n")
        file.write("PORT    STATUS\n")
        file.write("----    ------\n")
        for port in open_ports:
            file.write(f"{port:<8} OPEN\n")
        file.write("\n🔍 Scan summary: ")
        file.write(f"{len(open_ports)} open ports found.")

    print(f"\nResults saved to '{filename}'")

if __name__ == "__main__":
    target = input("Enter target IP: ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))
    port_scan(target, (start_port, end_port))