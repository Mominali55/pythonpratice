#Taking care of assignments of variable..
class Wizard:
    def __init__(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name

     


class Student(Wizard): #inheretance i.r super-class 
    def __init__(self, name, age, grade):
        super().__init__(name) # Fetching soem features of "Wizard" class
        self.age = age
        self.grade = grade

class Professor(Wizard):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department
        
wizard =Wizard("mello")
student =Student("Momin","valo")
proffesor = Professor("Mello","tello")


# Note:
# 1.Yu can inheretate multiple classes and also modify them
# 2.We have seen this somewhere..where we used exception