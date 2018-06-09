import logging
import socket
import sys
import time
import threading
from util import *

logger = logging.getLogger()

def listen(sock):
    print ("Starting listening...")
    while True:
        data, addr = sock.recvfrom(1024)
        print('RECEIVED: {}'.format(addr))

def main(host='45.77.74.113', port=9999):
    print('connecting: {}:{}'.format(host, port))
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(b'0', (host, port))

    while True:
        data, addr = sock.recvfrom(1024)
        print('client received: {} {}'.format(addr, data))
        addr = msg_to_addr(data)
        attempts = 1
        threading.Thread(target = listen, args = (sock,)).start()
        while attempts < 10:
            print('{} - Sending: {}'.format(attempts, addr))
            sock.sendto(b'0', addr)
            time.sleep(1)
            attempts+=1
        data, addr = sock.recvfrom(1024)
        print('client received: {} {}'.format(addr, data))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
