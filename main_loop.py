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

"""tabelaBLANK =     [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]

tabela =     [[0, 0, 0, 0, 0],
              [0, 3, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 2, 0, 1],
              [3, 0, 0, 0, 0]]"""

tabela =     [[0, 0, 0, 0, 1, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [4, 0, 0, 0, 0, 0, 4],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 6],
              [0, 0, 6, 0, 0, 0, 0]]

"""tabela =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
[0, 0, 3, 0, 0, 0, 0, 3, 0, 0],
[0, 0, 0, 2, 0, 0, 4, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 3, 0, 1, 0, 0, 2, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 4, 0, 0],
[0, 1, 0, 0, 0, 0, 4, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]"""

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
def printStates(stateHistory):
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
    flag = True
    undefinedInTable = False
    for line in table:
        if 0 in line:
            undefinedInTable = True
    if ns.wallBlockCheck(table) == None:
        pass
    else:
        flag = False
    if ns.checkWallIntegrity3(table):
        pass
    else:
        flag = False
    if ns.allIslCheck(table):
        pass
    else:
        flag = False
    if not undefinedInTable:
        pass
    else:
        flag = False
    #ns.printTableOld(table)
    return flag

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
            tempTiles = ns.returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
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
            tempTiles = ns.returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
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
            tempTiles = ns.returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
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
            tempTiles = ns.returnTiles(chosenIsland.x, chosenIsland.y, table)
            counter = 0
            for tile in tempTiles:
                if table[tile[0]][tile[1]] > 0:
                    counter += 1
            if counter > 1:
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
            return
def chooseIsland(consideredIslands, chosenIsland):
    """if chosenIsland == None:
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
                    break"""
    chosenIsland = None
    for island in consideredIslands:
        if not island.complete:
            chosenIsland = island
            break
    return chosenIsland
###################################################################################
# <editor-fold desc="Init Stuff">
currentState = ns.state(tabela)
table = currentState.table


def solve(table, currentState):
    depth = 0
    stateHistory = []
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
            wall(table)
            print("Nurikabe complete")
            ns.printTableOld(table)
            return
    # </editor-fold>
    #####################################################################################################
    while depth < 10000:
        logicalMoves(table)
        tableCopy = copy.deepcopy(table)
        wall(tableCopy)
        if doChecks(tableCopy):
            wall(table)
            print("Nurikabe complete")
            ns.printTableOld(table)
            return
        if depth == 6106:
            print ("debug")
        if returningFromBadState == False:
            print("Not returning from bad state, table:"); ns.printTableOld(table); print("impossible moves:",currentState.impossibleMoves)
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
                    print("Nurikabe complete")
                    ns.printTable(table)
                    return
                else:
                    print("All islands complete but Nurikabe not solved"); returningFromBadState = True
            else:
            # -----------------------------------------------------------------------------------------------------------
            #Doing a supposition on the chosenIsland---------------------------------------------------------------------
                print("Searching tiles for",chosenIsland.x,chosenIsland.y)
                potentialTiles = returnPotentialTiles(table, chosenIsland, currentState)
                if potentialTiles == None:
                    wall(table)
                    if doChecks(table):
                        print("Nurikabe complete")
                        ns.printTable(table)
                        return
                    else:
                        print("No potential tiles for island, must go back"); returningFromBadState = True
                else:
                    currentState.lastMove = (potentialTiles[0][0],potentialTiles[0][1])
                    currentState.lastIsland = copy.deepcopy(chosenIsland)
                    if len(stateHistory) == 0:
                        stateHistory.append(copy.deepcopy(currentState))
                        print("appended to stateHistory before supposition:")
                    elif len(stateHistory) > 0 and table != stateHistory[len(stateHistory)-1].table:
                        stateHistory.append(copy.deepcopy(currentState))
                        print("appended to stateHistory before supposition:")
                    stateHistory[len(stateHistory)-1].lastMove = (potentialTiles[0][0],potentialTiles[0][1])

                    printStates(stateHistory)
                    currentState.lastIsland =copy.deepcopy(chosenIsland)
                    lastMove = (potentialTiles[0][0],potentialTiles[0][1])
                    table[potentialTiles[0][0]][potentialTiles[0][1]] = -2
                    print("appended", potentialTiles[0][0], potentialTiles[0][1], "to", chosenIsland.x, chosenIsland.y, "table looks like this:---------------")
                    ns.printTableOld(table)
            # -----------------------------------------------------------------------------------------------------------
            # -----------------------------------------------------------------------------------------------------------
        else:
            print ("coming back from a bad state")
            #pop but revert only to the original unsolved state if can stay on same island
            popped = False
            if returnPotentialTiles(stateHistory[len(stateHistory)-1].table, stateHistory[len(stateHistory)-1].lastIsland, stateHistory[len(stateHistory)-1]) == None:
                stateHistory.pop()
                popped = True
            #should take last move of this state and append it as impossible move to this state
            stateHistory[len(stateHistory) - 1].impossibleMoves.append(stateHistory[len(stateHistory)-1].lastMove)
            currentState = copy.deepcopy(stateHistory[len(stateHistory)-1])
            table = currentState.table
            returningFromBadState = False
        depth += 1
        print("going in depth",depth)

solve(table, currentState)
