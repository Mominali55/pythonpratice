class Vault:
    def __init__(self,gold=0,silver=0,raduim=0):
        self.gold = gold
        self.silver = silver
        self.raduim = raduim

    def __str__(self):
        return f"Gold: {self.gold}, Silver: {self.silver}, Raduim: {self.raduim}"
    
    # The first self takes the value of "momin" and the second self takes the value of "keto"
    # "other" can be any data type but we are using "Vault" class here
    def __add__(self, other):
        gold =self.gold + other.gold
        silver = self.silver + other.silver
        raduim = self.raduim + other.raduim
        return Vault(gold, silver, raduim)

momin = Vault(10,20,30)
print(momin)
        
keto = Vault(5,10,15)
print(keto)

#This method will work but their is a better method

""" 
gold =momin.gold + keto.gold
silver = momin.silver + keto.silver
raduim = momin.raduim + keto.raduim

total=Vault(gold,silver,raduim)
print(total)

"""
# Operator overloading tiknik
total = momin + keto 
print(total)