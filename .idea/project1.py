a="*form to check wheather you are elible for vote*"
print(a.upper().center(70,"-"))
b=str(input("enter your name.".upper()))
if  b.isupper():
    print(b)
else:
    print("plz type the letter in capital".upper())

c=str(input("enter your surname".upper()))
if c.isalnum():
    print(c)
else:
    print("o")






