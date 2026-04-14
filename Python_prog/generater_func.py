def count(n):
    number=[]
    inc=1
    while inc < n:
        number.append(inc)
        inc+=1
    return number

user= int(input("Enter "))

for n in count(user):
    print(n)