# Nurikabe solver part
# By Jacek Wikiera
# last edit 27 april 19 - 22:45

import sys, math


# check if tile is an int (just a float function changed for name)
def isInt(table, x, y):
    val = True
    try:
        int(table[x][y])
    except ValueError:
        val = False
    return val


# check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1 - x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1 - y2) == 1):
        touching = True
    return touching


# check continuity of the wall
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

    print(setList)
    for i in range(len(setList)):
        setList[i] = set(setList[i])
    print(setList)

    if (len(setList[0] & setList[1])) > 0:
        print("hello")

    i = 0
    j = 0
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

    print(setList)
    if len(setList) > 1:
        print("La mer n'est pas continue")
    else:
        print("La mer est continue")


# turn tiles between numbers black "B"
def elimAdj(table):
    for i in range(x_len):
        for j in range(y_len):
            # check in the right direction
            if (i < (x_len - 2)) and isInt(table, i, j) and isInt(table, i + 2, j):
                table[i + 1][j] = "B"
            # check below
            if (j < (y_len - 2)) and isInt(table, i, j) and isInt(table, i, j + 2):
                table[i][j + 1] = "B"
    return table


# turns tiles next to "ones" black ("B")
def elimAroundOnes(table):
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


# turns tiles in diagonal black ("B")
def diagonal(table):
    for i in range(x_len):
        for j in range(y_len):
            # case n1: "2" "w"
            #          "w" "2"
            if i < x_len - 1 and j < y_len - 1:
                if isInt(table, i, j) and isInt(table, i + 1, j + 1):
                    table[i + 1][j] = "B"
                    table[i][j + 1] = "B"
                # case n2: "w" "2"
                #          "2" "w"
                if isInt(table, i + 1, j) and isInt(table, i, j + 1):
                    table[i][j] = "B"
                    table[i + 1][j + 1] = "B"
    return table


# output table in console
def printTable(table):
    tempStr = ""
    for i in range(y_len):
        for j in range(x_len):
            tempStr += table[j][i] + " "
        print(tempStr)
        tempStr = ""


# old table
table = ["w", "1", "w", "w",
         "w", "w", "w", "2",
         "1", "w", "2", "w",
         "w", "w", "w", "w",
         "w", "w", "w", "w",
         "2", "w", "2", "w"]
# new table
table = [["w", "w", "1", "w", "w", "2"],
         ["1", "w", "w", "w", "w", "w"],
         ["w", "w", "2", "w", "w", "2"],
         ["w", "2", "w", "w", "w", "w"]]

# set x and y length of the table
x_len = len(table)
y_len = len(table[0])

# execute functions
table = elimAroundOnes(table)
table = elimAdj(table)
table = diagonal(table)
checkWallIntegrity(table)

printTable(table)
