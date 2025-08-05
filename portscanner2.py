import socket
from datetime import datetime

def get_valid_input(prompt, input_type=int, min_val=0, max_val=65535):
    """Safely get and validate user input"""
    while True:
        try:
            value = input_type(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Error: Must be between {min_val}-{max_val}")
        except ValueError:
            print("Invalid input. Please enter a number")

def scan_port(ip, port, timeout=1):
    """Check if a single port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except:
        return False

def main():
    print("\n" + "="*50)
    print("=== INTERACTIVE PORT RANGE SCANNER ===")
    print("="*50 + "\n")
    
    # Get user inputs
    target = input("Enter target IP: ").strip()
    start_port = get_valid_input("Start port (0-65535): ")
    end_port = get_valid_input(f"End port ({start_port}-65535): ", min_val=start_port)
    timeout = get_valid_input("Timeout per port (seconds, 1-5): ", min_val=1, max_val=5)
    
    # Scan
    print(f"\nScanning {target} (ports {start_port}-{end_port})...")
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        if scan_port(target, port, timeout):
            print(f"✅ Port {port}: OPEN")
            open_ports.append(port)
        else:
            print(f"❌ Port {port}: Closed", end='\r')  # Overwrite line
    
    # Results
    print("\n\n=== RESULTS ===")
    print(f"Open ports on {target}: {open_ports or 'None'}")
    print(f"Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()