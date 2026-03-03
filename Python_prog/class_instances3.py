# Designing your code

class Student: 

    def __init__(self, name, house): 
        if not name:
            raise ValueError("Missing name") 
        if house not in ["poco", "garden", "mikes"]:
            raise ValueError("Invalid house")
        
        self.name = name 
        self.house = house

    def __str__(self): 
        return f"{self.name} from {self.house}"
    
    # The improved code
    @classmethod
    def get(cls):
        name =input("Name: ")
        house =input("House: ")
        return cls(name,house) # why use  "cls" here..?
        

def main():
    student = Student.get()
    if student:
        print(student) 
        print("Magic!!!")
        print(student.casting())
    else:
        print("No magic today, student creation failed.")

# Bad Design 

""" 
def get_student():
    name = input("Name: ")
    house = input("House: ")  
    student = Student(name, house) 
    return student

"""

if __name__ == "__main__":
    main()


# Note:
# 1.Now everthing related to studnet is in a sigle "Student" class 
# 2.Yu can also declare "main" function on teh top of the file..It will work bcz "main()" is called at last line 