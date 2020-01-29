from newspaper import Article
from bs4 import BeautifulSoup
import requests

#grab data from thehackernews home page
site = requests.get('https://thehackernews.com')

site_data = site.text

soup = BeautifulSoup(site_data, 'html.parser')

print(soup.title)

# loop through all blog posts in home page
blog_posts = soup.find("div", class_="blog-posts")

news_urls = []

story_links = soup.find_all('a', class_="story-link")


for story_link in  story_links:
    url = story_link.get('href')
    news_urls.append(url)


print(news_urls)
