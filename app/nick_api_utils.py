import os
from dotenv import load_dotenv
import requests

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

def search_movies(title):
    url = "https://imdb236.p.rapidapi.com/api/imdb/search"
    querystring = {
        "primaryTitleAutocomplete": title,
        "type": "movie",
        "rows": "25"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        return {"error": True, "message": "API request failed"}

    return response.json().get("results", [])



