# pythonpratice
# this file is made for pythonpractice or project.
# menu card


b="welcome to our hotel{:^10} have a good meal"
print(b.format("^_^").center(3,"-").upper())

a="*cold drinks*"
print(a.upper().center(49,"-"))


c=["1.lorem cold drink","2.ipsum cold drink","3.lorem ipsum cold drink","4.lorem cold drink"]
for x in c:
    print(x.upper().ljust(30),"20$".upper().center(20,"-"))


d="*kiddo*"
print(d.upper().center(49,"-"))

e=["1.she is sweet","2.she is cute","3.she is beauty^_^full"]
for x in e:
    print(x.upper().ljust(30),"cannot be define".upper().center(20,"-"))

d="*veg*"
print(d.upper().center(49,"-"))

f={"1.":"butter panner","2.":"panner shawarma","3.":"veg-mandi"}
for x in f:
    print(x)









