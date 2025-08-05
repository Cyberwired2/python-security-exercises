from scapy.all import IP, TCP, sr1, conf
import time
import ipaddress

# Suppress verbose output
conf.verb = 0

def is_valid_ip(ip_string):
    """Check if the entered IP address is valid"""
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def scan_port(ip, port):
    """Scan a single port to check if it's open"""
    # Send SYN packet
    syn_packet = IP(dst=ip)/TCP(dport=port, flags="S")
    # Wait for a response
    response = sr1(syn_packet, timeout=1)
    
    # Analyze the response
    if response is None:
        return False  # No response, port is filtered or closed
    elif response.haslayer(TCP):
        if response[TCP].flags == 0x12:  # SYN-ACK flags (0x12)
            return True  # Port is open
    return False  # Port is closed

def scan_ports(target, port_range):
    """Scan multiple ports on a target"""
    print(f"\nScanning {target} for open ports...\n")
    open_ports = []
    
    start_time = time.time()
    
    for port in port_range:
        print(f"Scanning port {port}...", end="")
        if scan_port(target, port):
            print(" Open!")
            open_ports.append(port)
        else:
            print(" Closed/Filtered")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nScan completed in {duration:.2f} seconds")
    
    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f"- Port {port}")
    else:
        print("\nNo open ports found in the specified range.")
    
    return open_ports

def get_target_ip():
    """Get IP address from user with validation"""
    while True:
        target_ip = input("Enter the IP address to scan: ").strip()
        
        if target_ip.lower() == 'localhost':
            target_ip = '127.0.0.1'
            print(f"Using localhost: {target_ip}")
            return target_ip
        
        if is_valid_ip(target_ip):
            return target_ip
        else:
            print("Invalid IP address format. Please try again.")
            print("Examples: 192.168.1.1, 127.0.0.1, or type 'localhost'")

def get_scan_type():
    """Let user choose between quick scan or custom ports"""
    print("\nChoose scan type:")
    print("1. Quick scan (common ports)")
    print("2. Custom port range")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            # Common ports
            return [21, 22, 23, 25, 53, 80, 135, 139, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        elif choice == '2':
            return get_custom_ports()
        else:
            print("Please enter 1 or 2")

def get_custom_ports():
    """Get custom port range from user"""
    while True:
        try:
            port_input = input("Enter ports (e.g., '80,443,22' or '1-100'): ").strip()
            
            if '-' in port_input:
                # Range format like "1-100"
                start, end = port_input.split('-')
                start_port = int(start.strip())
                end_port = int(end.strip())
                
                if start_port > end_port or start_port < 1 or end_port > 65535:
                    raise ValueError("Invalid port range")
                
                return list(range(start_port, end_port + 1))
            
            elif ',' in port_input:
                # Comma-separated format like "80,443,22"
                ports = [int(port.strip()) for port in port_input.split(',')]
                
                for port in ports:
                    if port < 1 or port > 65535:
                        raise ValueError(f"Port {port} is out of valid range (1-65535)")
                
                return ports
            
            else:
                # Single port
                port = int(port_input)
                if port < 1 or port > 65535:
                    raise ValueError("Port out of valid range")
                return [port]
                
        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Examples: '80,443,22' or '1-100' or '80'")

if __name__ == "__main__":
    print("=== Interactive Port Scanner ===")
    print("WARNING: Only scan networks and systems you own or have permission to scan!")
    
    # Get target IP from user
    target_ip = get_target_ip()
    
    # Get ports to scan
    ports_to_scan = get_scan_type()
    
    # Confirm before scanning
    print(f"\nTarget: {target_ip}")
    print(f"Ports to scan: {len(ports_to_scan)} ports")
    
    confirm = input("Proceed with scan? (y/n): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        # Perform the scan
        scan_ports(target_ip, ports_to_scan)
    else:
        print("Scan cancelled.")
    
    print("\nScan complete. Remember to only scan systems you own!")