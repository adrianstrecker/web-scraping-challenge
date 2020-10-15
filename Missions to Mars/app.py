from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    news_title = mongo.db.news_title.find_one()
    return render_template("index.html", news_title=news_title)


@app.route("/scrape")
def scraper():
    news_title = mongo.db.news_title
    news_title.drop()
    news_t_data = scrape_mars.scrape()
    # mongo.db.collection.update({}, news_t_data, upsert=True)

    news_title.insert_many(news_t_data)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
