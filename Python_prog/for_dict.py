#--Email sending--

def main():
    print(write_letter("Mario","Princess Peach"))
    print(write_letter("Luigi","Princess Peach"))
    print(write_letter("Daisy","Princess Peach"))
    print(write_letter("Yoshi","Princess Peach"))

def write_letter(receiver,sender):
    return f"""
    +---------------------+
    | Hello {receiver}    |
    | You are invited to  |
    | the annual party  |
    | of {sender}       |
    +---------------------+
    """

main()
