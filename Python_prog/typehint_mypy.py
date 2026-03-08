def meow(n: int) -> None:
    for _ in range(n):
        print("Meow!")



def main():
    number : int = int(input("Number: "))
    meows : str =meow_2(number)
    print(meows, end="")  # end="" prevents adding an extra newline after printing the meows

def meow_2(n : int) ->str:
    return "Meow\n"* n



if __name__ == "__main__":
    main()

    
# Note:
# 1. The type hints (like `n: int`) are just for readability and do not affect the actual execution of the code.
# 2. The `meow` function does not return anything, so its return type is `None`. If you want to indicate that, you can use `-> None` in the function definition.