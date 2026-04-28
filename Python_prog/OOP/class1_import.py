class Car:
    # The parametr taht are passed are attributes
    def __init__(self,model,year,color,for_sale): # Constructer or dunder method
        # Attribute sof teh object 
        self.model = model
        self.year = year
        self.color = color
        self.for_sale = for_sale

    #Methods of the object 
    def drive(self):
        print(f"You are driving {self.model}")

    def stop(self):
        print(f"You have stopped {self.model}")

    def details(self):
        print(f"Model: {self.model} with a color of {self.color} and is from the year {self.year} and is for sale: {self.for_sale}")