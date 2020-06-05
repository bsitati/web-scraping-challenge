from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)  
# Create an instance of Flask

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scrape_app"
mongo = PyMongo(app)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrape_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_scrape_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", scrapings=mars_scrape_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

   # Run the scrape function
    scrape_mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, scrape_mars_data, upsert=True)

    return redirect("/", code=302)

#-----------------------


if __name__ == '__main__':  
    app.run(debug = True)