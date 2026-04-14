
def add_tie(func):
    def wrapper(*args,**kwargs):
        print("Tie got added to child")
        func(*args,**kwargs) #child
    return wrapper

def add_tiffin(func):
    def wrapper(*args,**kwargs):
        print("Tiffin added")
        func(*args,**kwargs) #add_tie
    return wrapper #referenece passing

@add_tiffin
@add_tie    # child = add_tiffin(add_tie(child))
def child(name):
    print(f"The {name} child is ready with hsi school uniform")

child("Slop")