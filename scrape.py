from newspaper import Article
from bs4 import BeautifulSoup
import requests
import sqlite3
import os


connection = sqlite3.connect('news_scrape.db')
cursor = connection.cursor()

class NewsArticle:

    def __init__(self, news_urls):

        self.news_urls = news_urls

        for news_url in self.news_urls:

            article = Article(news_url)

            article.download()

            article.parse()

            self.title = article.title

            self.author = article.authors[0]

            article.nlp()

            self.summary = article.summary

            cursor.execute("""INSERT INTO Articlelist VALUES (?, ?, ?)""", (self.title, self.author, self.summary))



            connection.commit()




def scrape_news():

    cursor.execute("DROP TABLE Articlelist")

    print("Dropped Table")


    print("Creating Table")
    
    cursor.execute(
    """CREATE TABLE Articlelist(
        title  TEXT,
        author  TEXT,
        summary  TEXT
    )
    """)

    connection.commit()


    print("Created Table")

    site1_content = requests.get('https://thehackernews.com')

    site1_data = site1_content.text

    soup1 = BeautifulSoup(site1_data, 'html.parser')

    news_urls = []

    story_links1 = soup1.find_all('a', class_="story-link")

    for story_link1 in story_links1:
        url = story_link1.get('href')
        news_urls.append(url)

    site1 = NewsArticle(news_urls)


    news_urls.clear()

    site2_content = requests.get('https://www.ehackingnews.com/search/label/Cyber%20Crime?max-results=7')

    site2_data = site2_content.text

    soup2 = BeautifulSoup(site2_data, 'html.parser')

    blog_posts = soup2.find_all('article', class_="home-post")

    for blog_post in blog_posts:

        url = blog_post.h2.a.get('href')

        news_urls.append(url)

    site2 = NewsArticle(news_urls)













scrape_news()
