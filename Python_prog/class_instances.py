class Student: 
    #Special Methods

    #intialization method
    def __init__(self,name,house):  #instance method - gtes called automatically
        if not name:
            raise ValueError("Missing name") #yu can also make your own error
        if house not in ["poco","garden","mikes"]:
            raise ValueError("Invalid house")
        self.name = name #We are storing variable in this instances "it can be name anything"
        self.house = house
        

def main():
    # student = get_student()
    student = get_studenttwo()
    print(f"{student.name} from {student.house}") #The "student.name" are the instances variable

def get_student():
    student=Student() #object created
    student.name=input("Name: ")
    student.house=input("House: ")  #Yu can handle the Error of raise by using "try" and "except"
    return student

def get_studenttwo():
    name = input("Nmae: ")
    house = input("House: ")
    return  Student(name,house) #Constructer call - object created


# Note:
# 1.Class are mutabble and yu can make them imutable
# 2.We use class for customasing are inputs/data
# 3.