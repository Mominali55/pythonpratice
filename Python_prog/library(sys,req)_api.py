import sys 
import requests

def main():
    print("Search the Art Institute of Chicago!")
    try:
        response = requests.get(
            "https://api.artic.edu/api/v1/artworks/search", {"q": input("Artist: "), "limit": 3} #taking input from user and limiting the results to 3 
        )
        response.raise_for_status()  # Check if the request was successful
    except requests.HTTPError:
        print("Couldn'y not complet requets")
        sys.exit(1) #here we say one bcz of error we are exiting the program with status code 1

    #Coverting into python dictionary
    content = response.json()

    #Looping over each artwork in data that is in the form of dictionary and list
    for artwork in content["data"]:
        print(f"* {artwork['title']}") #printing the title of each artwork

main()

