import logging
import socket
import sys
import time
import threading
from util import *
import subprocess

logger = logging.getLogger()
core_file = '/home/$USER/.var/app/org.libretro.RetroArch/config/retroarch/cores/snes9x_libretro.so'
rom_file = '~/Downloads/sf2.zip'
cmd_host = 'org.libretro.RetroArch --host --port={} -L {} {}'
cmd_client = 'org.libretro.RetroArch --connect={} --port={} -L {} {}'

def listen(sock, player):
    print ("Starting listening...")
    while True:
        data, addr = sock.recvfrom(1024)
        print('RECEIVED: {}'.format(addr))
        # player_addr = msg_to_addr_player(data)

        if player == '2':
            logger.info("Starting as host... port: %s", sock.getsockname()[1])
            cmd = cmd_host.format(sock.getsockname()[1], core_file, rom_file)
            logger.info("Running: {}".format(cmd))
            p = subprocess.Popen(cmd, shell=True)
            break
        else:
            logger.info("Connecting at host... %s:%s", addr[0], addr[1])
            cmd = cmd_client.format(addr[0], addr[1], core_file, rom_file)
            logger.info("Running: {}".format(cmd))
            p = subprocess.Popen(cmd, shell=True)
            break

def main(host='3.15.42.116', port=5005):
    print('connecting: {}:{}'.format(host, port))
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(b'0', (host, port))

    while True:
        data, addr = sock.recvfrom(1024)
        print('client received: {} {}'.format(addr, data))
        addr = msg_to_addr_player(data)
        attempts = 1
        threading.Thread(target = listen, args = (sock,addr[2],)).start()
        while attempts < 10:
            print('{} - Sending: {}'.format(attempts, (addr[0],addr[1])))
            sock.sendto(b'0', (addr[0],addr[1]))
            time.sleep(1)
            attempts+=1
        data, addr = sock.recvfrom(1024)
        print('client received: {}:{} - {}'.format(addr[0], addr[1], data))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
