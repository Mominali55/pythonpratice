# pythonpratice
# this file is made for pythonpractice or project.
a = ["apple", "banana", "cherry"]
i = 0

while i < len(a):
    b = f"{i+1}.{a[i].upper().ljust(28)}"  # Padding fruit name to 28 chars for alignment

    if a[i] == "banana":
        price = "250$".center(20, "-")
    else:
        price = "200$".center(20, "-")

    print(b + price)
    i += 1




