from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)  

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/scrapemars_app"
# mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrapemars_app")


@app.route("/")
def index():
    scrape_mars = mongo.db.scrape_mars_db.find_one()
    return render_template("index.html", scrapings=scrape_mars)


@app.route("/scrape")
def scraper():
    # scrape_mars = mongo.db.scrape_mars_db
    # Run the scrape function

    scraping_data = scrape_mars.scrape()
    scrape_mars.update({}, scraping_data, upsert=True)
    return redirect("/", code=302)

#-----------------------


if __name__ == '__main__':  
    app.run(debug = True)