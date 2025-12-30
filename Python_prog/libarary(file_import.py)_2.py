import sys
from Python_prog.sayings_2 import goodbye, hello

def main():
    calling_hello()
    calling_goodbye()

def calling_hello():
    if len(sys.argv) == 2:
        print(hello(sys.argv[1]))

def calling_goodbye():
    # The third argument in the terminal
    if len(sys.argv) == 3:
        print(goodbye(sys.argv[3]))

main()

#Note: if argument for "goodbye" and "hello" are not passed it will print the default value mentioned in another file.
