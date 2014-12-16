#!/usr/bin/env python

import sys
import socket
import time
import argparse


description = "Simplified clone of netperf client:\n\
               - no separate control connection\n\
               - (data) connection destination port can be specified\n"
epilog = "Report bugs to v.maffione@gmail.com"
argparser = argparse.ArgumentParser(description = description,
                                    epilog = epilog)
argparser.add_argument('-H', '--host', help = "Server IP address",
                       type = str, default = "127.0.0.1")
argparser.add_argument('-p', '--port', help = "Server listening port",
                       type = int, default = 7777)
argparser.add_argument('-t', '--test-type',
                       help = "Test type",
                       type = str, default = "TCP_MAERTS",
                       choices = ["TCP_MAERTS", "TCP_STREAM"])
args = argparser.parse_args()

if args.test_type == "TCP_MAERTS":
    direction = 'd'
else:
    direction = 'u'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.host, args.port))
data = bytearray(4096)
bytes_cnt = 0
bytes_cnt_th = 1000
last_ts = time.time()

try:
    # negotiate the test configuration
    config = bytearray(1)
    config[0] = ord(direction[0])
    s.send(config)

    while 1:
        if direction == 'u':
            # upload test
            s.send(data)
        else:
            # download test
            data = s.recv(4096)
        bytes_cnt += len(data)
        if bytes_cnt > bytes_cnt_th:
            tslot = time.time() - last_ts
            bw = 0.0
            if tslot > 0.0:
                bw = bytes_cnt * 8.0 / 1024.0 / 1024.0 / tslot
            print("Bandwidth is %.2f Mbps" % bw)
            if tslot < 1.0:
                bytes_cnt_th *= 2
            elif tslot > 2.0:
                bytes_cnt_th /= 2
            bytes_cnt = 0
            last_ts = time.time()
except KeyboardInterrupt:
    pass

s.close()
