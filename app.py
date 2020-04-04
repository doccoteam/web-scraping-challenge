from flask import Flask, render_template, redirect
from datetime import datetime
import scrape_mars
import pymongo
import json

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
mars_db = client.mars


@app.route("/")
def index():      
    data = mars_db.mars_data.find_one()
    print(data)
    return render_template("index.html", data = data, current_time=datetime.utcnow())


@app.route("/scrape")
def scrape_data():
    scraped_data = scrape_mars.scrape()
    data = mars_db.mars_data
    data.delete_many({})
    data.insert(scraped_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug = True)