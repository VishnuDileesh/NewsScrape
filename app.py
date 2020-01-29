from newspaper import Article
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template

class Newsarticle:

    def __init__(self, title, author, keywords, summary):
        self.article_title = title
        self.article_author = author
        self.article_keywords = keywords
        self.article_summary = summary

    def get_article(self):
        #print(self.article_title)
        #print(self.article_author)
        #print(self.article_keywords)
        #print(self.article_summary)

        return [self.article_title, self.article_author, self.article_keywords, self.article_summary]


#grab data from thehackernews home page
site = requests.get('https://thehackernews.com')

site_data = site.text

soup = BeautifulSoup(site_data, 'html.parser')


# loop through all blog posts in home page
blog_posts = soup.find("div", class_="blog-posts")

news_urls = []

story_links = soup.find_all('a', class_="story-link")


for story_link in  story_links:
    url = story_link.get('href')
    news_urls.append(url)

list_articles = []


i = 0

for news_url in news_urls:

    article = Article(news_url)

    article.download()

    article.parse()

#    print(article.title)
#    print(article.publish_date)

#    print(article.authors)

    article.nlp()

#    print(article.keywords)

#    print(article.summary)

    title = article.title

    author = article.authors

    keywords = article.keywords

    summary = article.summary

    i += 1


    article_num = 'article_' + str(i) 

    article_num = Newsarticle(title, author, keywords, summary)


    list_articles.append(article_num)




app = Flask(__name__)

@app.route('/')
def index():

    #data = []

    data = {}

    for article in list_articles:

        #article_data = article.get_article()

        data[article.article_title] = {
                'author': article.article_author,
                'keywords': article.article_keywords,
                'summary': article.article_summary
        }

    

#       print(article.article_title)

     #   data.append(article_data)





    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run()
