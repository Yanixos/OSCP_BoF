#!/usr/bin/env python3

usage = """
Using Mona.py, you can pull up a list of modules loaded with the program by entering the command: 

!mona modules 

into the bottom left text bo in Immunity Debugger. 
Choose a dll/exe that has ASLR & DEP set to false so that the address we want to jump to is always the same and executable.

Once a DLL/EXE is found, type the command:

!mona find -s "\\xff\\xe4" -m FILE.[dll/exe]

"""

print(usage)

# !mona find -s "\xff\xe4" -m 