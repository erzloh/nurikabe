import sys, math


# Function to check if tile is an int (just a float function changed for name)
def isInt(table, x, y):
    flag = True
    try:
        int(table[x][y])
    except ValueError:
        flag = False
    return flag


# Function to check if a var is an int, must not be a tile
def isIntTwo(var):
    flag = True
    try:
        int(var)
    except ValueError:
        flag = False
    return flag


# Function to check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1 - x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1 - y2) == 1):
        touching = True
    return touching


# **OWN** **NOT IN USE** Function to check continuity of the wall
def checkWallIntegrity(table):
    setList = []
    for i in range(x_len):
        for j in range(y_len):
            if (table[i][j] == "B") and (len(setList) == 0):
                setList.append([(i, j)])
            elif table[i][j] == "B":
                found = False
                for k in range(len(setList)):
                    l = 0
                    while l < len(setList[k]):
                        if areTouching(i, j, setList[k][l][0], setList[k][l][1]):
                            setList[k].append((i, j))
                            found = True
                            break
                        l += 1
                if not found:
                    setList.append([(i, j)])  # print(setList)
    for i in range(len(setList)):
        setList[i] = set(setList[i])  # print(setList)
    if (len(setList[0] & setList[1])) > 0:
        pass  # print("hello")
    i = 0
    while i < len(setList) - 1:
        j = 1
        while j < len(setList):
            if (len(setList[i] & setList[j])) > 0 and not (setList[i] == setList[j]):
                setList[i] = setList[i] | setList[j]
                del setList[j]
                j = 1
            else:
                j += 1
        i += 1
    # verify if there is one or more sets
    # print(setList)
    if len(setList) > 1:  # print("The wall is not continuous")
        return True
    else:  # print("The wall is continuous")
        return False


# **FROM THE BOOK** **IN USE**
# Wall Integrity Algorithm
# Algorithm which checks whether the wall of a Nurikabe is continuous or not. It is based on an algorithm from the book: "Foundation of Computer Science in C" by Alfred V. Aho and Jeffrey D. Ullman.
# The original example was written in C and has been adapted to the Nurikabe. The original algorithm can be found here: http://blough.ece.gatech.edu/3020/focs.pdf on pages 474 - 475
# By Jacek Wikiera - Sat 27 april 19 - 22:11

# Check whether the wall of the Nurikabe is continuous or not
def checkWallIntegrity2(table):
    """#"B" means wall, this Nurikabe has a continous wall by default
    table = [["B", "B", "1", "B", "W", "2"],
            ["1", "B", "B", "B", "B", "B"],
            ["B", "B", "2", "W", "B", "2"],
            ["W", "2", "B", "B", "B", "W"]]"""

    # set x and y length of the table
    x_len = len(table)
    y_len = len(table[0])

    # define node class (helps for referring to nodes as to objects)
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

    # define edge class (helps for referring to edges as to objects)
    class Edge:
        def __init__(self, node1, node2):
            self.node1 = node1
            self.node2 = node2

        def __str__(self):
            return "node1:{}; node2:{}; -- ".format(self.node1, self.node2)

        def __repr__(self):
            return self.__str__()

    # creation of nodes
    nodeList = []
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == "B":
                nodeList.append(Node(i, j))

    # creation of edges
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
                # down
                if (i < x_len - 1 and table[i + 1][j] == "B"):
                    for node in nodeList:
                        if node.x == i and node.y == j:
                            node1 = node
                    for node in nodeList:
                        if node.x == (i + 1) and node.y == j:
                            node2 = node
                    edgeList.append(Edge(node1, node2))

    # function which gets the root of a node
    def find(node):
        root = node
        while root.parent != None:
            root = root.parent
        # print(root)
        return root

    # function which merges two tree roots
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

    # check whether multiple trees exist

    # If there is at least one wall cell
    if nodeList != []:
        rootList = [find(nodeList[0])]
        for node in nodeList:
            if find(node) not in rootList:
                rootList.append(find(node))

        if len(rootList) > 1:  # print("La mer n'est pas continue")
            return False
        else:  # print("La mer est continue")
            return True
    # If there are no wall cells at all
    else:  # print("Il n'y a pas de mer")
        return None


# Function to turn tiles between numbers black "B"
def elimAdj(table):
    x_len = len(table)
    y_len = len(table[0])

    for i in range(x_len):
        for j in range(y_len):
            # check in the right direction
            if (i < (x_len - 2)) and isInt(table, i, j) and isInt(table, i + 2, j):
                table[i + 1][j] = "B"
            # check below
            if (j < (y_len - 2)) and isInt(table, i, j) and isInt(table, i, j + 2):
                table[i][j + 1] = "B"
    return table


# Function to turn tiles next to "ones" black ("B")
def elimAroundOnes(table):
    x_len = len(table)
    y_len = len(table[0])
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == "1":
                if i > 0:  # left
                    table[i - 1][j] = "B"
                if j > 0:  # up
                    table[i][j - 1] = "B"
                if i < x_len - 1:  # right
                    table[i + 1][j] = "B"
                if j < y_len - 1:  # down
                    table[i][j + 1] = "B"
    return table


# Function to turn tiles in diagonal black ("B")
def diagonal(table):
    x_len = len(table)
    y_len = len(table[0])

    for i in range(x_len):
        for j in range(y_len):
            # case n°1: "2" "w"
            #           "w" "2"
            if i < x_len - 1 and j < y_len - 1:
                if isInt(table, i, j) and isInt(table, i + 1, j + 1):
                    table[i + 1][j] = "B"
                    table[i][j + 1] = "B"
                # case n°1: "w" "2"
                #           "2" "w"
                if isInt(table, i + 1, j) and isInt(table, i, j + 1):
                    table[i][j] = "B"
                    table[i + 1][j + 1] = "B"
    return table


# Function to check for 2x2 wall blocks
def wallBlockCheck(table):
    x_len = len(table)
    y_len = len(table[0])
    foundBlock = False
    for i in range(x_len - 1):
        for j in range(y_len - 1):
            if table[i][j] == "B" and table[i + 1][j] == "B" and table[i][j + 1] == "B" and table[i + 1][j + 1] == "B":
                foundBlock = True  # print("2x2 wall block found at x:",i,"and y:",j)
                return (i, j)
    if not foundBlock:  # print("No 2x2 blocks in the wall")
        return None


# Function to check if a single island is complete, NOT HANDLING CASE WHEN ISLAND TOO BIG, needed for this function
def islandCheckNotTooBig(x, y, table, counter, tempTable=[], revertTable=[], returning=False):
    x_len = len(table)
    y_len = len(table[1])
    if (x, y) not in tempTable:
        counter = counter - 1
        #print("counter is",counter)
        if counter == 0:
            #print("Island complete")
            return True
        tempTable.append((x, y))
    if not returning:
        revertTable.append((x, y))
    if x > 0 and table[x - 1][y] == "W" and (x - 1, y) not in tempTable:
        #print("left")
        return islandCheckNotTooBig(x - 1, y, table, counter, tempTable, revertTable, returning=False)
    elif y > 0 and table[x][y - 1] == "W" and (x, y - 1) not in tempTable:
        #print("up")
        return islandCheckNotTooBig(x, y - 1, table, counter,tempTable, revertTable, returning=False)
    elif (x < x_len - 1) and table[x + 1][y] == "W" and (
    x + 1, y) not in tempTable:  # I wonder if the < x_len-1 works in all cases ###print("right")
        return islandCheckNotTooBig(x + 1, y, table, counter,tempTable, revertTable, returning=False)
    elif (y < y_len - 1) and table[x][y + 1] == "W" and (x, y + 1) not in tempTable:
        #print("down")
        return islandCheckNotTooBig(x, y + 1, table, counter,tempTable, revertTable, returning=False)
    elif len(revertTable) > 1:
        revertTable.pop()
        #print("returning")
        return islandCheckNotTooBig(revertTable[len(revertTable) - 1][0], revertTable[len(revertTable) - 1][1], table,
                                    counter,tempTable, revertTable, returning=True)
    else:
        #print("Island not complete")
        return False


# FINAL Function to check if a single island is complete
def islandCheck(x, y, table, counter, returning=False):
    flag = True
    # counter = int(table[i][j])
    counterCopy = counter
    #tempTable.clear()
    if not islandCheckNotTooBig(x, y, table, counterCopy, tempTable=[], revertTable=[],returning=False):
        flag = False
    counterCopy = counter + 1
    if islandCheckNotTooBig(x, y, table, counterCopy,tempTable=[], revertTable=[], returning=False):
        flag = False
    return flag


# Function to check if all islands are complete
def allIslCheck(table):
    x_len = len(table)
    y_len = len(table[1])
    flag = True
    for i in range(x_len):
        for j in range(y_len):
            if isInt(table, i, j):
                counter = int(table[i][j])
                if flag:
                    flag = islandCheck(i, j, table, counter)
    return flag


# Function that returns a requested neighbour. Directions can be: up, down, right, left. "E" = edge
def neighbour(table, x, y, direction):
    if direction == "up":
        if y == 0:
            return "E"
        else:
            return table[x][y - 1]
    if direction == "down":
        if y == len(table[0]) - 1:
            return "E"
        else:
            return table[x][y + 1]
    if direction == "left":
        if x == 0:
            return "E"
        else:
            return table[x - 1][y]
    if direction == "right":
        if x == len(table) - 1:
            return "E"
        else:
            return table[x + 1][y]

#Function to replace a given neighbour by a string.
def setNeighbour(x, y, table, direction, value):
    if neighbour(table, x, y, direction) != "E":
        if direction == "up":
            table[x][y - 1] = value
        if direction == "down":
            table[x][y + 1] = value
        if direction == "left":
            table[x - 1][y] = value
        if direction == "right":
            table[x + 1][y] = value

# Function to turn a "U" in "B" if surrounded by "B" or edge
def surround(table):
    x_len = len(table)
    y_len = len(table[0])
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == "U" and (neighbour(table, i, j, "up") == "E" or neighbour(table, i, j, "up") == "B") and (
                    neighbour(table, i, j, "down") == "E" or neighbour(table, i, j, "down") == "B") and (
                    neighbour(table, i, j, "left") == "E" or neighbour(table, i, j, "left") == "B") and (
                    neighbour(table, i, j, "right") == "E" or neighbour(table, i, j, "right") == "B"):
                table[i][j] = "B"
    return table

# Function to return all island parts. I has two modes: "complete" (default) (island must be complete to return an array, if not returns False) and "everything" (will always retun an array)
# partList = []
def islandParts(x, y, table, counter, partList=[], tempTable=[], revertTable=[],mode="complete", returning=False):
    # print("iteration of islandParts on", x, y)
    x_len = len(table)
    y_len = len(table[1])
    if (x, y) not in tempTable:
        # print(x,y,"not in tempTable")
        counter = counter - 1  # print("counter is",counter)
        partList.append((x, y))
        if counter == 0:  # print("Island complete")
            return partList
        tempTable.append((x, y))
        # print("appended",x,y,"to partlist: ",partList)
    if not returning:
        revertTable.append((x, y))
    if x > 0 and table[x - 1][y] == "W" and (x - 1, y) not in tempTable:  # print("left")
        return islandParts(x - 1, y, table, counter, partList,tempTable, revertTable, mode, returning=False)
    elif y > 0 and table[x][y - 1] == "W" and (x, y - 1) not in tempTable:  # print("up")
        return islandParts(x, y - 1, table, counter, partList,tempTable, revertTable, mode, returning=False)
    elif (x < x_len - 1) and table[x + 1][y] == "W" and (
    x + 1, y) not in tempTable:  # I wonder if the < x_len-1 works in all cases ###print("right")
        return islandParts(x + 1, y, table, counter, partList,tempTable, revertTable, mode, returning=False)
    elif (y < y_len - 1) and table[x][y + 1] == "W" and (x, y + 1) not in tempTable:  # print("down")
        return islandParts(x, y + 1, table, counter, partList,tempTable, revertTable, mode, returning=False)
    elif len(revertTable) > 1:
        revertTable.pop()  # print("returning")
        return islandParts(revertTable[len(revertTable) - 1][0], revertTable[len(revertTable) - 1][1], table, counter, partList,tempTable, revertTable, mode,
                           returning=True)
    else:  # print("Island not complete")
        if mode == "complete":
            return False
        else:
            return partList


# Function to turn tiles next to islands into "B". It has two modes: "complete" and "everything". The complete mode will check if the island is complete before proceeding, the everything mode won't do that check.
def wallAroundIslands(table, mode="complete"):
    x_len = len(table)
    y_len = len(table[1])
    if mode == "complete":
        for i in range(x_len):
            for j in range(y_len):
                if isInt(table, i, j):
                    # tempTable.clear()
                    # revertTable.clear()
                    # partList.clear()
                    if islandCheck(i, j, table, int(table[i][j])):
                        # tempTable.clear()
                        # revertTable.clear()
                        # partList.clear()
                        tiles = islandParts(i, j, table, int(table[i][j]))
                        for tile in tiles:
                            if neighbour(table, tile[0], tile[1], "up") != "W" and neighbour(table, tile[0], tile[1],
                                                                                             "up") != "E" and not isIntTwo(
                                    neighbour(table, tile[0], tile[1], "up")):
                                table[tile[0]][tile[1] - 1] = "B"
                            if neighbour(table, tile[0], tile[1], "right") != "W" and neighbour(table, tile[0], tile[1],
                                                                                                "right") != "E" and not isIntTwo(
                                    neighbour(table, tile[0], tile[1], "right")):
                                table[tile[0] + 1][tile[1]] = "B"
                            if neighbour(table, tile[0], tile[1], "down") != "W" and neighbour(table, tile[0], tile[1],
                                                                                               "down") != "E" and not isIntTwo(
                                    neighbour(table, tile[0], tile[1], "down")):
                                table[tile[0]][tile[1] + 1] = "B"
                            if neighbour(table, tile[0], tile[1], "left") != "W" and neighbour(table, tile[0], tile[1],
                                                                                               "left") != "E" and not isIntTwo(
                                    neighbour(table, tile[0], tile[1], "left")):
                                table[tile[0] - 1][tile[1]] = "B"
                    else:
                        print("Could not put wall around island", i, j,
                              ". Not complete")  # actually should not happen but who knows
    else:
        for i in range(x_len):
            for j in range(y_len):
                if isIntTwo(table[i][j]) or table[i][j] == "W":
                    if neighbour(table, i, j, "up") != "W" and neighbour(table, i, j, "up") != "E" and not isIntTwo(
                            neighbour(table, i, j, "up")):
                        table[i][j - 1] = "B"
                    if neighbour(table, i, j, "right") != "W" and neighbour(table, i, j,
                                                                            "right") != "E" and not isIntTwo(
                            neighbour(table, i, j, "right")):
                        table[i + 1][j] = "B"
                    if neighbour(table, i, j, "down") != "W" and neighbour(table, i, j, "down") != "E" and not isIntTwo(
                            neighbour(table, i, j, "down")):
                        table[i][j + 1] = "B"
                    if neighbour(table, i, j, "left") != "W" and neighbour(table, i, j, "left") != "E" and not isIntTwo(
                            neighbour(table, i, j, "left")):
                        table[i - 1][j] = "B"

#Function to add tiles to an island if and only if it isn't complete and is surrounded by the Wall everywhere except on one spot. (It keeps relaunching itself until the conditions are not met)
def addOneTile(x, y, table, counter = None, succeeded = False, returning = False):
    if returning == False or succeeded == True:
        if counter == None:
            counter = int(table[x][y]) - 1
            if counter == 0:
                return
        else:
            counter -= 1
        if counter <= 0:
            return
        parts = islandParts(x, y, table, int(table[x][y]), [], [], [], mode="everything")
        print("parts are: ", parts)
        neighbours = []
        eligibleParts = []
        print("part length:",len(parts))
        for i in range(len(parts)):
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "up"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "right"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "down"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "left"))
            print("neighbours of",x, y, "are: ",neighbours)
            if neighbours.count("U") == 1:
                print("true")
                eligibleParts.append((parts[i][0], parts[i][1]))
            neighbours.clear()
        if len(eligibleParts) == 1:
            print("second true")
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "up") == "U":
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "up", "W")
                return addOneTile(x, y, table, counter, True, True)
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "right") == "U":
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "right", "W")
                return addOneTile(x, y, table, counter, True, True)
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "down") == "U":
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "down", "W")
                return addOneTile(x, y, table, counter, True, True)
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "left") == "U":
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "left", "W")
                return addOneTile(x, y, table, counter, True, True)
        else:
            return addOneTile(x, y, table, counter, False, True)
    else:
         return

# Function to triger addOneTile on all islands
def addOneTileEverywhere(table):
    x_len = len(table)
    y_len = len(table[0])
    for x in range(x_len):
        for y in range(y_len):
            if isIntTwo(table[x][y]):
                addOneTile(x, y, table)

# Function to display table in console
def printTable(table):
    tempStr = ""
    for i in range(y_len):
        for j in range(x_len):
            tempStr += table[j][i] + " "
        print(tempStr)
        tempStr = ""


# tables
table = [["1", "B", "2", "W", "B", "2", "W"],
         ["B", "B", "B", "B", "B", "B", "B"],
         ["2", "W", "B", "4", "W", "B", "1"],
         ["B", "B", "W", "W", "B", "B", "B"],
         ["2", "B", "B", "B", "2", "U", "B"],
         ["W", "B", "4", "B", "B", "B", "B"],
         ["B", "B", "W", "W", "W", "B", "1"]]

table = [["U", "U", "U", "U", "U", "U"],
         ["B", "U", "B", "B", "B", "U"],
         ["2", "B", "15", "U", "B", "U"],
         ["U", "U", "B", "U", "B", "U"],
         ["U", "U", "B", "U", "U", "U"]]

# set x and y length of the table
x_len = len(table)
y_len = len(table[0])

##execute functions
# table = elimAroundOnes(table)
# table = elimAdj(table)
# table = diagonal(table)
# block_coord = wallBlockCheck(table)
# print(block_coord[1])
#printTable(table)
#print("Any 2x2 blocks in the wall?", wallBlockCheck(table))
#print("Is the wall continuous?", checkWallIntegrity2(table))
#print("Are all islands complete?", allIslCheck(table))
#print("------------------")
# table = surround(table)
#wallAroundIslands(table)#, "everything")

print(islandParts(2, 2, table, int(table[2][2]), mode="everything"))
#addOneTile(2,2,table)
addOneTileEverywhere(table)
printTable(table)
#print("Any 2x2 blocks in the wall?", wallBlockCheck(table))
#print("Is the wall continuous?", checkWallIntegrity2(table))
#print("Are all islands complete?", allIslCheck(table))
