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

response = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=Jack+Reacher")
print(response)