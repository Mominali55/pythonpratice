def main():
    #Creating an empty list
    history=[]
    while True:
        only_possible_actions=["right","left","forward","back"]

        action=input("right,left,forward,back:\n").lower()
        if action in only_possible_actions:
            history.append(action)
            print(history)
        elif action == "undo":
            poped_val=history.pop()
            print("You undoed:",poped_val)
            print(history)
        elif action == "restart":
            history.clear()
            print("History is cleared",history)
        elif action == "exit":
            break
        else:
            print("Plz provide a valid action")
            continue
    print("Game Over")

main()
    
    
