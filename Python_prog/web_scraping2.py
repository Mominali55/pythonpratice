from bs4 import BeautifulSoup


with open("file.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

#This peeticular function prints your html files ina preety way
# print(soup.prettify()) 
print(soup.title) # To get the title of the webpage

"""
For more function plz use the provided documnetation
Link = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"

"""