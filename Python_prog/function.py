"""
Function in python are first class object therefore they can be treated as same as any variable.
"""
from typing import Callable

def add(a:int,b:int) -> int:
    return a+b

def sub(a:int,b:int) -> int:
    return a-b

# 1.Assigment to variables

my_obj = add

print(f"1.Assigment to variable{my_obj(5,2)}")

# 2.Passing as arguments

def cal(func:callable[[int,int],int],a:int,b:int) -> int:
    return func(a,b)

print(f"2.Passing as arguments :{cal(add,5,4)}")

# 3.Returning from function (We return the object we dont call it in this)

# Here we use callable type bcz in return we have specifies taht it will return a function object which takes two int and return int 
def choose(boolean : bool)-> Callable[[int,int],int]:
    if boolean:
        return add
    else:
        return sub

temp_obj=choose(False)   #This will return function object

print(f"3.Returning from function{temp_obj(5,3)}")

# 4. Storing in data structure

calculator = {
    "+":add,
    "-":sub
}

# Another method of calling a function without storing it first in a object is to call it directly from the data structure
print(f"4.Storing in data structure :{calculator["+"](5,3)}")

# Procedure:
# 1.here first the "calculator["+"]" will return the function object which is add and then we call it with (5,3) to get the result.

#Tuple

def do_idle():
    print("Doing nothing")

def do_patrol():
    print("Patrolling the area")

def do_attack():
    print("Attacking the enemy")

NPC_ACTION : tuple[callable] = (do_idle,do_patrol,do_attack)

def npc(action:int) -> None:
    #This is the pythonoic way of writting two conddition when there is a use of two condtions
    if 0 <= action < len(NPC_ACTION):

        # By adding "()" the function mentioned in teh tuple will execute imeadiately
        NPC_ACTION[action]()
    
    else:
        print("Errr:Unkmown action found")

print("--- Testing are npc ---\n")
npc(0)


"""
[AI]
Why is this useful? (The "Senior" Perspective)
By treating functions as data, you write highly modular code. 
If you want to add a "subtract" feature to the dictionary in step 4, 
you don't have to rewrite any core logic or add more elif statements. 
You just define def subtract() and add "-": subtract to the dictionary. 
This makes your code incredibly scalable.

"""