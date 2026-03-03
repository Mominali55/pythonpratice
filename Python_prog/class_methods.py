from random import random

class Hat:
    def __int__(self):
        self.houses=["meko","teko","leko","coco"]

    def sort(self,name):
        house = random.choice(self.houses)
        print(name,"is in",house)

hat = Hat() #Object creation
hat.sort("Momin")