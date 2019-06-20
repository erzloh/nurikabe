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

#set x and y length of the table
x_len = len(table)
y_len = len(table[0])

##execute functions
#table = elimAroundOnes(table)

printTable(table)    
