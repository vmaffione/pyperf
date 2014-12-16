#!/usr/bin/env python

import sys
import socket
import argparse


description = "Simplified clone of netperf server:\n\
               - no separate control connection\n\
               - (data) connection destination port can be specified\n"
epilog = "Report bugs to v.maffione@gmail.com"
argparser = argparse.ArgumentParser(description = description,
                                    epilog = epilog)
argparser.add_argument('-p', '--port', help = "Server listening port",
                       type = int, default = 7777)
args = argparser.parse_args()
host = ''
    
backlog = 5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,args.port))
s.listen(backlog)

try:
    while 1:
        client, address = s.accept()

        # negotiate the test cofiguration
        config = client.recv(1)
        direction = config[0] if type(config) == str else chr(config[0])
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
        except:
            # raised by client.send() if the client
            # has closed the connection
            pass
        client.close()
except KeyboardInterrupt:
    pass
