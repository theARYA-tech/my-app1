import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("span", class_="titleline")

for title in titles:
    link = title.find("a")["href"]   # get the link
    if link.startswith("item"):
     link = "https://news.ycombinator.com/" + link
    print(title.text)                # print the title
    print(link)                      # print the link
    print()                          # blank line for spacing