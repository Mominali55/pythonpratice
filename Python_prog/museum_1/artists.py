import requests #A module to handle HTTP requests

def get_artists(query, limit): #Function to get artists based on a search query and limit
    try:
        response = requests.get(
            "https://api.artic.edu/api/v1/agents/search", {"q":query,"limit":limit} #Making a GET request to the API with query and limit parameters
        )
        response.raise_for_status() #Check if the request was successful #This function is built into the requests library used to raise an error for bad responses
    except requests.HTTPError:
        return [] #Return an empty list if there was an HTTP error why not return None? #Returning an empty list allows the calling code to iterate over the result without additional checks

    content = response.json() #Parse the JSON response
    return [artists["title"] for artists in content["data"]] #Extract and return the titles of the artists from the response data
