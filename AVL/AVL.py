import sys

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
            root.left = self.insert(root.left, id)
        else:
            root.right = self.insert(root.right, id)

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
        print(root.id)
        print("/  \\")
