import sys, math

#Function to check if tile is an int (just a float function changed for name)
def isInt(table, x, y):
    flag = True
    try:
        int(table[x][y])
    except ValueError:
        flag = False
    return flag

#Function to check if a var is an int, must not be a tile
def isIntTwo(var):
    flag = True
    try:
        int(var)
    except ValueError:
        flag = False
    return flag

#Function to check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1-x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1-y2) == 1):
        touching = True
    return touching

#Function that returns a requested neighbour. Directions can be: up, down, right, left. "E" = edge
def neighbour(table, x, y, direction):
    if direction == "up":
        if y == 0:
            return "E"
        else:
            return table[x][y-1]
    if direction == "down":
        if y == len(table[0])-1:
            return "E"
        else:
            return table[x][y+1]
    if direction == "left":
        if x == 0:
            return "E"
        else:
            return table[x-1][y]
    if direction == "right":
        if x == len(table)-1:
            return "E"
        else:
            return table[x+1][y]

#Function to check if a single island is complete
tempTable = []
revertTable = []
def islandCheck(x, y, table, counter, returning = False):
    
    x_len = len(table)
    y_len = len(table[1])
    
    if (x, y) not in tempTable:
        counter = counter-1 #print("counter is",counter)
        if counter == 0: #print("Island complete")
            return True
        tempTable.append((x, y))
    if not returning:
        revertTable.append((x, y))
    if x > 0 and table[x-1][y] == "W" and (x-1, y) not in tempTable: #print("left")
        return islandCheck(x-1, y, table, counter, returning = False)
    elif y > 0 and table[x][y-1] == "W" and (x, y-1) not in tempTable: #print("up")
        return islandCheck(x, y-1, table, counter, returning = False)
    elif (x < x_len-1) and table[x+1][y] == "W" and (x+1, y) not in tempTable: #I wonder if the < x_len-1 works in all cases ###print("right")
        return islandCheck(x+1, y, table, counter, returning = False)
    elif (y < y_len-1) and table[x][y+1] == "W" and (x, y+1) not in tempTable: #print("down")        
        return islandCheck(x, y+1, table, counter, returning = False)
    elif len(revertTable) > 1:
        revertTable.pop() #print("returning")
        return islandCheck(revertTable[len(revertTable)-1][0], revertTable[len(revertTable)-1][1], table, counter, returning = True)
    else: #print("Island not complete")
        return False

#Function to return all island parts
partList = []
def islandParts(x, y, table, counter, returning = False):
    #print("iteration of islandParts on", x, y)
    x_len = len(table)
    y_len = len(table[1])
    if (x, y) not in tempTable:
        #print(x,y,"not in tempTable")
        counter = counter-1 #print("counter is",counter)
        partList.append((x, y))
        if counter == 0: #print("Island complete")
            return partList
        tempTable.append((x, y))
        #print("appended",x,y,"to partlist: ",partList)
    if not returning:
        revertTable.append((x, y))
    if x > 0 and table[x-1][y] == "W" and (x-1, y) not in tempTable: #print("left")
        return islandParts(x-1, y, table, counter, returning = False)
    elif y > 0 and table[x][y-1] == "W" and (x, y-1) not in tempTable: #print("up")
        return islandParts(x, y-1, table, counter, returning = False)
    elif (x < x_len-1) and table[x+1][y] == "W" and (x+1, y) not in tempTable: #I wonder if the < x_len-1 works in all cases ###print("right")
        return islandParts(x+1, y, table, counter, returning = False)
    elif (y < y_len-1) and table[x][y+1] == "W" and (x, y+1) not in tempTable: #print("down")        
        return islandParts(x, y+1, table, counter, returning = False)
    elif len(revertTable) > 1:
        revertTable.pop() #print("returning")
        return islandParts(revertTable[len(revertTable)-1][0], revertTable[len(revertTable)-1][1], table, counter, returning = True)
    else: #print("Island not complete")
        return False

#Function to turn tiles next to islands "B". It has two modes: "complete" and "everything". The complete mode will check if the island is complete before proceeding, the everything mode won't do that check.
def wallAroundIslands(table, mode="complete"):
    if mode == "complete":
        for i in range(x_len):
            for j in range(y_len):
                if isInt(table, i, j):
                    tempTable.clear()
                    revertTable.clear()
                    partList.clear()
                    if islandCheck(i, j, table, int(table[i][j])):
                        tempTable.clear()
                        revertTable.clear()
                        partList.clear()
                        tiles = islandParts(i, j, table, int(table[i][j]))

                        for tile in tiles:
                            if neighbour(table, tile[0], tile[1], "up") != "W" and neighbour(table, tile[0], tile[1], "up") != "E" and not isIntTwo(neighbour(table, tile[0], tile[1], "up")):
                                table[tile[0]][tile[1]-1] = "B"
                            if neighbour(table, tile[0], tile[1], "right") != "W" and neighbour(table, tile[0], tile[1], "right") != "E" and not isIntTwo(neighbour(table, tile[0], tile[1], "right")):
                                table[tile[0]+1][tile[1]] = "B"
                            if neighbour(table, tile[0], tile[1], "down") != "W" and neighbour(table, tile[0], tile[1], "down") != "E" and not isIntTwo(neighbour(table, tile[0], tile[1], "down")):
                                table[tile[0]][tile[1]+1] = "B"
                            if neighbour(table, tile[0], tile[1], "left") != "W" and neighbour(table, tile[0], tile[1], "left") != "E" and not isIntTwo(neighbour(table, tile[0], tile[1], "left")):
                                table[tile[0]-1][tile[1]] = "B"
                    else:
                        print("Could not put wall around island",i,j,". Not complete") #actually should not happen but who knows
    else:
        for i in range(x_len):
            for j in range(y_len):
                if isIntTwo(table[i][j]) or table[i][j] == "W":
                    if neighbour(table, i, j, "up") != "W" and neighbour(table, i, j, "up") != "E" and not isIntTwo(neighbour(table, i, j, "up")):
                        table[i][j-1] = "B"
                    if neighbour(table, i, j, "right") != "W" and neighbour(table, i, j, "right") != "E" and not isIntTwo(neighbour(table, i, j, "right")):
                        table[i+1][j] = "B"
                    if neighbour(table, i, j, "down") != "W" and neighbour(table, i, j, "down") != "E" and not isIntTwo(neighbour(table, i, j, "down")):
                        table[i][j+1] = "B"
                    if neighbour(table, i, j, "left") != "W" and neighbour(table, i, j, "left") != "E" and not isIntTwo(neighbour(table, i, j, "left")):
                        table[i-1][j] = "B"
                        
#tables
table = [["4", "W", "U"],
         ["U", "W", "U"],
         ["U", "W", "U"]]

table =[["U", "U", "1", "U", "W", "2"],
        ["1", "U", "U", "U", "U", "U"],
        ["U", "U", "2", "W", "U", "2"],
        ["W", "2", "U", "U", "U", "W"]]

#set x and y length of the table
x_len = len(table)
y_len = len(table[0])

#Function to display table in console
def printTable(table):
    tempStr = ""
    for i in range(y_len):
        for j in range(x_len):
            tempStr += table[j][i]+" "
        print(tempStr)
        tempStr = ""

##execute functions
#table = surround(table)

wallAroundIslands(table)
printTable(table)

#idea: to check if an island has got more tiles than it should, just redo a check with counter+1. If it succeeds that means the island is too big. genius.
