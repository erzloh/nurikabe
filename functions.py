# "U": 0
# "B": -1
# "W": -2
# "E": -3 (edge)
import sys, math
import copy


class island:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        #self.complete = False

class state:
    def __init__(self, table):
        self.table = table
        self.impossibleMoves = []
        self.lastMove = None
        self.lastIsland = None

#Function to check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1 - x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1 - y2) == 1):
        touching = True
    return touching

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

# Function to check for undefined tiles
def checkForUndefined(table):
    # return False if there is no undefined tiles
    undefinedInTable = False
    for line in table:
        if 0 in line:
            undefinedInTable = True
    return undefinedInTable

# Function to check if a single island is complete, NOT HANDLING CASE WHEN ISLAND TOO BIG, needed for this function
def islandCheckNotTooBig(x, y, table, counter, tempTable=None, revertTable=None, returning=False):
    if tempTable == None:
        tempTable, revertTable = [], []
    x_len = len(table)
    y_len = len(table[1])
    if (x, y) not in tempTable:
        counter = counter - 1
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
    counterCopy = counter
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

# 2nd Function that returns a requested neighbour. Directions can be: up, down, right, left. "-3" = edge
def neighbour(table, x, y, direction):
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
            table[x-1][y] = value
        if direction == "down":
            table[x+1][y] = value
        if direction == "left":
            table[x][y-1] = value
        if direction == "right":
            table[x][y+1] = value


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

# Function to turn tiles next to islands into "-1". It has two modes: "complete" and "everything". The complete mode will check if the island is complete before proceeding, the everything mode won't do that check.
def wallAroundIslands(table, mode="complete"):
    x_len = len(table)
    y_len = len(table[1])
    if mode == "complete":
        for i in range(x_len):
            for j in range(y_len):
                if table[i][j] > 0:
                    if islandCheck(i, j, table, int(table[i][j])):
                        tiles = returnTiles(i, j, table)
                        for tile in tiles:
                            if neighbour(table, tile[0], tile[1], "up") != -2 and neighbour(table, tile[0], tile[1], "up") != -3 and (neighbour(table, tile[0], tile[1], "up") < 1):
                                setNeighbour(tile[0], tile[1], table, "up", -1)
                            if neighbour(table, tile[0], tile[1], "right") != -2 and neighbour(table, tile[0], tile[1],
                                                                                               "right") != -3 and (
                                    neighbour(table, tile[0], tile[1], "right") < 1):
                                setNeighbour(tile[0], tile[1], table, "right", -1)
                            if neighbour(table, tile[0], tile[1], "down") != -2 and neighbour(table, tile[0], tile[1],
                                                                                              "down") != -3 and (
                                    neighbour(table, tile[0], tile[1], "down") < 1):
                                setNeighbour(tile[0], tile[1], table, "down", -1)
                            if neighbour(table, tile[0], tile[1], "left") != -2 and neighbour(table, tile[0], tile[1],
                                                                                              "left") != -3 and (
                                    neighbour(table, tile[0], tile[1], "left") < 1):
                                setNeighbour(tile[0], tile[1], table, "left", -1)
    else:
        for i in range(x_len):
            for j in range(y_len):
                if table[i][j] > 0 or table[i][j] == -2:
                    if neighbour(table, i, j, "up") != -2 and neighbour(table, i, j, "up") != -3 and (
                            neighbour(table, i, j, "up") < 1):
                        table[i - 1][j] = -1
                    if neighbour(table, i, j, "right") != -2 and neighbour(table, i, j, "right") != -3 and (
                            neighbour(table, i, j, "right") < 1):
                        table[i][j + 1] = -1
                    if neighbour(table, i, j, "down") != -2 and neighbour(table, i, j, "down") != -3 and (
                            neighbour(table, i, j, "down") < 1):
                        table[i + 1][j] = -1
                    if neighbour(table, i, j, "left") != -2 and neighbour(table, i, j, "left") != -3 and (
                            neighbour(table, i, j, "left") < 1):
                        table[i][j - 1] = -1


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
        parts = returnTiles(x, y, table)
        neighbours = []
        eligibleParts = []
        totalOnlyZeros = []
        islandEligibleForAddingOneTile = False
        for i in range(len(parts)):
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "up"))
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "right"))
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "down"))
            totalOnlyZeros.append(neighbour(table, parts[i][0], parts[i][1], "left"))
            if totalOnlyZeros.count(0) == 1:
                islandEligibleForAddingOneTile = True
            else:
                return
        for i in range(len(parts)):
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "up"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "right"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "down"))
            neighbours.append(neighbour(table, parts[i][0], parts[i][1], "left"))
            if neighbours.count(0) == 1:
                eligibleParts.append((parts[i][0], parts[i][1]))
            neighbours.clear()
        if len(eligibleParts) == 1:
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

# Function to trigger addOneTile on all islands
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

# Function to display table in console in the old way (Letters instead of numbers, it's way easier to read)
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

# return possible tiles for an incomplete island
def returnPotentialTiles(table, x, y):
    tiles = returnTiles(x, y, table)
    potentialNewTiles = []
    for item in tiles:
        if neighbour(table, item[0], item[1], "up") == 0:
            potentialNewTiles.append((item[0], item[1]-1))
        if neighbour(table, item[0], item[1], "right") == 0:
            potentialNewTiles.append((item[0], item[1] + 1))
        if neighbour(table, item[0], item[1], "down") == 0:
            potentialNewTiles.append((item[0], item[1]+1))
        if neighbour(table, item[0], item[1], "left") == 0:
            potentialNewTiles.append((item[0], item[1] - 1))
    return potentialNewTiles


# Function to return all parts of an island, comlete or not
def returnTiles(x, y, table, partList=None, mode=-2, undefined=False):
    if partList == None:
        partList = []
    if (table[x][y] == mode or (table[x][y] > 0 and mode==-2) or (table[x][y] == 0 and undefined)) and (x, y) not in partList:
        partList.append((x, y))
        if x > 0:
            returnTiles(x - 1, y, table, partList, mode, undefined)
        if x < len(table) - 1:
            returnTiles(x + 1, y, table, partList, mode, undefined)
        if y > 0:
            returnTiles(x, y - 1, table, partList, mode, undefined)
        if y < len(table[0]) - 1:
            returnTiles(x, y + 1, table, partList, mode, undefined)
    return partList

def checkWallIntegrity3(table, mode="normal"):
    x_len = len(table)
    y_len = len(table[0])
    islandSum = 0
    islandCount = 0
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] > 0:
                islandSum += table[i][j]
                islandCount += len(returnTiles(i, j, table))
    tempCoords = None
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == -1 or (table[i][j] == 0 and mode == "undefined"):
                coords = (i, j)
                break
    if mode == "undefined":
        print("debug")
    partList = returnTiles(coords[0], coords[1], table, None, -1, True)
    if mode == "normal" and (len(partList)+islandSum == x_len*y_len):
        return True
    elif mode == "undefined" and (len(partList)+islandCount == x_len*y_len):
        return True
    else:
        return False

#do logical moves
def logicalMoves(table):
    tempTable = []
    while tempTable != table:
        tempTable = copy.deepcopy(table)
        wallAroundIslands(table)
        addOneTileEverywhere(table)
        surround(table)

#walling function
def wall(table):
    x_len = len(table)
    y_len = len(table[0])
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == 0:
                table[i][j] = -1

#print states
def printStates(stateHistory, table):
    for k in range(len(table)):
        temp = ""
        for state in stateHistory:
            for l in range(len(table[0])):
                if state.table[k][l] == -2:
                    temp += "W "
                elif state.table[k][l] == -1:
                    temp += "B "
                elif state.table[k][l] == 0:
                    temp += "U "
                else:
                    temp += str(state.table[k][l]) + " "
            temp += "| "
        print(temp)

#find potential tiles for an island
def returnPotentialTiles(table, chosenIsland, currentState):
    potentialNewTiles = []
    for item in chosenIsland.tiles:
        if neighbour(table, item[0], item[1], "up") == 0:
            setNeighbour(item[0], item[1], table, "up", -2)
            tempTiles = returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
                pass
            elif not checkWallIntegrity3(table, "undefined"):
                pass
            elif (item[0] - 1, item[1]) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0] - 1, item[1]))
            setNeighbour(item[0], item[1], table, "up", 0)
        if neighbour(table, item[0], item[1], "right") == 0:
            setNeighbour(item[0], item[1], table, "right", -2)
            tempTiles = returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
                pass
            elif not checkWallIntegrity3(table, "undefined"):
                pass
            elif (item[0], item[1] + 1) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0], item[1] + 1))
            setNeighbour(item[0], item[1], table, "right", 0)
        if neighbour(table, item[0], item[1], "down") == 0:
            setNeighbour(item[0], item[1], table, "down", -2)
            tempTiles = returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
                pass
            elif not checkWallIntegrity3(table, "undefined"):
                pass
            elif (item[0] + 1, item[1]) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0] + 1, item[1]))
            setNeighbour(item[0], item[1], table, "down", 0)
        if neighbour(table, item[0], item[1], "left") == 0:
            setNeighbour(item[0], item[1], table, "left", -2)
            tempTiles = returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
                pass
            elif not checkWallIntegrity3(table, "undefined"):
                pass
            elif (item[0], item[1] - 1) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0], item[1] - 1))
            setNeighbour(item[0], item[1], table, "left", 0)
    if len(potentialNewTiles) > 0:
        return potentialNewTiles
    else:
        return None

#update island tiles lists and also if they are complete
def updateIslands(consideredIslands, table):
    for island in consideredIslands:
        tiles = returnTiles(island.x, island.y, table)
        if len(tiles) < table[island.x][island.y]:
            island.complete = False
            island.tiles = copy.deepcopy(tiles)
        elif len(tiles) == table[island.x][island.y]:
            island.complete = True
        else:
            print("table looks like this:");
            printTableOld(table)
            print("Island", island.x, island.y, "too big, errored somewhere")
            print("Island", island.x, island.y, "tiles:", island.tiles)
            return

#return the next non-complete island
def chooseIsland(consideredIslands, chosenIsland):
    chosenIsland = None
    for island in consideredIslands:
        if not island.complete:
            chosenIsland = island
            break
    return chosenIsland

#checking function
def doChecks(table):
    flag = True
    if wallBlockCheck(table) == None:
        undefinedInTable = False
        for line in table:
            if 0 in line:
                undefinedInTable = True
        if not undefinedInTable:
            if allIslCheck(table):
                if checkWallIntegrity3(table):
                    pass
                else:
                    flag = False
            else:
                flag = False
        else:
            flag = False
    else:
        flag = False
    return flag

#############################################################

if __name__ == '__main__':
    # set x and y length of the table
    x_len = len(table)
    y_len = len(table[0])