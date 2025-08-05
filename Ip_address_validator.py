import os 
import platform 
from datetime import datetime
import threading 
import queue
import re

def ping_host(host, ping_cmd, result_queue):
    """Ping a single host, extract TTL, and guess OS."""
    comm = ping_cmd + host
    response = os.popen(comm)
    data = response.read()
    response.close()

    ttl_match = re.search(r'ttl=(\d+)', data.lower())

    if ttl_match:
        ttl_value = int(ttl_match.group(1))


        if ttl_value <= 64:
            os_guess = "Linux/Unix"
        elif ttl_value <= 128:
            os_guess = "Windows"
        else:
            os_guess = "Networking Device"
        

        result_queue.put((host, os_guess, ttl_value))

def main():
    net = input("Enter the Network Address (e.g., 192.168.1.0): ").strip()
    net_parts = net.split('.')

    if len(net_parts) != 4:
        print("❌ Invalid network format. Please enter like: 192.168.1.0")
        return
    

    base_ip = net_parts[0] + '.' + net_parts[1] + '.' + net_parts[2] + '.'


    start = int(input("Enter the Starting Number: "))
    end = int(input("Enter the Last Number: "))

    oper = platform.system()
    if oper == "Windows":
        ping_cmd = "ping -n 1 "
    else:
        ping_cmd = "ping -c 1"

    t1 = datetime.now()
    print("nScanning in Progress...\n" + "-" * 40) 

    result_queue = queue.Queue()
    threads = []

    for ip in range(start, end + 1):
        addr = base_ip + str(ip)
        command = ping_cmd + addr

        print(f"\nDebug Info:")
        print(f"Base IP: {base_ip}")
        print(f"Current IP: {ip}")
        print(f"Target IP: {addr}")
        print(f"Full Command: {command}\n")

        thread = threading.Thread(target=ping_host, args=(addr, ping_cmd, result_queue))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()


    live_hosts = []
    while not result_queue.empty():
       live_hosts.append(result_queue.get())

    live_hosts.sort(key=lambda x: int(x[0].split('.')[-1]))


    t2 =datetime.now()
    total = t2 - t1


    print("\n" + "-" * 40)
    print(f"Scan completed in: {total}")
    print(f"Found {len(live_hosts)} live hosts\n")


    if live_hosts:
        print("Live Host Detected:")
        for host, os_guess, ttl in live_hosts:
            print(f"  {host} --> {os_guess} (TTL={ttl}) --> Live")


if __name__ == "__main__":
    main()
