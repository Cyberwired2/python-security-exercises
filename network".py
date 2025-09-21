# STEP 1: The Most Basic Port Scanner
# Let's start with checking if ONE port is open

import socket

# What is a socket? Think of it like a phone line
# We use it to "call" another computer and see if anyone answers

def check_one_port():
    """Check if port 80 (web server) is open on Google"""
    
    # Create a socket (like picking up the phone)
    sock = socket.socket()
    
    # Set a timeout (don't wait forever for an answer)
    sock.settimeout(3)
    
    try:
        # Try to connect to google.com on port 80
        # This is like dialing a phone number
        result = sock.connect(("https://mpulse.mtn.ng/", 80))
        print("Port 80 is OPEN on google.com")
        
    except:
        # If connection fails, the port is closed or filtered
        print("Port 80 is CLOSED or FILTERED on google.com")
    
    finally:
        # Always close the socket (hang up the phone)
        sock.close()

# Test this basic function
print("=== STEP 1: Testing one port ===")
check_one_port()

# ================================================================

# STEP 2: Check Multiple Ports (One at a time)
# Now let's check several ports in a row

def check_multiple_ports():
    """Check several common ports on a target"""
    
    target = "google.com"  # The computer we want to scan
    ports = [80, 443, 22, 21, 25]  # List of ports to check
    
    print(f"\n=== STEP 2: Checking multiple ports on {target} ===")
    
    for port in ports:  # Go through each port one by one
        
        # Create a new socket for each port
        sock = socket.socket()
        sock.settimeout(2)
        
        try:
            # Try to connect
            result = sock.connect((target, port))
            print(f"Port {port} is OPEN")
            
        except:
            print(f"Port {port} is CLOSED")
            
        finally:
            sock.close()

# Test this function
check_multiple_ports()

# ================================================================

# STEP 3: Make it into a Function we can reuse
# Let's organize our code better

def scan_ports(target, port_list):
    """
    Scan a list of ports on a target
    
    target: the website or IP address to scan
    port_list: a list of port numbers like [80, 443, 22]
    """
    
    print(f"\n=== STEP 3: Scanning {target} ===")
    open_ports = []  # Empty list to store open ports
    
    for port in port_list:
        sock = socket.socket()
        sock.settimeout(2)
        
        try:
            sock.connect((target, port))
            print(f"✓ Port {port} is OPEN")
            open_ports.append(port)  # Add to our list
            
        except:
            print(f"✗ Port {port} is CLOSED")
            
        sock.close()
    
    return open_ports  # Give back the list of open ports

# Test our reusable function
common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
open_ports = scan_ports("google.com", common_ports)
print(f"Summary: Found {len(open_ports)} open ports: {open_ports}")

# ================================================================

# STEP 4: Add Port Information
# Let's make our scanner more informative

def get_service_name(port):
    """Tell us what service usually runs on this port"""
    
    services = {
        21: "FTP (File Transfer)",
        22: "SSH (Secure Shell)", 
        23: "Telnet",
        25: "SMTP (Email)",
        53: "DNS (Domain Names)",
        80: "HTTP (Web Server)",
        110: "POP3 (Email)",
        143: "IMAP (Email)",
        443: "HTTPS (Secure Web)",
        993: "IMAPS (Secure Email)",
        995: "POP3S (Secure Email)"
    }
    
    return services.get(port, "Unknown Service")

def enhanced_scan(target, port_list):
    """Enhanced scanner with service information"""
    
    print(f"\n=== STEP 4: Enhanced scan of {target} ===")
    print(f"{'Port':<6} {'Status':<8} {'Service'}")
    print("-" * 40)
    
    for port in port_list:
        sock = socket.socket()
        sock.settimeout(2)
        
        try:
            sock.connect((target, port))
            status = "OPEN"
            service = get_service_name(port)
            print(f"{port:<6} {status:<8} {service}")
            
        except:
            status = "CLOSED"
            print(f"{port:<6} {status:<8} ---")
            
        sock.close()

# Test our enhanced scanner
test_ports = [21, 22, 80, 443, 3389]
enhanced_scan("google.com", test_ports)

# ================================================================

# STEP 5: User Input Version
# Let's make it interactive

def interactive_scanner():
    """Let the user choose what to scan"""
    
    print("\n=== STEP 5: Interactive Scanner ===")
    
    # Get target from user
    target = input("Enter target (like google.com or 192.168.1.1): ")
    
    # Get ports from user
    print("Enter ports to scan:")
    print("Examples: 80  or  80,443,22  or  1-100")
    port_input = input("Ports: ")
    
    # Parse the port input
    if '-' in port_input:
        # Handle range like "1-100"
        start, end = port_input.split('-')
        ports = list(range(int(start), int(end) + 1))
    elif ',' in port_input:
        # Handle list like "80,443,22"
        ports = [int(p.strip()) for p in port_input.split(',')]
    else:
        # Handle single port like "80"
        ports = [int(port_input)]
    
    # Run the scan
    print(f"\nScanning {len(ports)} ports on {target}...")
    enhanced_scan(target, ports)

# Uncomment the line below to run the interactive version
# interactive_scanner()

print("\n" + "="*50)
print("EXPLANATION OF WHAT EACH STEP DOES:")
print("="*50)
print("Step 1: Checks if ONE specific port is open")
print("Step 2: Checks MULTIPLE ports one by one") 
print("Step 3: Organizes code into reusable functions")
print("Step 4: Adds information about what each port is for")
print("Step 5: Lets user choose target and ports interactively")
print("\nTo run interactive version, uncomment the last line!")