# NewsScrape
### Personal Project built on Python, using Flask and Newspaper3k

I love reading cyber tech news, and i wanted to create a single web page to skim through all the latest cyber sec news from more than one hacking news sites.
I decided to build a web scraper which would go and check through the site links provided, and will get the latest articles links using BeautifulSoup.
The links are passed through Newspaper3k to grab the title and author of every article.
Newspaper3k is used along Natural Language Processing function to create a summary of the complete article.
All the individually scraped articles are stored in the sqlite3 database.
Python Flask web app will grab the data from the database and display the articles title, author and summary of all the articles from the passed in site urls scraped in above step and saved to the db.
Scraping function is set to run every day at 12:00 AM using the Schedule package.
