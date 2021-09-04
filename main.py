import requests

# themoviedb.org key
#
KEY = "fd1ba63489529c937b3759165608f6cd"
# sample query:
# "https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=Jack+Reacher"

class Actor:

    def __init__(self, name):
        self.name = name
        self.movies = []

class Movie:

    def __init__(self, title):
        self.title = title
        self.cast = []


details = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=Jack+Reacher")
details = details.json()
id = str(details["results"][0]["id"])
print("movie id: " + id)
cast = requests.get("https://api.themoviedb.org/3/movie/" + id + "/credits?api_key=" + KEY + "&language=en-US")
cast = cast.json()
print(cast)

cast = cast["cast"]
print(cast)

castList = []
for actor in cast:
    castList.append(actor["name"])
print(castList)

