import ipaddress

def ip_to_cidr():
    ip = input("Enter IP address (e.g., 192.168.1.1): ")
    subnet_mask = input("Enter subnet mask (e.g., 255.255.255.0): ")
    
    try:
        # Combine IP and subnet mask into network
        network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
        print(f"\nCIDR Notation: {network.with_netmask}")
        print(f"CIDR Format: {network.with_prefixlen}")
        print(f"Network Address: {network.network_address}")
        print(f"Broadcast Address: {network.broadcast_address}")
        print(f"Usable Host Range: {network.network_address + 1} - {network.broadcast_address - 1}")
        print(f"Total Usable Hosts: {network.num_addresses - 2}")
    except ValueError as e:
        print(f"Error: {e}")

def check_same_subnet():
    ip1 = input("Enter first IP address: ")
    ip2 = input("Enter second IP address: ")
    subnet_mask = input("Enter subnet mask: ")
    
    try:
        network = ipaddress.IPv4Network(f"{ip1}/{subnet_mask}", strict=False)
        ip2_obj = ipaddress.IPv4Address(ip2)
        
        if ip2_obj in network:
            print(f"\n{ip1} and {ip2} are in the same subnet ({network})")
        else:
            print(f"\n{ip1} and {ip2} are NOT in the same subnet")
    except ValueError as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\nIP Subnet Calculator")
        print("1. Convert IP/Subnet to CIDR and show network info")
        print("2. Check if two IPs are in the same subnet")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            ip_to_cidr()
        elif choice == '2':
            check_same_subnet()
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again")

if __name__ == "__main__":
    main()