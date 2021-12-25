import sys
import requests

KEY = "fd1ba63489529c937b3759165608f6cd"


# nodes for AVL tree
class Node:
    def __init__(self, id, src):
        self.id = int(id)
        self.left = None
        self.right = None
        self.height = 1
        # source variable to trace back the path when a connection is found
        self.src = src


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, root, id, src):
        # compare id to root, move left or right or return if equal
        if not root:
            return Node(id, src)
        elif id < root.id:
            root.left = self.insert(root.left, id, src)
        elif id > root.id:
            root.right = self.insert(root.right, id, src)
        else:
            return root

        # adjust height for balancing
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        # check balance and rotate if needed
        balance = self.getBalance(root)
        if balance > 1:
            if id < root.left.id:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balance < -1:
            if id > root.right.id:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    def leftRotate(self, node):
        newRoot = node.right
        child = newRoot.left
        newRoot.left = node
        node.right = child
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
        return newRoot

    def rightRotate(self, node):
        newRoot = node.left
        child = newRoot.right
        newRoot.right = node
        node.left = child
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
        return newRoot

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    # print an in-order traversal of the tree
    def printTree(self, root):
        if not root:
            return

        self.printTree(root.left)
        print(root.id, end=" ")
        self.printTree(root.right)

    def getInOrderArray(self, root, arr):
        if not root:
            return

        self.getInOrderArray(root.left, arr)
        arr.append(root.id)
        self.getInOrderArray(root.right, arr)

    def search(self, root, id):
        if not root:
            return None

        if id < root.id:
            return self.search(root.left, id)
        elif id > root.id:
            return self.search(root.right, id)
        else:
            return root


def getActorIDFromName(name):
    name = name.replace(" ", "+")
    details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + name)
    details = details.json()
    name = str(details["results"][0]["id"])
    return name

def getMovieList(id):
    actor = getActorNameFromID(id)
    print("getting movie list for " + actor)
    data = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "/movie_credits?api_key=" + KEY)
    data = data.json()
    data = data["cast"]
    movieList = []
    for movie in data:
        movieList.append(movie["id"])

    return movieList

def getCastList(id):
    movie = getMovieNameFromID(id)
    print("getting cast list for " + movie)
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "/credits?api_key=" + KEY + "&language=en-US")
    data = data.json()
    data = data["cast"]
    castList = []
    for actor in data:
        castList.append(actor["id"])
    return castList

def getActorNameFromID(id):
    data = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "?api_key=fd1ba63489529c937b3759165608f6cd")
    data = data.json()
    name = data["name"]
    return name


def getMovieNameFromID(id):
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=fd1ba63489529c937b3759165608f6cd")
    data = data.json()
    title = data["title"]
    return title

def checkConnections(actors, movies, aTree, aRoot, mTree, mRoot, count, target):
    if count >= 5:
        return -1
    newMovieList = []
    newActorList = []
    # TODO: close infinite loop
    for actor in actors:
        movieList = getMovieList(actor)
        for movie in movieList:
            if movie not in movies and movie not in newMovieList:
                newMovieList.append(movie)
                mRoot = mTree.insert(mRoot, movie, actor)
        for movie in newMovieList:
            actorList = getCastList(movie)
            for actr in actorList:
                if actr not in actors and actr not in newActorList:
                    newActorList.append(actr)
                    aRoot = aTree.insert(aRoot, actr, movie)
                if actr == target:
                    path = [actr, movie]
                    path = backtrack(path, aTree, mTree, aRoot, mRoot)
                    return path

    return checkConnections(newActorList, newMovieList, aTree, aRoot, mTree, mRoot, count+1, target)


def backtrack(path, aTree, mTree, aRoot, mRoot):
    pathlength = len(path)
    last = path[pathlength-1]
    if last == None:
        return path
    if pathlength % 2 == 0:
        path.append(mTree.search(mRoot, last).src)
        return backtrack(path, aTree, mTree, aRoot, mRoot)
    else:
        path.append(aTree.search(aRoot, last).src)
        return backtrack(path, aTree, mTree, aRoot, mRoot)





# actorTree = Tree()
# actor = None
# ids = [10, 5, 15, 12, 5, 17, 20, 12]
# for id in ids:
#     actor = actorTree.insert(actor, id, None)
# actorTree.printTree(actor)
# print()
# print("    " + str(actor.id))
# print("  " + str(actor.left.id), end="   ")
# print(actor.right.id)
# print(str(actor.left.left.id), end="   ")
# print(str(actor.left.right.id), end="   ")
# print(actor.right.right.id)

# actor1 = input("Enter an actor: ")
# actor1 = actor1.replace(" ", "+")
# details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + actor1)
# details = details.json()
# actor1 = str(details["results"][0]["id"])
# actor2 = input("Enter another actor: ")
# actor2 = actor2.replace(" ", "+")
# details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + actor2)
# details = details.json()
# actor2 = str(details["results"][0]["id"])


matchFound = False

actor1 = input("Enter an actor: ")
actor1 = int(getActorIDFromName(actor1))
actor2 = input("Enter another actor: ")
actor2 = int(getActorIDFromName(actor2))


print("Actor1 ID: " + str(actor1))
actor1Name = getActorNameFromID(actor1)
print(actor1Name)
print("Actor2 ID: " + str(actor2))
actor2Name = getActorNameFromID(actor2)
print(actor2Name)


# actorTree = Tree()
# actorRoot = None
# actorRoot = actorTree.insert(actorRoot, actor1, None)
# movieTree = Tree()
# movieRoot = None
# lst = getMovieList(actorRoot.id)
# print("nodes being added to movies tree: ")
# for movie in lst:
#     # print("Movie: " + getMovieNameFromID(movie))
#     movieRoot = movieTree.insert(movieRoot, movie, actorRoot)
#
# # print("Movie list for actor1:")
# # print(lst)
#
# # print("Preorder traversal of movielist from actor1: ")
# # movieTree.printTree(movieRoot)
# print()
# # print("title of root: " + getMovieNameFromID(str(movieRoot.id)))
# print("getting actor list from each movie")
# for mv in lst:
#     # list of IDs of actors in mv
#     actrList = []
#     # get IDs of full cast of mv and fill actrList
#     actrList = getCastList(mv)
#     for actr in actrList:
#         # Insert new actors into actorTree and add the new node into actorNodeList
#         actorRoot = actorTree.insert(actorRoot, int(actr), mv)
#         if actr == actor2:
#             print("Connection found!")
#             print(actor1Name + " Has appeared in " + getMovieNameFromID(mv) + " with " + actor2Name)
#             exit()
#     # print("Added actors from movie " + getMovieNameFromID(mv))
#
# print("List of actors who have appeared in films with " + actor1Name + ": ")
# inOrder = []
# actorTree.getInOrderArray(actorRoot, inOrder)
# print(inOrder)
# # count = 0
# # for actor in inOrder:
# #     print(getActorNameFromID(actor), end=", ")
# #     count += 1
# #     if count > 8:
# #         print()
# #         count = 0

# steps = 0
# actorList = [actor1]
# adjActors = []
# movieList = []
# acTree = Tree()
# acRoot = None
# movTree = Tree()
# movRoot = None
# acRoot = acTree.insert(acRoot, actor1, None)



# while steps < 6 and not matchFound:
#     for actor in actorList:
#         movieList = []
#         movieList = getMovieList(actor)
#         for movie in movieList:
#             actors = []
#             movRoot = movTree.insert(movRoot, movie, actor)
#             actors = getCastList(movie)
#             adjActors += actors
#             for actr in actors:
#                 acRoot = acTree.insert(acRoot, actr, movie)
#                 if actr == actor2:
#                     print("Connection found! " + actor2Name + " appeared in " + getMovieNameFromID(movie) + " with " + getActorNameFromID(actor))
#                     print("Degrees of separation: " + str(steps))
#                     matchFound = True
#                     break
#     actorList = adjActors
#     adjActors = []
#     steps += 1

aTree = Tree()
actorList = [actor1]
movieList = []
aTree = Tree()
aRoot = None
mTree = Tree()
mRoot = None
aRoot = aTree.insert(aRoot, actor1, None)
res = checkConnections(actorList, movieList, aTree, aRoot, mTree, mRoot, 0, actor2)
print(res)
fullpath = res[-2::-1]
print(fullpath)
if res == -1:
    print("No connection found")
else:
    print("Connection found: ")


    print(getActorNameFromID(actor1) + " appeared in ", end="")
    for i in range(1, len(fullpath)-1):
        if i % 2 == 0:
            name = getActorNameFromID(fullpath[i])
            print(name + ", who appeared in ", end="")
        else:
            title = getMovieNameFromID(fullpath[i])
            print(title + " with ", end="")
    print(getActorNameFromID(actor2))
