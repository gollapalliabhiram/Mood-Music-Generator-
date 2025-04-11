from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

MOOD_TO_GENRE = {
    "Happy": "pop",
    "Sad": "blues",
    "Relaxed": "jazz",
    "Energetic": "rock",
}

def get_songs_by_mood(mood):
    genre = MOOD_TO_GENRE.get(mood, "pop")
    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={genre}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    data = response.json()
    return data["tracks"]["track"][:10]  # Get top 10 songs

@app.route("/", methods=["GET", "POST"])
def index():
    songs = []
    mood = ""
    if request.method == "POST":
        mood = request.form["mood"]
        songs = get_songs_by_mood(mood)
    return render_template("index.html", songs=songs, mood=mood)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
