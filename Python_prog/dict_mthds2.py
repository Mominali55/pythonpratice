#---spelling-bee game---

#Declaring the words

words = {"PAIR":5,"HAIR":4,"CHAIR":5,"GRAPHIC":7}

def main():
    print("Welcome to the game!")
    print("You letters are: A I P R C H G")
    
    while len(words) > 0:
        print(f"{len(words)} words left")
        guess = input("Guess a word: ").upper()

        #The jackpot word
        if guess == "GRAPHIC":
            words.clear()
            print(f"Good jovb you scored {words.get('GRAPHIC')} points")
            print("You win!")

        elif guess in words.keys():
            points =words.pop(guess)
            print(f"Good job you scored {points} points")
        else:
            print("Wrong")
    print("That's the game!")
            
        
main()
