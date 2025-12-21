#---try except else---

def main():
    while True:
        try:
            x = int(input("Enter a number:"))
        except (ValueError,EOFError,KeyboardInterrupt): 
            print("\n--plz enter a valid number--\n")
        else:
            print(f"You entered {x}")

main()


# Note: You can have multiple except blocks/use "," to catch different exceptions