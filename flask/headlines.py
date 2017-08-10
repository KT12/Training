import feedparser

from flask import Flask
app = Flask(__name__)

MR_Feed = "http://feeds.feedburner.com/marginalrevolution/feed?format=xml"
BBC_Feed = 'http://feeds.bbci.co.uk/news/rss.xml'

@app.route("/")
def get_news():
    feed = feedparser.parse(MR_Feed)
    first_article = feed.get('entries')[0]
    print(len(feed.get('entries')))
    #print(first_article)
    return ("""<html>
         <body>
            <h1> MR </h1>
            <b>{}</b> <br/>
            <i>{}</i> <br/>
            <p>{}</p> <br/>
        <body/>
    <html/>""".format(first_article.get('title'), first_article.get('published'), first_article.get('summary')))

@app.route("/hello")
def hello():
    return "Hello, World!"
if __name__ == "__main__":
    app.run(port=5000, debug=True)
