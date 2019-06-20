import sys, math

#Function to check if tile is an int (just a float function changed for name)
def isInt(table, x, y):
    flag = True
    try:
        int(table[x][y])
    except ValueError:
        flag = False
    return flag

#Function to check if two given tiles are touching
def areTouching(x1, y1, x2, y2):
    touching = False
    if (abs(x1-x2) == 1 and y2 == y1) or (x2 == x1 and abs(y1-y2) == 1):
        touching = True
    return touching
    
#tables
table = [["1", "B", "2", "W", "B", "2", "W"],
         ["B", "B", "B", "B", "B", "B", "B"],
         ["2", "W", "B", "4", "W", "B", "1"],
         ["B", "B", "W", "W", "B", "B", "B"],
         ["2", "B", "B", "B", "2", "W", "B"],
         ["W", "B", "4", "B", "B", "B", "B"],
         ["B", "B", "W", "W", "W", "B", "1"]]
         
table =[["B", "B", "1", "B", "W", "2"],
        ["1", "B", "B", "B", "B", "B"],
        ["B", "B", "2", "W", "B", "2"],
        ["W", "2", "B", "B", "B", "W"]]

table = [["U", "B", "U"],
         ["B", "U", "B"],
         ["U", "B", "U"]]

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

#Function to turn a "U" in "B" if surrounded by "B" or edge
def surround(table):
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == "U" and (neighbour(table,i,j,"up")=="E" or neighbour(table,i,j,"up")=="B") and (neighbour(table,i,j,"down")=="E" or neighbour(table,i,j,"down")=="B") and (neighbour(table,i,j,"left")=="E" or neighbour(table,i,j,"left")=="B") and (neighbour(table,i,j,"right")=="E" or neighbour(table,i,j,"right")=="B"):
                table[i][j] = "B"
    return table
    
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
table = surround(table)
#print(neighbour(table, 0, 0, "left"))

printTable(table)
