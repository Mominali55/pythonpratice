"""
# Calss variables : Shared among all instances of a class
                    Defined outside te constructor
                    Allow yu ti share data among all objects of a class
                    
"""

class Student:
    # Class variable 
    school = "Harvard University"
    no_of_st = 0

    def __init__(self,name,age):
        self.name = name
        self.age = age
        Student.no_of_st += 1


# So after defining the {Student.no_of_st}
# After each object the value of this var will be increased by 1
student1 = Student("Momin", 20)
student2 = Student("Jhon", 22)
student3 = Student("Smith", 21)

print(student1.name)
print(student2.name)
print(student3.name)

# Best practice to acces class variable by using calss names
print(Student.school)
print(Student.no_of_st)

print(f"Total number of student from {Student.school} is {Student.no_of_st}")