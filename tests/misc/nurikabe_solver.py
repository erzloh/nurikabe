# "U": 0
# "B": -1
# "W": -2
# "E": -3 (edge)
import sys, math


class island:
    def __init__(self, x, y, size, table):
        self.table = table
        self.x = x
        self.y = y
        self.size = size
        self.lastTouched = False
        self.triedFailedTiles = []
        self.addedTilesHistory = []
        self.complete = False
        self.potentialNewTiles = None
        # the unused tiles are, if a tile gets removed from the island but its information should be kept
        self.unusedTiles = []
        self.tiles = []
        tempTiles = returnTiles(x, y, self.table)
        for element in tempTiles:
            self.tiles.append(tile(element[0], element[1]))
            # print("appended", element[0], element[1])
        # self.impossibleMoves = [] moved to a class
        # impossible moves ex: [[(2, 2), [(2, 1), (2, 3)]]]


class tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.impossibleMoves = []


class state:
    def __init__(self, table):
        self.table = table
        self.impossibleMoves = []
        self.lastMove = None
        self.lastIsland = None


class state2:
    def __init__(self):
        self.tables = []


class table:
    def __init__(self, table):
        self.table = table
        self.impossibleMoves = []


#Function to check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1 - x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1 - y2) == 1):
        touching = True
    return touching


# Function to check continuity of the wall including undefined space to check if the creation of a continuous wall is possible
def checkWallIntegrityIncludingUndefined(table):
    x_len = len(table)
    y_len = len(table[0])
    setList = []
    for i in range(x_len):
        for j in range(y_len):
            if (table[i][j] == -1 or table[i][j] == 0) and (len(setList) == 0):
                setList.append([(i, j)])
            elif table[i][j] == -1 or table[i][j] == 0:
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
    # if (len(setList[0] & setList[1])) > 0:
    # pass  # print("hello")
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
        return False
    else:  # print("The wall is continuous")
        return True


# **OWN** **NOT IN USE** Function to check continuity of the wall
def checkWallIntegrity(table):
    x_len = len(table)
    y_len = len(table[0])
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
        return False
    else:  # print("The wall is continuous")
        return True


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
            if table[i][j] == -1:
                nodeList.append(Node(i, j))

    # creation of edges
    edgeList = []
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == -1:
                # right
                if (j < y_len - 1 and table[i][j + 1] == -1):
                    for node in nodeList:
                        if node.x == i and node.y == j:
                            node1 = node
                    for node in nodeList:
                        if node.x == i and node.y == (j + 1):
                            node2 = node
                    edgeList.append(Edge(node1, node2))
                # down
                if (i < x_len - 1 and table[i + 1][j] == -1):
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


# Function to turn tiles between numbers black "-1"
def elimAdj(table):
    x_len = len(table)
    y_len = len(table[0])

    for i in range(x_len):
        for j in range(y_len):
            # check in the right direction
            if (i < (x_len - 2)) and table[i][j] > 0 and table[i + 2][j] > 0:
                table[i + 1][j] = -1
            # check below
            if (j < (y_len - 2)) and table[i][j] > 0 and table[i][j + 2] > 0:
                table[i][j + 1] = -1
    return table


# Function to turn tiles next to "ones" black ("-1"), kinda useless, now that there is the wallAroundIslands function
def elimAroundOnes(table):
    x_len = len(table)
    y_len = len(table[0])
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == 1:
                if i > 0:  # left
                    table[i - 1][j] = -1
                if j > 0:  # up
                    table[i][j - 1] = -1
                if i < x_len - 1:  # right
                    table[i + 1][j] = -1
                if j < y_len - 1:  # down
                    table[i][j + 1] = -1
    return table


# Function to turn tiles in diagonal black ("-1")
def diagonal(table):
    x_len = len(table)
    y_len = len(table[0])

    for i in range(x_len):
        for j in range(y_len):
            # case n1: "2" "-1"
            #           "-1" "2"
            if i < x_len - 1 and j < y_len - 1:
                if table[i][j] > 0 and table[i + 1][j + 1] > 0:
                    table[i + 1][j] = -1
                    table[i][j + 1] = -1
                # case n2: "-1" "2"
                #           "2" "-1"
                if table[i + 1][j] > 0 and table[i][j + 1] > 0:
                    table[i][j] = -1
                    table[i + 1][j + 1] = -1
    return table


# Function to check for 2x2 wall blocks
def wallBlockCheck(table):
    x_len = len(table)
    y_len = len(table[0])
    foundBlock = False
    for i in range(x_len - 1):
        for j in range(y_len - 1):
            if table[i][j] == -1 and table[i + 1][j] == -1 and table[i][j + 1] == -1 and table[i + 1][j + 1] == -1:
                foundBlock = True  # print("2x2 wall block found at x:",i,"and y:",j)
                return (i, j)
    if not foundBlock:  # print("No 2x2 blocks in the wall")
        return None


# Function to check if a single island is complete, NOT HANDLING CASE WHEN ISLAND TOO BIG, needed for this function
def islandCheckNotTooBig(x, y, table, counter, tempTable=None, revertTable=None, returning=False):
    if tempTable == None:
        tempTable, revertTable = [], []
    x_len = len(table)
    y_len = len(table[1])
    if (x, y) not in tempTable:
        counter = counter - 1
        # print("counter is",counter)
        if counter == 0:
            # print("Island complete")
            return True
        tempTable.append((x, y))
    if not returning:
        revertTable.append((x, y))
    if x > 0 and table[x - 1][y] == -2 and (x - 1, y) not in tempTable:
        # print("left")
        return islandCheckNotTooBig(x - 1, y, table, counter, tempTable, revertTable, returning=False)
    elif y > 0 and table[x][y - 1] == -2 and (x, y - 1) not in tempTable:
        # print("up")
        return islandCheckNotTooBig(x, y - 1, table, counter, tempTable, revertTable, returning=False)
    elif (x < x_len - 1) and table[x + 1][y] == -2 and (
            x + 1, y) not in tempTable:  # I wonder if the < x_len-1 works in all cases ###print("right")
        return islandCheckNotTooBig(x + 1, y, table, counter, tempTable, revertTable, returning=False)
    elif (y < y_len - 1) and table[x][y + 1] == -2 and (x, y + 1) not in tempTable:
        # print("down")
        return islandCheckNotTooBig(x, y + 1, table, counter, tempTable, revertTable, returning=False)
    elif len(revertTable) > 1:
        revertTable.pop()
        # print("returning")
        return islandCheckNotTooBig(revertTable[len(revertTable) - 1][0], revertTable[len(revertTable) - 1][1], table,
                                    counter, tempTable, revertTable, returning=True)
    else:
        # print("Island not complete")
        return False


# FINAL Function to check if a single island is complete
def islandCheck(x, y, table, counter, returning=False):
    flag = True
    # counter = int(table[i][j])
    counterCopy = counter
    # tempTable.clear()
    if not islandCheckNotTooBig(x, y, table, counterCopy):
        flag = False
    counterCopy = counter + 1
    if islandCheckNotTooBig(x, y, table, counterCopy):
        flag = False
    return flag


# Function to check if all islands are complete
def allIslCheck(table):
    x_len = len(table)
    y_len = len(table[1])
    flag = True
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] > 0:
                counter = table[i][j]
                if flag:
                    flag = islandCheck(i, j, table, counter)
    return flag


# Function that returns a requested neighbour. Directions can be: up, down, right, left. "-3" = edge
def neighbour(table, x, y, direction):
    if direction == "up":
        if y == 0:
            return -3
        else:
            return table[x][y - 1]
    if direction == "down":
        if y == len(table[0]) - 1:
            return -3
        else:
            return table[x][y + 1]
    if direction == "left":
        if x == 0:
            return -3
        else:
            return table[x - 1][y]
    if direction == "right":
        if x == len(table) - 1:
            return -3
        else:
            return table[x + 1][y]


# 2nd Function that returns a requested neighbour. Directions can be: up, down, right, left. "-3" = edge
def neighbour2(table, x, y, direction):
    if direction == "up":
        if x == 0:
            return -3
        else:
            return table[x - 1][y]
    if direction == "down":
        if x == len(table) - 1:
            return -3
        else:
            return table[x + 1][y]
    if direction == "left":
        if y == 0:
            return -3
        else:
            return table[x][y - 1]
    if direction == "right":
        if y == len(table[0]) - 1:
            return -3
        else:
            return table[x][y + 1]


# Function to replace a given neighbour by a value.
def setNeighbour(x, y, table, direction, value):
    if neighbour(table, x, y, direction) != -3:
        if direction == "up":
            table[x][y - 1] = value
        if direction == "down":
            table[x][y + 1] = value
        if direction == "left":
            table[x - 1][y] = value
        if direction == "right":
            table[x + 1][y] = value


# Function to turn a "0" (undefinded) in "-1" (black) if surrounded by "-1" or -3 (edge)
def surround(table):
    x_len = len(table)
    y_len = len(table[0])
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == 0 and (neighbour(table, i, j, "up") == -3 or neighbour(table, i, j, "up") == -1) and (
                    neighbour(table, i, j, "down") == -3 or neighbour(table, i, j, "down") == -1) and (
                    neighbour(table, i, j, "left") == -3 or neighbour(table, i, j, "left") == -1) and (
                    neighbour(table, i, j, "right") == -3 or neighbour(table, i, j, "right") == -1):
                table[i][j] = -1
    return table


# Function to return all island parts. I has two modes: "complete" (default) (island must be complete to return an array, if not returns False) and "everything" (will always retun an array)
# actually might be obsolete because of the returnTiles function which doesn't need to be given the "center" tile of the island.
def islandParts(x, y, table, counter, partList=None, tempTable=None, revertTable=None, mode="complete",
                returning=False):
    if partList == None:
        partList, tempTable, revertTable = [], [], []
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
    if x > 0 and table[x - 1][y] == -2 and (x - 1, y) not in tempTable:  # print("left")
        return islandParts(x - 1, y, table, counter, partList, tempTable, revertTable, mode, returning=False)
    elif y > 0 and table[x][y - 1] == -2 and (x, y - 1) not in tempTable:  # print("up")
        return islandParts(x, y - 1, table, counter, partList, tempTable, revertTable, mode, returning=False)
    elif (x < x_len - 1) and table[x + 1][y] == -2 and (
            x + 1, y) not in tempTable:  # I wonder if the < x_len-1 works in all cases ###print("right")
        return islandParts(x + 1, y, table, counter, partList, tempTable, revertTable, mode, returning=False)
    elif (y < y_len - 1) and table[x][y + 1] == -2 and (x, y + 1) not in tempTable:  # print("down")
        return islandParts(x, y + 1, table, counter, partList, tempTable, revertTable, mode, returning=False)
    elif len(revertTable) > 1:
        revertTable.pop()  # print("returning")
        return islandParts(revertTable[len(revertTable) - 1][0], revertTable[len(revertTable) - 1][1], table, counter,
                           partList, tempTable, revertTable, mode,
                           returning=True)
    else:  # print("Island not complete")
        if mode == "complete":
            return False
        else:
            return partList


# Function to turn tiles next to islands into "-1". It has two modes: "complete" and "everything". The complete mode will check if the island is complete before proceeding, the everything mode won't do that check.
def wallAroundIslands(table, mode="complete"):
    x_len = len(table)
    y_len = len(table[1])
    if mode == "complete":
        for i in range(x_len):
            for j in range(y_len):
                if table[i][j] > 0:
                    if islandCheck(i, j, table, int(table[i][j])):
                        # tempTable.clear()
                        # revertTable.clear()
                        # partList.clear()
                        tiles = islandParts(i, j, table, int(table[i][j]))
                        # print("tiles:",tiles)
                        for tile in tiles:
                            if neighbour(table, tile[0], tile[1], "up") != -2 and neighbour(table, tile[0], tile[1],
                                                                                            "up") != -3 and (
                                    neighbour(table, tile[0], tile[1], "up") < 1):
                                table[tile[0]][tile[1] - 1] = -1
                            if neighbour(table, tile[0], tile[1], "right") != -2 and neighbour(table, tile[0], tile[1],
                                                                                               "right") != -3 and (
                                    neighbour(table, tile[0], tile[1], "right") < 1):
                                table[tile[0] + 1][tile[1]] = -1
                            if neighbour(table, tile[0], tile[1], "down") != -2 and neighbour(table, tile[0], tile[1],
                                                                                              "down") != -3 and (
                                    neighbour(table, tile[0], tile[1], "down") < 1):
                                table[tile[0]][tile[1] + 1] = -1
                            if neighbour(table, tile[0], tile[1], "left") != -2 and neighbour(table, tile[0], tile[1],
                                                                                              "left") != -3 and (
                                    neighbour(table, tile[0], tile[1], "left") < 1):
                                table[tile[0] - 1][tile[1]] = -1
                    else:
                        # print("Could not put wall around island", i, j,". Not complete")  # actually should not happen but who knows
                        pass
    else:
        for i in range(x_len):
            for j in range(y_len):
                if table[i][j] > 0 or table[i][j] == -2:
                    if neighbour(table, i, j, "up") != -2 and neighbour(table, i, j, "up") != -3 and (
                            neighbour(table, i, j, "up") < 1):
                        table[i][j - 1] = -1
                    if neighbour(table, i, j, "right") != -2 and neighbour(table, i, j, "right") != -3 and (
                            neighbour(table, i, j, "right") < 1):
                        table[i + 1][j] = -1
                    if neighbour(table, i, j, "down") != -2 and neighbour(table, i, j, "down") != -3 and (
                            neighbour(table, i, j, "down") < 1):
                        table[i][j + 1] = -1
                    if neighbour(table, i, j, "left") != -2 and neighbour(table, i, j, "left") != -3 and (
                            neighbour(table, i, j, "left") < 1):
                        table[i - 1][j] = -1


# Function to add tiles to an island if and only if it isn't complete and is surrounded by the Wall everywhere except on one spot. (It keeps relaunching itself until the conditions are not met)
def addOneTile(x, y, table, counter=None, succeeded=False, returning=False):
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
        # print("parts are: ", parts)
        neighbours = []
        eligibleParts = []
        # print("part length:",len(parts))
        totalOnlyZeros = []
        islandEligibleForAddingOneTile = False
        for i in range(len(parts)):
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "up"))
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "right"))
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "down"))
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "left"))
            # print("neighbours of",x, y, "are: ",neighbours)
            if totalOnlyZeros.count(0) == 1:
                islandEligibleForAddingOneTile = True
            else:
                # print("island",x,y,"finally not eligible, returning")
                return
        for i in range(len(parts)):
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "up"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "right"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "down"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "left"))
            # print("neighbours of",x, y, "are: ",neighbours)
            if neighbours.count(0) == 1:
                # print("true")
                eligibleParts.append((parts[i][0], parts[i][1]))
            neighbours.clear()
        if len(eligibleParts) == 1:
            # print("second true")
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "up") == 0:
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "up", -2)
                return addOneTile(x, y, table, counter, True, True)
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "right") == 0:
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "right", -2)
                return addOneTile(x, y, table, counter, True, True)
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "down") == 0:
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "down", -2)
                return addOneTile(x, y, table, counter, True, True)
            if neighbour(table, eligibleParts[0][0], eligibleParts[0][1], "left") == 0:
                setNeighbour(eligibleParts[0][0], eligibleParts[0][1], table, "left", -2)
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
            if table[x][y] > 0:
                addOneTile(x, y, table)


# Function to display table in console
def printTable(table):
    x_len = len(table)
    y_len = len(table[0])
    tempStr = ""
    for i in range(y_len):
        for j in range(x_len):
            tempStr += str(table[j][i]) + " "
        print(tempStr)
        tempStr = ""


# Function to display table in console in the old way
def printTableOld(table):
    x_len = len(table)
    y_len = len(table[0])
    tempStr = ""
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == 0:
                convert = "U"
            elif table[i][j] == -1:
                convert = "B"
            elif table[i][j] == -2:
                convert = "W"
            else:
                convert = table[i][j]
            tempStr += str(convert) + " "
        print(tempStr)
        tempStr = ""


if __name__ == '__main__':
    # tables
    table = [["1", "B", "2", "W", "B", "2", "W"],
             ["B", "B", "B", "B", "B", "B", "B"],
             ["2", "W", "B", "4", "W", "B", "1"],
             ["B", "B", "W", "W", "B", "B", "B"],
             ["2", "B", "B", "B", "2", "U", "B"],
             ["W", "B", "4", "B", "B", "B", "B"],
             ["B", "B", "W", "W", "W", "B", "1"]]

    table = [[0, 0, 0, 0, 0, 0],
             [-1, 0, -1, -1, -1, 0],
             [2, -1, 15, 0, -1, 0],
             [0, 0, -1, 0, -1, 0],
             [0, 0, -1, 0, 0, 0]]

    table = [[0, 0, 0, 0, 0, 0],
             [-1, -1, -1, -1, -1, 0],
             [2, -1, 15, 0, -1, 0],
             [0, -1, -1, 0, -1, 0],
             [-1, -1, -1, 0, 0, 0]]
    table = [[0, 0, 0, 2, 0],
             [0, 1, 0, -2, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 2, 0, 2, 0],
             [0, 0, 0, 0, 0],
             [0, 2, 0, 0, 0],
             [0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 2, 0, 0],
             [0, 3, 0, 0, 1],
             ]
    table = [[1, -1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 0],
             [2, 0, 2, 0],
             [0, 0, 0, 0]]


# return possible tiles for an incomplete island
def returnPotentialTiles(table, x, y):
    tiles = returnTiles(x, y, table)
    potentialNewTiles = []
    for item in tiles:
        if neighbour2(table, item[0], item[1], "up") == 0:
            potentialNewTiles.append((item[0] - 1, item[1]))
        if neighbour2(table, item[0], item[1], "right") == 0:
            potentialNewTiles.append((item[0], item[1] + 1))
        if neighbour2(table, item[0], item[1], "down") == 0:
            potentialNewTiles.append((item[0] + 1, item[1]))
        if neighbour2(table, item[0], item[1], "left") == 0:
            potentialNewTiles.append((item[0], item[1] - 1))
    return potentialNewTiles


#############################################################
# Function to count tiles in an island TEST
def returnTiles(x, y, table, partList=None):
    if partList == None:
        partList = []
    if (table[x][y] == -2 or table[x][y] > 0) and (x, y) not in partList:
        partList.append((x, y))
        if x > 0:
            returnTiles(x - 1, y, table, partList)
        if x < len(table) - 1:
            returnTiles(x + 1, y, table, partList)
        if y > 0:
            returnTiles(x, y - 1, table, partList)
        if y < len(table[0]) - 1:
            returnTiles(x, y + 1, table, partList)
    return partList


#############################################################

if __name__ == '__main__':
    # set x and y length of the table
    x_len = len(table)
    y_len = len(table[0])

    ##execute functions
    """elimAroundOnes(table)
    elimAdj(table)
    diagonal(table)

    surround(table)
    wallAroundIslands(table)#, "everything")
    wallAroundIslands(table)

    addOneTileEverywhere(table)
    surround(table)
    #wallAroundIslands(table)
    printTable(table)
    print("Any 2x2 blocks in the wall?", wallBlockCheck(table))
    print("Is the wall continuous?", checkWallIntegrity2(table))
    print("Are all islands complete?", allIslCheck(table))
    print("count",countTiles(0, 3, table))

    wallAroundIslands(table)
    printTableOld(table)


    print(table)"""
    print(checkWallIntegrityIncludingUndefined(table))
