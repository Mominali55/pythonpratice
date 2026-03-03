import random

class Hat:

    houses = ["meko","teko","leko","coco"] #This are called "class variable"

    @classmethod 
    def sort(cls,name): 
        house = random.choice(cls.houses)
        print(name,"is in",house)


Hat.sort("Momin")


# Note:
# 1. if we pass class as parameter in sort it gets conflicted with the original class
# 2. When yu use "@classmethod" yu dont have to make an object hence we use thsi sometimes