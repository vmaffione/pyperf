#!/usr/bin/env python

import sys
import socket

def usage_and_quit():
    print("Usage: %s [up|down] LISTENPORT" % (sys.argv[0],))
    quit()


if len(sys.argv) < 3:
    usage_and_quit()

host = ''
try:
    direction = sys.argv[1]
    port = int(sys.argv[2])
except ValueError:
    usage_and_quit()
    
backlog = 5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(backlog)

try:
    while 1:
        client, address = s.accept()
        data = bytearray(4096)
        while 1:
            if direction == 'up':
                # upload test
                data = client.recv(4096)
                if not data:
                    break
            else:
                # download test
                sent = client.send(data)
                if sent == 0:
                    break
        client.close()
except KeyboardInterrupt:
    pass
