import socket
import time 

startTime = time.time()


if __name__ == '__main__':
    target = input('Enter the host to be scanned: ')
    t_IP = socket.gethostbyname(target)
    print ('Starting scan on host: ', t_IP)

for i in range(50, 500):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((t_IP,i)) 

    if result == 0:
        print(f'Port {i}: OPEN')

    s.close()

print('Time taken:', time.time() - startTime)



