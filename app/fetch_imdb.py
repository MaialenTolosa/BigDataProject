import requests
import pandas as pd

url = "https://imdb236.p.rapidapi.com/api/imdb/search"
querystring = {
    "type": "movie",
    "genre": "Drama",
    "rows": "25",
    "sortOrder": "ASC",
    "sortField": "id"
}
headers = {
    "x-rapidapi-key": "b847622aa8mshfc4538cd3edb0aep1dbcfajsn1ea3987b7406",
    "x-rapidapi-host": "imdb236.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# Convert to JSON
data = response.json()

# Inspect what keys are available
print(data.keys())  # optional

# Extract movies (this may vary slightly depending on structure)
movies = data.get("results") or data.get("data") or data  # fallback if it's a list

# Convert to DataFrame
df = pd.DataFrame(movies)

# Show top 10 entries in table form
print(df.head(10))