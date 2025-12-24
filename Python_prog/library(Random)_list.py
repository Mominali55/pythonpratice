import random

cards =["jack", "queen", "king"]

def main():
    choice(cards)
    choices(cards)
    choices_with_weights(cards)
    sample(cards)
    sample_two(cards)
    suffle(cards)

def choice(cards):
    #This function will print one random card
    print(random.choice(cards))

def choices(cards):
    #This function will print two random cards
    print(random.choices(cards,k=2)) #here we use k=2 to get two random cards(this will only print)

def choices_with_weights(cards):
    # This function will print two random cards according to th weight given
    print(random.choices(cards, weights=[100, 0, 0], k=2)) # bcz of high weight of jack it will print jack only(both 2 cards)

def sample(cards):
    #This function will print two random cards without replacement
    print(random.sample(cards, k=2)) # here we use k=2 to get two random cards(this will only print)

def sample_two(cards):
    #This function will print two random cards without replacement with seed
    random.seed(0)
    print(random.sample(cards, k=2)) # here we use k=2 to get two random cards(this will only print)

def suffle(cards):
    #This function will shuffle the cards and print them
    random.shuffle(cards)
    for card in cards:
        print(card)     

main()

# Note:
# random.choice(): returns a single random element from the list.
# random.choices(): returns a list of elements chosen from the list, allowing for duplicates.
# random.sample(): returns a list of unique elements chosen from the list, without replacement.

# -------------------------------------------------------------------- #    
# --Meaning of with replacement and without replacement--
# Eg:
# With replacement: If you have a bag of 3 different colored balls (red, blue, green) and you draw one ball, note its color, and then put it back in the bag before drawing again, you could potentially draw the same color multiple times.
# Without replacement: If you draw a ball from the bag and do not put it back, the next draw will be from the remaining balls, so you cannot draw the same color again until all colors have been drawn.
# In summary, "with replacement" allows for the same item to be selected multiple times, while "without replacement" ensures that each item can only be selected once until all items have been chosen.
# In the above code:
# - random.choices() allows for the same card to be selected multiple times (with replacement).
# - random.sample() ensures that each card is selected only once (without replacement).`
