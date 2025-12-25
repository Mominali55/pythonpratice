import sys 
import requests
import json #importing json library to work with json data line: 32

def main():
    json_lib()
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


def json_lib():
    if len(sys.argv) != 2:
        sys.exit()
    
    response = requests.get(
        "https://itunes.apple.com/search?entity=song&limit=1&term=" + sys.argv[1] #Artist name passed as command line argument
    )
    # print(json.dumps(response.json(),indent=2)) #The json becomes more readible by explicitly telling intend by 2
    temp=response.json()
    for result in temp["results"]: #looping over each result in results list Eg:Taylor Swift songs
        print(result["trackName"]) #printing the track name of each result
main()


# Note:
# When you provide input from terminal the sys.argv takes its as a list so if the artist name has space Eg: Taylor swift it will consider it as two different arguments,
# so to avoid that we can provide the name in quotes Eg:"Taylor Swift"

