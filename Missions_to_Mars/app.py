# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# using PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from mongo
@app.route("/")
def home():

    # find data in collection from mongo database
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # define database and collection
    mars = mongo.db.mars

    # calling the scrape_data function in scrape_mars.py
    mars_data = scrape_mars.scrape_data()

    # updating collection in mongodb
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
