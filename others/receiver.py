#!/usr/bin/env python

import socket
import sys


if len(sys.argv) < 3:
    print("USAGE: %s IP PORT" % sys.argv[0])
    quit()

ip = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while 1:
    data, addr = sock.recvfrom(1024)
    print("Received from", addr)
