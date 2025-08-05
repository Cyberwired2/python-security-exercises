import ipaddress

ip = "192.168.56.101"
common_subnet_lengths = [24, 16, 8]  # Most common

print(f"Testing IP: {ip}")
print("=" * 50)

for subnet_len in common_subnet_lengths:
    network = ipaddress.IPv4Network(f"{ip}/{subnet_len}", strict=False)
    hosts = list(network.hosts())
    
    print(f"If subnet is /{subnet_len}:")
    print(f"  Network: {network}")
    print(f"  Subnet Mask: {network.netmask}")
    print(f"  Network Address: {network.network_address}")
    print(f"  Broadcast: {network.broadcast_address}")
    print(f"  Host Range: {hosts[0]} - {hosts[-1]}")
    print(f"  Total Hosts: {len(hosts)}")
    print()