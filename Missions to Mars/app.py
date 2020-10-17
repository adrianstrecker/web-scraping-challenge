from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find()
    return render_template("index.html", mars_info=mars_info)



@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars_info
    mars_info.drop()
    mars_data = scrape_mars.scrape()
    print(mars_info)
    # Assistance from Benjamen Alford - use update instead of insert_many
    mongo.db.mars_info.update({}, mars_data, upsert=True)

    # mars_info.insert_many(mars_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
