#Algorithm which checks whether the wall of a Nurikabe is continuous or not. It is based on an algorithm from the book: "Foundation of Computer Science in C" by Alfred V. Aho and Jeffrey D. Ullman.
#The original example was written in C and has been adapted to the Nurikabe. The original algorithm can be found here: http://blough.ece.gatech.edu/3020/focs.pdf on pages 474 - 475
#By Jacek Wikiera - Sat 27 april 19 - 22:11

#"B" means wall, this Nurikabe has a continous wall by default
table = [["B", "B", "1", "B", "I", "2"],
        ["1", "B", "B", "B", "B", "B"],
        ["B", "B", "2", "I", "B", "2"],
        ["I", "2", "B", "B", "B", "I"]]

#set x and y length of the table
x_len = len(table)
y_len = len(table[0])

#define node class (helps for referring to nodes as to objects)
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.height = 0

    def __str__(self):
        return "x:{}; y:{}; parent:{}; height:{} -- ".format(self.x, self.y, self.parent, self.height)
    def __repr__(self):
        return self.__str__()

#define edge class (helps for referring to edges as to objects)
class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __str__(self):
        return "node1:{}; node2:{}; -- ".format(self.node1, self.node2)
    def __repr__(self):
        return self.__str__()

#creation of nodes
nodeList = []
for i in range(x_len):
    for j in range(y_len):
        if table[i][j] == "B":
            nodeList.append(Node(i, j))

#creation of edges
edgeList = []
for i in range(x_len):
    for j in range(y_len):
        if table[i][j] == "B":
            # right
            if (j < y_len - 1 and table[i][j + 1] == "B"):
                for node in nodeList:
                    if node.x == i and node.y == j:
                        node1 = node
                for node in nodeList:
                    if node.x == i and node.y == (j + 1):
                        node2 = node
                edgeList.append(Edge(node1, node2))
            #down
            if (i < x_len - 1 and table[i + 1][j] == "B"):
                for node in nodeList:
                    if node.x == i and node.y == j:
                        node1 = node
                for node in nodeList:
                    if node.x == (i + 1) and node.y == j:
                        node2 = node
                edgeList.append(Edge(node1, node2))

#function which gets the root of a node
def find(node):
    root = node
    while root.parent != None:
        root = root.parent
    #print(root)
    return root

#function which merges two tree roots
def merge(root1, root2):
    higher = root1
    lower = root2
    if root2.height > root1.height:
        higher = root2
        lower = root1
    if root1.height == root2.height:
        root1.height += 1
    lower.parent = higher

for edge in edgeList:
    a = find(edge.node1)
    b = find(edge.node2)
    if a != b:
        merge(a, b)

#check whether multiple trees existx
rootList = [find(nodeList[0])]
for node in nodeList:
    if find(node) not in rootList:
        rootList.append(find(node))
if len(rootList) > 1:
    print("La mer n'est pas continue")
else:
    print("La mer est continue")
