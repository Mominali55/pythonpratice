def meow(n:int ) -> str :
    """
    Meow n times

    :param n: Number of times to meow
    :type n : int
    :raise TypeError : if n is not an integer
    :return : A string of n meows
    :rtype : str
    """
    for _ in range(n):
        print("Meow!")

def main():
    number : int = int(input("Number: "))
    meow(number)
