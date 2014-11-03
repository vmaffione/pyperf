#!/usr/bin/env python

import sys
import socket

def usage_and_quit():
    print("Usage: %s LISTENPORT" % (sys.argv[0],))
    quit()


if len(sys.argv) < 2:
    usage_and_quit()

host = ''
try:
    port = int(sys.argv[1])
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

        # negotiate the test cofiguration
        config = client.recv(1)
        direction = chr(config[0])
        print("Negotiated %s" % (direction,))

        data = bytearray(4096)
        try:
            while 1:
                if direction == 'u':
                    # upload test
                    data = client.recv(4096)
                    if not data:
                        break
                else:
                    # download test
                    sent = client.send(data)
                    if sent == 0:
                        break
        except ConnectionResetError:
            # raised by client.send() if the client
            # has closed the connection
            pass
        client.close()
except KeyboardInterrupt:
    pass
