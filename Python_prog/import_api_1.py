from museum_1.artwork import get_artwork
from museum_1.artists import get_artists

def main():
    artist = input("Artist: ")
    artworks = get_artwork(query=artist, limit=3)
    for artwork in artworks:
        print(f"* {artwork}")

main()