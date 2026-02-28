class Student: 
    # Special Methods

    # Initialization method
    def __init__(self, name, house, spell):  # Instance method - gets called automatically
        if not name:
            raise ValueError("Missing name") # You can make your own error
        if house not in ["poco", "garden", "mikes"]:
            raise ValueError("Invalid house")
        
        # We are storing variables in this instance
        self.name = name 
        self.house = house
        self.spell = spell

    # String representation method
    def __str__(self): # This will be called if you print(student) instead of the object address
        return f"{self.name} from {self.house}"
    
    # Custom method
    def casting(self):
        match self.spell:
            case "abrakadabra":
                return "🧙"
            case "daba":
                return "(❁´◡`❁)"
            case "gaba":
                return "🍟"
            case _:  # It's good practice to add a default case!
                return "✨ (Spell Fizzled)"
        

def main():
    student = get_studenttwo()
    # We must check if the student was successfully created before doing magic!
    if student:
        print(student) 
        print("Magic!!!")
        print(student.casting())
    else:
        print("No magic today, student creation failed.")

"""  
def get_student():
    name = input("Name: ")
    house = input("House: ")  
    spell = input("Spell: ")
    # You must pass name, house, AND spell when creating the object!
    student = Student(name, house, spell) 
    return student

"""

def get_studenttwo():
    name = input("Name: ")
    house = input("House: ")
    spell_name = input("Name of the spell: ") 
    
    # Handling the error using try/except
    try:
        return Student(name, house, spell_name) # Constructor call
    except ValueError as e:
        print(f"Error creating student: {e}")
        return None


if __name__ == "__main__":
    main()

# Notes:
# 1. Classes are mutable, but you can make them behave immutably using properties.
# 2. We use classes for customizing and grouping our inputs/data.
# 3. When a function is inside a class, it's called a method. When it's outside, it's just a function.