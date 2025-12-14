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


d="*Aneme*"
print(d.upper().center(49,"-"))

e=["1.Gear-5!","2.bankai!!","3.Domain expansion"]
for x in e:
    print(x.upper().ljust(30),"cannot be define".upper().center(20,"-"))

d="*veg*"
print(d.upper().center(49,"-"))

f={
    "1.":"butter panner"
    ,
    "2.":"manchorein"
    ,
    "3.":"swendish"


}
for x,y in f.items():
    print(f"{x[:-1]}.{y}".upper().ljust(30),"30".upper().center(20,"-"))

g="*non-veg*"
print(g.center(49,"-").upper())
# Now using list
b=["butter chicken","chicken sharwma","butter nun"]
b.insert(2,"kabab")
b.insert(4,"kiddo")
print("1."+b[0].upper().ljust(28),"200$".upper().center(20,"-"))
print("2."+b[1].upper().ljust(28),"40$".upper().center(20,"-"))
print("3."+b[2].upper().ljust(28),"1000$".upper().center(20,"-"))
print("4."+b[3].upper().ljust(28),"1$".upper().center(20,"-"))
print("5."+b[4].upper().ljust(28),"sold out".upper().center(20,"-"))


a="*fruits*"
print(a.upper().center(49,"-"))
thislist=["apple","banana","cherry"]
for i in range(len(thislist)):
     print(f"{i+1}.{thislist[i].upper().ljust(28)}","20$".upper().center(20,"-"))

b="*dessert*"
print(b.upper().center(49,"~"))

c=["Gulab Jamun","Rasgulla","Ice Cream","Chocolate Brownie"]
c[4:5]=["khee"]
price=["200$","111$","300$","400$","200$"]

for x in range(len(c)):
    print(f"{x+1}.{c[x].upper().ljust(28)}{price[x].upper().center(20,"-")}")

b="*subject*"
print(b.upper().center(49,"~"))

a=["apple","banana","mango"]
i=0


while i < len(a): #range(len(c)):  You cannot use this in while loops
    fruits=f"{i+1}.{a[i].upper().ljust(9)}"
    price="200$".upper().center(20,"-").rjust(43)
    b="\nhello".upper().rjust(30)
    print(fruits + price+ b)
    i +=1








    












