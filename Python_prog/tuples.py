#We use tuples bcz it occupies less space compared to list
#But only used tuples when you know the data is not gonna change in the tuple
import sys

def main():
    coordinate_tuple=(42.376,-71.115)
    coordinate_list=[42.376,-71.115]

    print(f"{sys.getsizeof(coordinate_tuple)} bytes")
    print(f"{sys.getsizeof(coordinate_list)} bytes")

main()