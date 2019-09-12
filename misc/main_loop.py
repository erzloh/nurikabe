import nurikabe_solver as ns
import copy #answer from stack overflow by Sukrit Kalra, about how to do deepcopy
import pprint

if __name__ == '__main__':
    tabela =[[1, 0, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 0],
            [2, 0, 2, 0],
            [0, 0, 0, 0]]
    tabela = [[0,0,0,0,0],
             [2,0,0,2,0],
             [0,0,0,0,0],
             [3,0,1,0,0],
             [0,0,0,0,1]]
    tabela = [[0, 0, 2, 0, 1],
              [0, 0, 0, 0, 0],
              [0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0],
              [2, 0, 5, 0, 0]]

tabela =     [[0, 0, 2, 0, 1],
              [0, 0, 0, 0, 0],
              [0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0],
              [2, 0, 5, 0, 0]]

tabela =     [[0, 0, 0, 0, 0],
              [2, 0, 0, 0, 2],
              [0, 0, 0, 0, 0],
              [1, 0, 0, 2, 0],
              [0, 0, 0, 0, 0]]

currentState = ns.state(tabela)
table = currentState.table
#######################################################
#walling function
def wall(table):
    x_len = len(table)
    y_len = len(table[0])
    for i in range(x_len):
        for j in range(y_len):
            if table[i][j] == 0:
                table[i][j] = -1
#print states
def printStates(table):
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
#checking function
def doChecks(table):
    undefinedInTable = False
    for line in table:
        if 0 in line:
            undefinedInTable = True
    if ns.wallBlockCheck(table) == None and ns.checkWallIntegrity2(table) and ns.allIslCheck(table) and not undefinedInTable:
        ns.printTableOld(table)
        return True
    else:
        return False
#do logical moves
def logicalMoves(table):
    tempTable = []
    while tempTable != table:
        tempTable = copy.deepcopy(table)
        ns.wallAroundIslands(table)
        #print("table before addOneTileEverywhere from logicalMoves:")
        #ns.printTableOld(table)
        ns.addOneTileEverywhere(table)
        #print("table after addOneTileEverywhere from logicalMoves:")
        #ns.printTableOld(table)
        ns.surround(table)
#find potential tiles for an island
def returnPotentialTiles(table, chosenIsland, currentState):
    potentialNewTiles = []
    for item in chosenIsland.tiles:
        # <editor-fold desc="Finding the tiles in all directions">
        if ns.neighbour2(table, item[0], item[1], "up") == 0:
            table[item[0] - 1][item[1]] = -2
            if len(ns.returnTiles(chosenIsland.x, chosenIsland.y, table)) > table[chosenIsland.x][chosenIsland.y]:
                pass
            elif not ns.checkWallIntegrityIncludingUndefined(table):
                pass
            elif (item[0] - 1, item[1]) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0] - 1, item[1]))
            table[item[0] - 1][item[1]] = 0
        if ns.neighbour2(table, item[0], item[1], "right") == 0:
            table[item[0]][item[1] + 1] = -2
            if len(ns.returnTiles(chosenIsland.x, chosenIsland.y, table)) > table[chosenIsland.x][chosenIsland.y]:
                pass
            elif not ns.checkWallIntegrityIncludingUndefined(table):
                pass
            elif (item[0], item[1] + 1) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0], item[1] + 1))
            table[item[0]][item[1] + 1] = 0
        if ns.neighbour2(table, item[0], item[1], "down") == 0:
            table[item[0] + 1][item[1]] = -2
            if len(ns.returnTiles(chosenIsland.x, chosenIsland.y, table)) > table[chosenIsland.x][chosenIsland.y]:
                pass
            elif not ns.checkWallIntegrityIncludingUndefined(table):
                pass
            elif (item[0] + 1, item[1]) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0] + 1, item[1]))
            table[item[0] + 1][item[1]] = 0
        if ns.neighbour2(table, item[0], item[1], "left") == 0:
            table[item[0]][item[1] - 1] = -2
            if len(ns.returnTiles(chosenIsland.x, chosenIsland.y, table)) > table[chosenIsland.x][chosenIsland.y]:
                pass
            elif not ns.checkWallIntegrityIncludingUndefined(table):
                pass
            elif (item[0], item[1] - 1) in currentState.impossibleMoves:
                pass
            else:
                potentialNewTiles.append((item[0], item[1] - 1))
            table[item[0]][item[1] - 1] = 0
    if len(potentialNewTiles) > 0:
        return potentialNewTiles
    else:
        return None
def updateIslands(consideredIslands, table):
    for island in consideredIslands:
        tiles = ns.returnTiles(island.x, island.y, table)
        if len(tiles) < table[island.x][island.y]:
            island.complete = False
            island.tiles = copy.deepcopy(tiles)
            # print("tiles",tiles)
        elif len(tiles) == table[island.x][island.y]:
            # print("tiles",tiles)
            island.complete = True
        else:
            print("table looks like this:");
            ns.printTableOld(table)
            print("Island", island.x, island.y, "too big, errored somewhere")
            print("Island", island.x, island.y, "tiles:", island.tiles)
            exit(420)
def chooseIsland(consideredIslands, chosenIsland):
    if chosenIsland == None:
        for island in consideredIslands:
            if not island.complete:
                chosenIsland = island
                break
    else:
        if chosenIsland.complete:
            chosenIsland = None
            for island in consideredIslands:
                if not island.complete:
                    chosenIsland = island
                    break
    return chosenIsland
###################################################################################
# <editor-fold desc="Init Stuff">
depth = 0
stateHistory = []
#stateHistory.append(ns.state(copy.deepcopy(table))) #no need to do this maybe but it smplifies smth. "Yeah, whatever." - Franklin, Grand Theft Auto: V
ns.elimAdj(table)
ns.diagonal(table)
originalTable = copy.deepcopy(table)
returningFromBadState = False
lastMove = None
islandHistory = []
returningFromSameIsland = False
lastTouchedIsland = None
chosenIsland = None
#list of considered islands
consideredIslands = []
for i in range(len(table)):
    for j in range(len(table[0])):
        if table[i][j] > 0:
            if not ns.islandCheckNotTooBig(i, j, table, table[i][j]):
                consideredIslands.append(ns.island(i, j, table[i][j], table))
if len(consideredIslands) > 0:
    tableCopy = copy.deepcopy(table)
    wall(tableCopy)
    if doChecks(tableCopy):
        exit("success1")
# </editor-fold>
#####################################################################################################
while depth < 500:
    if returningFromBadState == False:
        print("Not returning from bad state, table:"); ns.printTableOld(table)
        # -----------------------------------------------------------------------------------------------------------
        # updating each considered island (mostly checking if complete) and choosing the first valid-----------------
        updateIslands(consideredIslands, table)
        #-----------------------------------------------------------------------------------------------------------
        #Choosing island--------------------------------------------------------------------------------------------
        chosenIsland = chooseIsland(consideredIslands, chosenIsland)
        # -----------------------------------------------------------------------------------------------------------
        #Handling case when all islands are complete-----------------------------------------------------------------
        if chosenIsland == None:
            wall(table)
            if doChecks(table):
                exit("success2")
            else:
                print("All islands complete but Nurikabe not solved"); returningFromBadState = True
        else:
        # -----------------------------------------------------------------------------------------------------------
        #Doing a supposition on the chosenIsland---------------------------------------------------------------------
            potentialTiles = returnPotentialTiles(table, chosenIsland, currentState)
            if potentialTiles == None:
                wall(table)
                if doChecks(table):
                    exit("success3")
                else:
                    print("No potential tiles for island, must go back"); returningFromBadState = True
            else:
                stateHistory.append(copy.deepcopy(currentState))
                print("appended to stateHistory before supposition:");printStates(table)
                islandHistory.append((chosenIsland.x, chosenIsland.y))
                lastMove = (potentialTiles[0][0],potentialTiles[0][1])
                table[potentialTiles[0][0]][potentialTiles[0][1]] = -2
                print("appended", potentialTiles[0][0], potentialTiles[0][1], "to", chosenIsland.x, chosenIsland.y, "table looks like this:")
                ns.printTableOld(table)
        # -----------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------
    else:
        #1: pop
        #2: append impossibleMoves
        stateHistory.pop()
        if len(stateHistory) == 0:
            currentState = ns.state(originalTable)
            currentState.impossibleMoves.append(lastMove)
            print("didn't pop stateHistory because it was empty")
        else:
            print("popped stateHistory:"); printStates(table)
            stateHistory[len(stateHistory)-1].impossibleMoves.append(lastMove)
            currentState = copy.deepcopy(stateHistory[len(stateHistory)-1])
            returningFromBadState = False
    depth += 1
    print("going in depth",depth)
