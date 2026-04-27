# Web scraping Notes 


"""
1.Beautifull soup 
2.Scrpy 
3.Requests

Proxy can be used to hide your IP address and avoid getting blocked by websites
    1.Dataimpulse (Gives yu diffrent IP addreses)


Questions:
1. Extract product and price etc from thsi website of flipkart.
Ans:
    1.Always download the website html documnet and then proceed

Eg:
"""

import requests
import time 
from fake_useragent import useragent

url = "https://www.flipkart.com/mobile-phone-ab-at-store?pageUID=1777294384623"

session = requests.Session() # To maintain the session and cookies

headers = {
    "User-Agent": useragent().random # To mimic a real browser and avoid getting blocked
}

proxies = {
    #Here yu have to enter a proxies bought or provided by a proxy service, the format is "http://username:password@proxy_ip:proxy_port"
    "http": "http://<IP_ADDRESS>:8080", 
    "https": "http://<IP_ADDRESS>:8080"
}

time.sleep(2) # To avoid getting blocked by the website for making too many requests in a short time
r = session.get(url, headers=headers, proxies=proxies)
print(r.text)

with open("file.html","w") as b:
    b.write(r.text)