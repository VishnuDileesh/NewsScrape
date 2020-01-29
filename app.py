from newspaper import Article
from bs4 import BeautifulSoup
import requests

#grab data from thehackernews home page
site = requests.get('https://thehackernews.com')
print(site.status_code)


