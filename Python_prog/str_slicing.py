import sys


def slice_sys_argv():
    if len(sys.argv) < 2:
        sys.exit()
    for arg in sys.argv[1:]: #Looping over the sys.argv list
        print("hello there",arg)


def main():
    phone = "6174829384"
    
    print("\n1.First 4 digits")
    print(phone[0:4])
    
    print("\n2.First 8 digits")
    print(phone[:8])

    print("\n3.Last 4 digits")
    print(phone[6:10])

    print("\n4.Last 4 digits")
    print(phone[6:])
    
    print("\n5.Last 4 digits")
    print(phone[-4:])
    
    print("\n6.First 10 digits")
    print(phone[0:10:1]) #here we use one in last to print the string in original order you can use -1 to print the string in reverse order
    
    print("\n7.Reversed")
    print(phone[::-1])
    
    print("\n8.Copy of string")
    print(phone[:])

    slice_sys_argv()

main()