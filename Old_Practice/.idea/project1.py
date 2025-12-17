a="*form to check wheather you are elible for vote*"
print(a.upper().center(70,"-"))
b=str(input("male or female".upper()))
if b=='y' or b=='Y':
    print("gender is male".upper())
else:
    print("gneder is female".upper())
a = "*enter your address in the given format*"
print(a.upper().center(70, "-"))
b = "state,city,pincode,flat"
print(b.upper().center(70, "-"))
def address(c):
    print(user_input.upper())


# Input prompt from user
user_input = input("Enter your address: ")
address(user_input)

print("*is this your perfect address ?(y/n)*".upper())
d=str(input())
if d=='y' or d=='Y':
    print("confirmed".upper())
else:
    print("re-submission".upper())
    user_input = input("Enter your address: ")
    address(user_input)
    print("updated address:",user_input)

def pancard(n1,n2="Re-nenter!"):
    print("Pancard no1:",n1)
    print("Pancard no2:",n2)

print("Enter your pancard number in a order way:".upper().center(70, "-"))
pan_input=input("enter your first pancard no:".upper())
pan_input2=input("enter your alternate pancard no:".upper())
if pan_input.isalpha():
    print("enter number not alphabet".upper())
    print("Enter your pancard number in a order way:".upper().center(70, "-"))
    pan_input=input("enter your first pancard no:".upper())
    print("plz also enter a alternate pancard".upper().center(70, "-"))
    pan_input2=input("enter your alternate pancard no:".upper())
    if pan_input2.isalpha():
        print("enter number not alphabet".upper())
        print("Enter your pancard number in a order way:".upper().center(70, "-"))
        pan_input2=input("enter your alternate pancard no:".upper())
        pancard(pan_input,pan_input2)
    elif pan_input2.isnumeric():
        pancard(pan_input,pan_input2)
    else:
        print("Error!*Re-enter")
        pan_input2=input("enter your alternate pancard no:".upper())
        pancard(pan_input,pan_input2)

else:
    pancard(pan_input,pan_input2)
























