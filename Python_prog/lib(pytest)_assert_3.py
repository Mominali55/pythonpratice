# Testing a function with pytest assertions methods

def main():
    x=int(input("What's is x"))
    print("X squared is:",square(x))

def square(n):
    return n * n

if __name__== "__main__":
    main()