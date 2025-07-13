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

def check_service(port):
    common_services = {
        21: "FTP",
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        8000: "HTTP-Alt",
        8080: "HTTP-Alt"
    }
    return common_services.get(port, "Unknown")

def port_scan(target, start_port, end_port):
    open_ports = []
    print(f"\nScanning {target}...")
    
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target, port))
                if result == 0:
                    service = check_service(port)
                    print(f"✅ Port {port}: OPEN ({service})")
                    open_ports.append(port)
                else:
                    print(f"❌ Port {port}: Closed")
        except Exception as e:
            print(f"⚠️ Port {port}: Error ({str(e)})")
    
    return open_ports

def suggest_test_ports():
    print("\nSuggested test ports (start a service first):")
    print("8000 - Python HTTP server (run: python -m http.server 8000)")
    print("8080 - Common alternative HTTP port")
    print("9000 - Test port for custom apps")

if __name__ == "__main__":
    print("=== Enhanced Port Scanner ===")
    target = input("Enter target IP [127.0.0.1]: ").strip() or "127.0.0.1"
    
    if not is_valid_ip(target):
        print("Error: Invalid IP address!")
        exit()

    suggest_test_ports()
    
    while True:
        port_input = input("\nEnter port/range (e.g. 80 or 79-81): ").strip()
        try:
            if '-' in port_input:
                start_port, end_port = map(int, port_input.split('-'))
            else:
                start_port = end_port = int(port_input)
            
            if 0 <= start_port <= end_port <= 65535:
                break
            print("Error: Ports must be 0-65535")
        except ValueError:
            print("Error: Use numbers like '80' or '79-81'")

    open_ports = port_scan(target, start_port, end_port)
    
    if target == "127.0.0.1" and not open_ports:
        print("\nTip: No open ports found. Did you start a test service?")
        print("Try these in another terminal:")
        print("  python -m http.server 8000")
        print("  nc -lvnp 8080")