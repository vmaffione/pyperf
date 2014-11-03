#!/usr/bin/env python

import sys
import socket
import time


def usage_and_quit():
    print("Usage: %s [up|down] DSTIP DSTPORT" % (sys.argv[0],))
    quit();


if len(sys.argv) < 4:
    usage_and_quit()

direction = sys.argv[1]
host = sys.argv[2]
try:
    port = int(sys.argv[3])
except ValueError:
    usage_and_quit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
data = bytearray(4096)
bytes_cnt = 0
bytes_cnt_th = 1000
last_ts = time.time()

try:
    while 1:
        if direction == 'up':
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
