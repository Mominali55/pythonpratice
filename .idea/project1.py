a="*form to check wheather you are elible for vote*"
print(a.upper().center(70,"-"))
b=str(input("male or female".upper()))
if b=='y' or b=='Y':
    print("gender is male".upper())
else:
    print("gneder is female".upper())
a = "*enter your address in the given format*"
print(a.upper().center(70, "-"))
def address(c):
    b = "state,city,pincode,flat"
    print(b.upper().center(70, "-"))
    print("Your entered address:", c)

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
    print(user_input)

















