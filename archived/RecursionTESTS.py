import sys, math
#check if tile is an int (just a float function changed for name)
def isInt(table, x, y):
    val = True
    try:
        int(table[x][y])
    except ValueError:
        val = False
    return val

#check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1-x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1-y2) == 1):
        touching = True
    return touching

#check continuity of the wall
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
                    setList.append([(i, j)])
    #print(setList)
    for i in range(len(setList)):
        setList[i] = set(setList[i])
    #print(setList)
    #if (len(setList[0] & setList[1])) > 0:
        #pass #print("hello")
    i = 0
    while i < len(setList) - 1:
        j = 1
        while j < len(setList):
            if (len(setList[i] & setList[j])) > 0 and not(setList[i] == setList[j]):
                setList[i] = setList[i] | setList[j]
                del setList[j]
                j = 1
            else:
                j += 1
        i += 1
    #verify if there is one or more sets
    #print(setList)
    if len(setList) > 1:
        print("The wall is not continuous")
    else:
        print("The wall is continuous")

#turn tiles between numbers black "B"
def elimAdj(table):
    for i in range(x_len):
        for j in range(y_len):
            #check in the right direction
            if (i < (x_len-2)) and isInt(table, i,j) and isInt(table, i+2,j):
                table[i+1][j] = "B"
            #check below
            if (j < (y_len-2)) and isInt(table, i,j) and isInt(table, i,j+2):
                table[i][j+1] = "B"
    return table

#turns tiles next to "ones" black ("B")
def elimAroundOnes(table):
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == "1":
                if i > 0: #left
                    table[i-1][j] = "B"
                if j > 0: #up
                    table[i][j-1] = "B"
                if i < x_len-1: #right
                    table[i+1][j] = "B"
                if j < y_len-1: #down
                    table[i][j+1] = "B"
    return table

#turns tiles in diagonal black ("B")
def diagonal(table):
    for i in range(x_len):
        for j in range(y_len):
            # case n°1: "2" "w"
            #           "w" "2"
            if i < x_len-1 and j < y_len-1:
                if isInt(table, i,j) and isInt(table, i+1,j+1):
                    table[i+1][j] = "B"
                    table[i][j+1] = "B"
            # case n°1: "w" "2"
            #           "2" "w"
                if isInt(table, i+1,j) and isInt(table, i,j+1):
                    table[i][j] = "B"
                    table[i+1][j+1] = "B"
    return table

#check for 2x2 wall blocks
def wallBlockCheck(table):
    foundBlock = False
    for i in range(x_len-1):
        for j in range(y_len-1):
            if table[i][j] == "B" and table[i+1][j] == "B" and table[i][j+1] == "B" and table[i+1][j+1] == "B":
                foundBlock = True
                print("2x2 wall block found at x:",i,"and y:",j)
    if not foundBlock:
        print("No 2x2 blocks in the wall")

#display table in console
def printTable(table):
    tempStr = ""
    for i in range(y_len):
        for j in range(x_len):
            tempStr += table[j][i]+" "
        print(tempStr)
        tempStr = ""

#new table
"""table =[["B", "B", "1", "B", "I", "2"],
        ["1", "B", "B", "B", "Q", "B"],
        ["B", "B", "2", "I", "B", "2"],
        ["I", "2", "B", "B", "B", "I"]]"""
#new table
table =[["B", "B", "1", "B", "I", "2"],
        ["1", "B", "B", "B", "B", "B"],
        ["B", "B", "2", "I", "B", "2"],
        ["I", "2", "B", "B", "B", "I"]]

table = [["1", "B", "2", "I", "B", "2", "I"],
         ["B", "B", "B", "B", "B", "B", "B"],
         ["2", "I", "B", "4", "M", "B", "1"],
         ["B", "B", "I", "I", "B", "B", "B"],
         ["2", "B", "B", "B", "2", "I", "B"],
         ["I", "B", "4", "B", "B", "B", "B"],
         ["B", "B", "I", "I", "I", "B", "1"]]


#set x and y length of the table
x_len = len(table)
y_len = len(table[0])

#execute functions
#table = elimAroundOnes(table)
#table = elimAdj(table)
#table = diagonal(table)
#wallBlockCheck(table)
#completeIslands(table)

#checkWallIntegrity(table)

#printTable(table)

#recursion test
def factorielle(n):
    if n > 1:
        return n * factorielle(n-1)
    else:
        return 1
#print(factorielle(3))

printTable(table)

tempTable = []
counter = int(table[2][3])
revertTable = []
print("counter is",counter)
def islandCheck(x, y, table, counter, returning = False):
    print("revertTable length:",len(revertTable))
    if (x, y) not in tempTable:
        counter = counter-1
        print("counter is",counter)
        if counter == 0:
            print("Island complete")
            return True
        tempTable.append((x, y))
    print("tempTable:",tempTable)
    if not returning:
        revertTable.append((x, y))
    if x > 0 and table[x-1][y] == "I" and (x-1, y) not in tempTable:
        print("left")
        return islandCheck(x-1, y, table, counter, returning = False)
    elif y > 0 and table[x][y-1] == "I" and (x, y-1) not in tempTable:
        print("up")
        return islandCheck(x, y-1, table, counter, returning = False)
    elif (x < x_len-1) and table[x+1][y] == "I" and (x+1, y) not in tempTable: #I wonder if the < x_len-1 works in all cases
        print("right")
        return islandCheck(x+1, y, table, counter, returning = False)
    elif (y < y_len-1) and table[x][y+1] == "I" and (x, y+1) not in tempTable:
        print("down")
        return islandCheck(x, y+1, table, counter, returning = False)
    elif len(revertTable) > 1:
        revertTable.pop()
        print("returning")
        return islandCheck(revertTable[len(revertTable)-1][0], revertTable[len(revertTable)-1][1], table, counter, returning = True)
    else:
        print("island not complete")
        return False
#!!DON'T FORGET TO RESET VARIABLES BEFORE SECOND FUNCTION CALL!!

print(islandCheck(2, 3, table, counter))
