# Demostration of how a Function return and type it returns.

def main():
    name,house = get_student()
    state,city = get_address()
    state, city = ("Maharashtra", "Pune") if state.strip() == "" and city.strip() == "" else (state, city) # pythonic way of writing
    marks = get_marks()
    print(f"{name} from {house}")
    print(f"{state} is your state and {city} is your city")
    print(f"{marks['marks']} and {marks['grade']}")

def get_student():
    name = input("Name: ")
    house = input("House: ")
    return (name,house) # By defualt a fuction always return a "Tuple" datatype 

def get_address():
    state = input("Enter a state: ")
    city = input("Enter your city name: ")
    return [state,city] # Returning a list.

def get_marks():
    marks = int(input("Enter your marks: "))
    grade = input("Enter your grade: ")
    return {"marks":marks,"grade":grade} #Returning a Dictionay

if __name__ == "__main__":
    main()

# Note:
# 1.Dictionary and list are mutable datatypes.
# 2.Tuple is an immutable datatype.