class Student: 
    def __init__(self, name, house):  
        if not name:
            raise ValueError("Missing name") 
        # We are storing variables in this instance
        self.name = name 
        self.house = house #This will also called the "setter" method

    def __str__(self): 
        return f"{self.name} from {self.house}"
    
    #getter
    @property
    def house(self):  #Always Zero argument excluding "self"
        return self._house #To avoid getting loop
    
    #setter
    @house.setter 
    def house(self,house): #Alway one argumnet
        if house not in ["poco", "garden", "mikes"]:
            raise ValueError("Invalid house")
        self._house = house
    
def main():
    student = get_student()
    student.house = "Ebyss" #Explicitly  settig values
    if student:
        print(student) 
    else:
        print("No magic today, student creation failed.")

def get_student():
    name = input("Name: ")
    house = input("House: ")  
    student = Student(name, house)
    return student



# Note:
# 1.The above will raise error bcz of accessing the "student.house = "Ebyss"
if __name__ == "__main__":
    main()