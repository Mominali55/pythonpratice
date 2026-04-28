class Car:
    # The parametr taht are passed are attributes
    def __init__(self,model,year,color,for_sale): # Constructer or dunder method
        self.model = model
        self.year = year
        self.color = color
        self.for_sale = for_sale

    def drive(self):
        print("Yu are driving")

    def stop(self):
        print("You have stopped")