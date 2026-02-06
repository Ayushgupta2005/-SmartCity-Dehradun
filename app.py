from flask import Flask, render_template, request
import requests
import sqlite3
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Weather API Key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/traffic")
def traffic():
    return render_template("traffic.html")

@app.route("/weather")
def weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Dehradun&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        weather_data = {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "description": data["weather"][0]["description"].title()
        }

        return render_template("weather.html", weather=weather_data)
    except Exception as e:
        return f"<h3>Error fetching weather: {e}</h3>"

@app.route("/waste/user", methods=["GET", "POST"])
def waste_user():
    if request.method == "POST":
        location = request.form["location"]
        conn = sqlite3.connect("db.sqlite3")
        cur = conn.cursor()
        cur.execute("INSERT INTO bins (location, status) VALUES (?, ?)", (location, "Not Collected"))
        conn.commit()
        conn.close()
        return render_template("waste_user.html", success=True)
    return render_template("waste_user.html")

@app.route("/waste/admin", methods=["GET", "POST"])
def waste_admin():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    if request.method == "POST":
        bin_id = request.form["id"]
        cur.execute("UPDATE bins SET status='Collected' WHERE id=?", (bin_id,))
        conn.commit()
    cur.execute("SELECT * FROM bins")
    bins = cur.fetchall()
    conn.close()
    return render_template("waste_admin.html", bins=bins)

@app.route("/tourism")
def tourism():
    return render_template("tourism.html")

EWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route("/news")
def news():
    url = f"https://newsapi.org/v2/everything?q=Dehradun&apiKey={EWS_API_KEY}&sortBy=publishedAt&pageSize=10"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return render_template("news.html", articles=articles, now=datetime.now)

if __name__ == "__main__":
    app.run(debug=True)
