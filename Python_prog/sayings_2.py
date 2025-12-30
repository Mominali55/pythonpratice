def main():
    hello()
    goodbye()

def hello(name="world"):
    return f"hello {name}"

def goodbye(greet="great"):
    return f"goodbye {greet}" # or you can directly print the value here

if __name__ == "__main__":
    main()
    