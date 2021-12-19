import sys
import requests

KEY = "fd1ba63489529c937b3759165608f6cd"


class Node:
    def __init__(self, id, src):
        self.id = id
        self.left = None
        self.right = None
        self.height = 1
        self.src = src

class Tree:
    def __init__(self):
        self.root = None


    def insert(self, root, id, src):
        if not root:
            return Node(id, src)
        elif id < root.id:
            root.left = self.insert(root.left, id, src)
        elif id > root.id:
            root.right = self.insert(root.right, id, src)
        else:
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

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

    def printTree(self, root):
        if not root:
            return

        self.printTree(root.left)
        print(root.id, end=" ")
        self.printTree(root.right)

def getMovieList(id):
    movieList = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "/movie_credits?api_key=" + KEY)
    movieList = movieList.json()
    # movieList = movieList["cast"]
    return movieList

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

actor1 = input("Enter an actor: ")
actor1 = actor1.replace(" ", "+")
details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + actor1)
details = details.json()
actor1 = str(details["results"][0]["id"])
actor2 = input("Enter another actor: ")
actor2 = actor2.replace(" ", "+")
details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + actor2)
details = details.json()
actor2 = str(details["results"][0]["id"])

print("Actor1 ID: " + str(actor1))
print("Actor2 ID: " + str(actor2))

actorTree = Tree()
actorRoot = None
actorRoot = actorTree.insert(actorRoot, actor1, None)
movieTree = Tree()
movieRoot = None
lst = getMovieList(actorRoot)
print(lst)