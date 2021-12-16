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

title = input("Enter a movie title: ")

title = title.replace(" ", "+")

movie1 = Movie(title)
title = input("Enter a second movie title: ")
title = title.replace(" ", "+")
movie2 = Movie(title)

# =============== get cast for movie1
details = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=" + movie1.title)
details = details.json()
id = str(details["results"][0]["id"])
# print("movie id: " + id)
cast = requests.get("https://api.themoviedb.org/3/movie/" + id + "/credits?api_key=" + KEY + "&language=en-US")
cast = cast.json()
# print(cast)

cast = cast["cast"]
# print(cast)

castList = []
for actor in cast:
    castList.append(actor["name"])
movie1.cast = castList



# ======================= get cast for movie2 =====================================

details = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=" + movie2.title)
details = details.json()
id = str(details["results"][0]["id"])
# print("movie id: " + id)
cast = requests.get("https://api.themoviedb.org/3/movie/" + id + "/credits?api_key=" + KEY + "&language=en-US")
cast = cast.json()
# print(cast)

cast = cast["cast"]
# print(cast)

castList = []
for actor in cast:
    castList.append(actor["name"])
movie2.cast = castList

print(movie1.cast)
print()
print(movie2.cast)

common = []

for actor in movie1.cast:
    if actor in movie2.cast:
        common.append(Actor(actor))
print("Common: ")
for actor in common:
    print(actor.name)