def count(n):
    inc=1
    while inc < n:
        yield inc
        inc+=1
    # return None

user= int(input("Enter "))

for n in count(user):  #Here "n" gets incremnetd never forget that
    print(n)

