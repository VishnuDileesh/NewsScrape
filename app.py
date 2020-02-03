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

class Articlelist(db.Model):
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    summary = db.Column(db.Text)

@app.route('/')
def index():

    articles = Articlelist.query.all()

    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    app.run()
