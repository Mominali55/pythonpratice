#Dictionary methods

#---spelling-bee game---

#Declaring the words
words = {"PAIR":5,"HAIR":4,"CHAIR":5}

# You cannot add "correct = 0" here same as C bcz python does not allow to change global variable you have to explicity tell python for chnaging it
def main():
    correct = 0
    print("Welcome to spelling bee game!")
    print("You letter are: A I P C R H G")

    while len(words) > 0:
        print(f"{len(words)} words left")
        guess = input("Guess a word: ").upper()
        if guess in words:
            correct += 1
            words.pop(guess)
        else:
            print("--Wrong plz try again--")

    print(f"you got {correct} words correct")

main()