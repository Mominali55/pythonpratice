from dumbledore import *

jaren=Symbol("jaren") # jaren went for playing.
farijha=Symbol("farejha") # farijha went for playing with rehan
person=Symbol("person") # rehan went with the person for playing


knowledge= And(
    Implication(Not(jaren),farijha), # ~jaren not went for playing ->rehan went with farijha
    Or(farijha,person), # (farijha went for playing) or (rehan went with the person and playing)
   # (rehan went with farijha) or (rehan went with person)
    Not(And(farijha,person)), #
     # rehan went with farijha
    person
)

if __name__=="__main__":
    query=farijha
    result=model_check(query,knowledge)
    print(f"does teh knowlege inteal that rehan went playing with farijha?{result}")


    #  Or(directionleft,directionright),
    #directionleft=Symbol("directionl") #rehan went left with farijha
#directionright=Symbol("directionr") #rehan went right with person