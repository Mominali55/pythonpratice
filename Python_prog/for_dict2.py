def main():
    name = ["mario","luigi","yoshi","peach"]
    for i in range(len(name)):
        print(write_letter("Princess Peach",name[i]))

#You can write i also instead of name[i] but have to modify list accordingly

def write_letter(sender,receiver):
    return f"""
    +---------------------+
    | Hello {receiver}    |
    | You are invited to  |
    | the annual party  |
    | of {sender}       |
    +---------------------+
    """

main()  