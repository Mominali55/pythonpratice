#---spelling-bee game---

words = {"PAIR":5,"HAIR":4,"CHAIR":5,"GRAPHIC":7}

def key_item():
    print("\n--- Point Values ---")
    for name, points in words.items():
        print(f"{name}: {points} points")
    print("--------------------\n")

def main():
    print("Welcome to the game!")
    print("Your letters are: A I P R C H G")
    
    # FIX 1: Call this at the START, while the dictionary is still full
    key_item() 
    
    while len(words) > 0:
        print(f"{len(words)} words left")
        guess = input("Guess a word: ").upper()

        if guess == "GRAPHIC":
            # FIX 2: Save the points BEFORE you clear the list
            points = words.get("GRAPHIC") 
            words.clear()
            print(f"JACKPOT! You scored {points} points and won automatically!")
            
        elif guess in words:
            points = words.pop(guess)
            print(f"Good job you scored {points} points")
        else:
            print("Wrong or already guessed.")
            
    print("That's the game!")  

main()