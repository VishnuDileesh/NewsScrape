from newspaper import Article
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
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



# New Class code goes here

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

            print(self.summary)

            new_article = Articlelist(title=self.title, author=self.author, summary=self.summary)

            db.session.add(new_article)
            db.session.commit()



        def get_article(self):
            return [self.title, self.author, self.summary]





# New Class code ends here




@app.route('/')
def index():
    # new code goes here
    #grab data from thehackernews home page


    

    db.drop_all()


    site1_content = requests.get('https://thehackernews.com')

    site1_data = site1_content.text

    soup1 = BeautifulSoup(site1_data, 'html.parser')


    # loop through all blog posts in home page
    blog_posts = soup1.find("div", class_="blog-posts")

    news_urls = []

    story_links1 = soup1.find_all('a', class_="story-link")


    for story_link1 in  story_links1:
        url = story_link1.get('href')
        news_urls.append(url)

    db.create_all()


    site1 = NewsArticle(news_urls)





    # new code ends here






#       print(article.article_title)

     #   data.append(article_data)



    #print(data[1])

    #print(data[1]['author'])


    # iterating over outer dictionary keys
    #for i in data:
    #    print(i)


    #iterating over values of outer dictionary
    #for i in data:
    #    print(i, " : " , data[i])



    # print keys of inner dictionary
    #for i in data:

     #   for j in data[i]:
     #       print(j)


    # print keys and values of inner dictionary

    #for i in data:

    #    for j in data[i]:
    #        print(j, ":", data[i])

    # print values of inner dictionary

    #for i in data:

    #    for j in data[i]:

    #       print(data[i][j])

    #print(' ')
    #print(type(data))

    articles = Articlelist.query.all()


    return render_template("index.html", articles=articles)


#db.session.query(Articledb).delete()
#db.session.commit()



if __name__ == "__main__":
    app.run()
