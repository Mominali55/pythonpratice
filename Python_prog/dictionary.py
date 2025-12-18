#Use of .get(),keys(),values() methods in dictionary
dictionary = {
    "voyager":2023,
    "enterprise":2265,
    "discovery":2371,
    "excalibur":2366
    }

print("\n---Key names only---\n ")
for name in dictionary.keys():
    print(name)

print("\n---Values of dictionary---\n ")
for age in dictionary.values():
    print(age)

print("\n---printing key,values pair---\n ")
for name in dictionary.keys():
    #Note:you have to use single quotes inside the double quotes
    print(f"{name} has a discovery date of {dictionary.get(name,'unknown')}")

print("\n---Without using get method---\n ")
for name in dictionary.keys():
    print(f"{name} has a discovery date of {dictionary[name]}")