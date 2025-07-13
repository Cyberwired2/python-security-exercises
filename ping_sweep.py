import os 
import platform 
from datetime import datetime
import threading 
import queue
import re
import time
import ipaddress  # New import for safety checks

MAX_THREADS = 50  # Prevent network flooding

def ping_host(host, ping_cmd, result_queue):
    """Enhanced ping with better OS detection"""
    ttl_os_map = {
        (0, 64): "Linux/Unix",
        (65, 128): "Windows",
        (129, 254): "Network Device",
        (255, 256): "Solaris/AIX"
    }
    
    comm = f"{ping_cmd} {host}"
    try:
        response = os.popen(comm)
        data = response.read()
        response.close()

        ttl_match = re.search(r'ttl=(\d+)', data.lower())
        if ttl_match:
            ttl_value = int(ttl_match.group(1))
            os_guess = next((os_name for (min_ttl, max_ttl), os_name in ttl_os_map.items() 
                           if min_ttl <= ttl_value <= max_ttl), "Unknown")
            result_queue.put((host, os_guess, ttl_value))
    except Exception as e:
        print(f"Error pinging {host}: {str(e)}")

def validate_scan_range(net, start, end):
    """Safety check for private IP ranges only"""
    try:
        test_ip = f"{net}{start}"
        ip_obj = ipaddress.ip_address(test_ip)
        
        if ip_obj.is_loopback or ip_obj.is_private:
            return True
            
        print(f"❌ WARNING: {test_ip} is not in private IP range!")
        print("Only scan networks you own or have permission to scan")
        return False
    except ValueError:
        print("❌ Invalid IP address format")
        return False

def main():
    print("""
    NETWORK SCANNER TOOL
    --------------------
    WARNING: Only scan networks you own!
    Unauthorized scanning may violate laws.
    """)
    
    net = input("Enter Network Address (e.g., 192.168.1.0): ").strip()
    net_parts = net.split('.')
    
    if len(net_parts) != 4:
        print("❌ Invalid format. Use like: 192.168.1.0")
        return
    
    base_ip = '.'.join(net_parts[:3]) + '.'
    
    try:
        start = int(input("Start IP (last octet): "))
        end = int(input("End IP (last octet): "))
        
        if not (0 <= start <= 255 and 0 <= end <= 255):
            print("❌ IP octets must be 0-255")
            return
            
        if not validate_scan_range(base_ip, start, end):
            return
    except ValueError:
        print("❌ Invalid number input")
        return

    # Platform detection
    ping_cmd = "ping -n 1 " if platform.system() == "Windows" else "ping -c 1 "
    
    print(f"\nScanning {base_ip}{start} to {base_ip}{end}...")
    print("Press Ctrl+C to stop\n" + "-" * 40)
    
    result_queue = queue.Queue()
    threads = []
    t1 = datetime.now()
    
    try:
        for ip in range(start, end + 1):
            while threading.active_count() > MAX_THREADS:
                time.sleep(0.1)
                
            addr = f"{base_ip}{ip}"
            thread = threading.Thread(target=ping_host, args=(addr, ping_cmd, result_queue))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
        for thread in threads:
            thread.join(timeout=2)
            
    except KeyboardInterrupt:
        print("\nScan stopped by user!")
    
    # Process results
    live_hosts = []
    while not result_queue.empty():
        live_hosts.append(result_queue.get())
    live_hosts.sort(key=lambda x: tuple(map(int, x[0].split('.'))))
    
    # Display results
    print("\n" + "-" * 40)
    print(f"Scan completed in: {datetime.now() - t1}")
    print(f"Live hosts found: {len(live_hosts)}\n")
    
    if live_hosts:
        print("{:<15} {:<15} {}".format("IP", "OS Guess", "TTL"))
        print("-" * 40)
        for host, os_guess, ttl in live_hosts:
            print("{:<15} {:<15} {}".format(host, os_guess, ttl))
    else:
        print("No live hosts found")

if __name__ == "__main__":
    main()