
class Car:
    # The parametr taht are passed are attributes
    def __init__(self,model,year,color,for_sale): # Constructer or dunder method
        self.model = model
        self.year = year
        self.color = color
        self.for_sale = for_sale

car1 = Car("BMW",2020,"Red",True) #invoking the constructor
print(car1)  #Printing out the address of the object