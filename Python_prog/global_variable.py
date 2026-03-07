#implementation of a bank example
balance = 0

def main():
    deposit(100)
    print(balance) # This will print 0 bcz of "balance" is a global variable and we are not modifying it in the "deposit" function

def deposit(amount):
    global balance # This will allow us to modify the global variable "balance" in this function
    balance += amount # This will raise error bcz of "balance" is a global variable and we are trying to modify it in the "deposit" function

if __name__ == "__main__":
    main()