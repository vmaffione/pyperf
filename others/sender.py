#!/usr/bin/env python

import socket
import sys


if len(sys.argv) < 3:
    print("USAGE: %s IP PORT", sys.argv[0])
    quit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("Ciao!", (sys.argv[1], int(sys.argv[2])))
