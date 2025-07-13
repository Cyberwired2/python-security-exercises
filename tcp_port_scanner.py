import socket
from datetime import datetime

target_ip = input("Enter the target IP address: ").strip()


start_port = int(input("Enter the starting port number: "))
end_port = int(input("Enter the ending port number: "))

start_time = datetime.now()

print(f"\nScanning {target_ip} from port {start_port} to {end_port} ... \n")

for port in range(start_port, end_port + 1):

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) 

        result = s.connect_ex((target_ip, port))

        if result == 0:

            print(f"Port {port} is OPEN")

        s.close()


    except KeyboardInterrupt:
         print("\nScan stopped by user.")
         break

    except socket.error:
         print("\nCould not connect to server.")
         break

end_time = datetime.now()
total_time = end_time - start_time

print(f"\nScan completed in {total_time}\n")