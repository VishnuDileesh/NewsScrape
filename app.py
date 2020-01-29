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


    article_num = 0

    for article in list_articles:

        article_num += 1

        data[article_num] = {}

        data[article_num]['title'] = article.article_title

        data[article_num]['author'] = article.article_author[0]

        data[article_num]['summary'] = article.article_summary


        #article_data = article.get_article()

        #data[article.article_title] = {}

        #data[article.article_title]['author'] = article.article_author
        #data[article.article_title]['keywords'] = article.article_keywords
        #data[article.article_title]['summary'] = article.article_summary
    

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

    for i in data:

        for j in data[i]:

            print(data[i][j])

    print(' ')
    print(type(data))





    return render_template("index.html", articles=data)



if __name__ == "__main__":
    app.run()
