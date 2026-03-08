def meow(n: int):
    for _ in range(n):
        print("Meow!")

number= input("Number: ")
meow(number)  # This will cause a type error because input() returns a string, not an int.