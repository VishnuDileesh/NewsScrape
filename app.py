from newspaper import Article
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "news_scrape.db"))


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "newisthesecretofsecretscrape"

db = SQLAlchemy(app)



# Article model

class Articlelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    summary = db.Column(db.Text())


db.create_all()


# New Class code goes here




@app.route('/')
def index():

    articles = Articlelist.query.all()

    return render_template("index.html", articles=articles)





class NewsArticle:

    def __init__(self, news_urls):
        self.news_urls = news_urls
        
        for news_url in self.news_urls:


            article = Article(news_url)

            article.download()
            
            #print(article.html)

           
            article.parse()

            #print(article.authors)

            self.title = article.title

            self.author = article.authors[0]

            article.nlp()

            self.summary = article.summary

            #self.summary = article.summary

            #print(self.summary)

            new_article = Articlelist(title=self.title, author=self.author, summary=self.summary)

            db.session.add(new_article)
            db.session.commit()



# New Class code ends here

def scrape_news():

    print("Scraping News")

    db.drop_all()


    db.create_all()

    site1_content = requests.get('https://thehackernews.com')

    site1_data = site1_content.text

    soup1 = BeautifulSoup(site1_data, 'html.parser')


    # loop through all blog posts in home page
    #blog_posts = soup1.find("div", class_="blog-posts")

    news_urls = []

    story_links1 = soup1.find_all('a', class_="story-link")


    for story_link1 in  story_links1:
        url = story_link1.get('href')
        news_urls.append(url)

    db.create_all()


    site1 = NewsArticle(news_urls)

    # site 2

    news_urls.clear()

    site2_content = requests.get('https://www.ehackingnews.com/search/label/Cyber%20Crime?max-results=7')

    site2_data = site2_content.text

    soup2 = BeautifulSoup(site2_data, 'html.parser')

    # loop through all blog posts in home page

    blog_posts = soup2.find_all('article', class_="home-post")


    for blog_post in blog_posts:

        #print(blog_post.h2.a.get('href'))

        url = blog_post.h2.a.get('href')

        news_urls.append(url)

    site2 = NewsArticle(news_urls)




if __name__ == "__main__":
    app.run()


#schedule.every(2).minutes.do(hello())


#while True:
#    schedule.run_pending()
#    time.sleep(1)

#db.session.query(Articledb).delete()
#db.session.commit()
