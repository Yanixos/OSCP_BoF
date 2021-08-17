import socket


PREFIX = ""
SUFFIX = ""

encode  = lambda x : bytes(x , encoding='raw_unicode_escape')

def connect_send(target, port, buffer):

    try : 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        print("[!] Connecting to {} {}.".format(target,port))
        s.connect((target,port))

        #"""
        print("[!] Receiving data: ")
        data = s.recv(1024)
        print(data)
        #"""

        buffer = PREFIX + buffer + SUFFIX
        print("[!] Sending buffer of len {}.".format(len(buffer)))
        s.send(encode(buffer))

        #"""
        print("[!] Receiving data: ")
        data = s.recv(1024)
        print(data)
        #"""

        print("[!] Closing socket.\n\n")
        s.close()

    except Exception as e :
        print("Error: {}\n\n".format(e))
        return True

    return False

def get_answer(answer) :
    
    while True :
        if answer.lower() == "no" or answer.lower() == "n" :
            return False
        elif answer.lower() == "yes" or answer.lower() == "y" :
            return True
        else :
            answer = input("(yes/no): ").strip()