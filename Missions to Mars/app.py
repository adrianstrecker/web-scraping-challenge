from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def n_title():
    news_title = mongo.db.news_title.find()
    # news_p = mongo.db.news_p.find_one()
    return render_template("index.html", news_title=news_title)

@app.route("/")
def n_para():
    news_p = mongo.db.news_p.find()
    # news_p = mongo.db.news_p.find_one()
    return render_template("index.html", news_p=news_p)


@app.route("/scrape")
def scraper():
    news_title = mongo.db.news_title
    news_title.drop()
    news_t_data = scrape_mars.scrape()
    # mongo.db.collection.update({}, news_t_data, upsert=True)

    news_title.insert_many(news_t_data)
    return redirect("/", code=302)
    
@app.route("/scrape")
def news_p_run():
    news_p = mongo.db.news_p
    news_p.drop()
    news_p_data = scrape_mars.scrape()
    # mongo.db.collection.update({}, news_p_data, upsert=True)

    news_p.insert_many(news_p_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
