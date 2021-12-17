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

    def getMovieList(self):
        details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + self.name)
        details = details.json()
        id = str(details["results"][0]["id"])
        movieList = requests.get("https://api.themoviedb.org/3/person/" + id + "/movie_credits?api_key=" + KEY)
        movieList = movieList.json()
        movieList = movieList["cast"]
        for movie in movieList:
            self.movies.append(movie["title"])


class Movie:

    def __init__(self, title):
        self.title = title
        self.cast = []

    def getCast(self):
        details = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=" + self.title)
        details = details.json()
        id = str(details["results"][0]["id"])
        cast = requests.get("https://api.themoviedb.org/3/movie/" + id + "/credits?api_key=" + KEY + "&language=en-US")
        cast = cast.json()
        cast = cast["cast"]
        for actor in cast:
            self.cast.append(actor["name"])

actor = input("Enter actor: ")
actor = actor.replace(" ", "+")
actor1 = Actor(actor)
actor1.getMovieList()
print(actor1.movies)
actor = input("Enter another actor: ")
actor = actor.replace(" ", "+")
actor2 = Actor(actor)
actor2.getMovieList()
print(actor2.movies)

common = []
for movie in actor1.movies:
    if movie in actor2.movies:
        common.append(movie)
print(common)


# title = input("Enter a movie title: ")
#
# title = title.replace(" ", "+")
#
# movie1 = Movie(title)
# title = input("Enter a second movie title: ")
# title = title.replace(" ", "+")
# movie2 = Movie(title)
#
# movie1.getCast()
# print(movie1.cast)
# movie2.getCast()
# print(movie2.cast)

# =============== get cast for movie1
# details = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=" + movie1.title)
# details = details.json()
# id = str(details["results"][0]["id"])
# # print("movie id: " + id)
# cast = requests.get("https://api.themoviedb.org/3/movie/" + id + "/credits?api_key=" + KEY + "&language=en-US")
# cast = cast.json()
# # print(cast)
#
# cast = cast["cast"]
# # print(cast)
#
# castList = []
# for actor in cast:
#     castList.append(actor["name"])
# movie1.cast = castList



# ======================= get cast for movie2 =====================================

# details = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + KEY + "&query=" + movie2.title)
# details = details.json()
# id = str(details["results"][0]["id"])
# # print("movie id: " + id)
# cast = requests.get("https://api.themoviedb.org/3/movie/" + id + "/credits?api_key=" + KEY + "&language=en-US")
# cast = cast.json()
# # print(cast)
#
# cast = cast["cast"]
# # print(cast)
#
# castList = []
# for actor in cast:
#     castList.append(actor["name"])
# movie2.cast = castList
#
# print(movie1.cast)
# print()
# print(movie2.cast)

# common = []
#
# for actor in movie1.cast:
#     if actor in movie2.cast:
#         common.append(Actor(actor))
# print("Common: ")
# for actor in common:
#     print(actor.name)