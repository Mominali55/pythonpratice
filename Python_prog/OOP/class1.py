"""
    Here we first use the name of the file {class1_import} 
    and then {class name}
""" 
from class1_import import Car  

car1 = Car("BMW",2020,"Red",True) #invoking the constructor
print(car1)  #Printing out the address of the object

print(car1.model) 
print(car1.year)
print(car1.color)
print(car1.for_sale)

car1.drive() # calling the "method" drive
car1.stop() # calling the "method" stop