class Student: 
    # Special Methods

    # Initialization method
    def __init__(self, name, house):  # Instance method - gets called automatically
        if not name:
            raise ValueError("Missing name") # You can make your own error
        if house not in ["poco", "garden", "mikes"]:
            raise ValueError("Invalid house")
        
        # We are storing variables in this instance
        self.name = name 
        self.house = house

    # String representation method
    def __str__(self): #This will be called if just said print(student) instead of the object addreses,etc
        # Now it prints the actual student's info instead of just "a student"
        return f"{self.name} from {self.house}"
        

def main():
    student = get_studenttwo()
    # Only print if a valid student was returned
    if student:
        print(student) 

""" 
def get_student():
    name = input("Name: ")
    house = input("House: ")  
    # You must pass name and house when creating the object!
    student = Student(name, house) 
    return student
"""

def get_studenttwo():
    name = input("Name: ")
    house = input("House: ")
    
    # Handling the error using try/except as you mentioned in your notes
    try:
        return Student(name, house) # Constructor call - object created
    except ValueError as e:
        print(f"Error creating student: {e}")
        return None


if __name__ == "__main__":
    main()

# Notes:
# 1. Classes are mutable, but you can make them behave immutably using properties.
# 2. We use classes for customizing and grouping our inputs/data.