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

tabela = [[0, 0, 2, 0, 1],
              [0, 0, 0, 0, 0],
              [0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0],
              [2, 0, 5, 0, 0]]

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
    if ns.wallBlockCheck(table) == None and ns.checkWallIntegrity2(table) and ns.allIslCheck(table):
        ns.printTableOld(table)
        return  True
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
###################################################################################
# <editor-fold desc="Init Stuff">
dephth = 0
stateHistory = []
stateHistory.append(ns.state(copy.deepcopy(table))) #no need to do this maybe but it smplifies smth. "Yeah, whatever." - Franklin, Grand Theft Auto: V
ns.elimAdj(table)
ns.diagonal(table)
returningFromBadState = False
wasInBadState = False
lastMove = None
islandHistory = []
returningFromSameIsland = False
#list of considered islands
consideredIslands = []
for i in range(len(table)):
    for j in range(len(table[0])):
        if table[i][j] > 0:
            if not ns.islandCheckNotTooBig(i, j, table, table[i][j]):
                consideredIslands.append(ns.island(i, j, table[i][j], table))
# </editor-fold>
while dephth < 500:
    if dephth == 6:
        print("dephth 6, debug")
    #do logical moves
    # <editor-fold desc="Logical moves">
    logicalMoves(table)
    # </editor-fold>
    #Check if Nurikabe is complete
    if doChecks(table):
        print("Nurikabe complete1"); exit("success")
#--------------------------------------------------------------------------------------
    #not bad state
    if not returningFromBadState:
        # updating each considered island (mostly checking if complete) and choosing the first valid
        for island in consideredIslands:
            tiles = ns.returnTiles(island.x, island.y, table)
            if len(tiles) < table[island.x][island.y]:
                island.complete = False
                island.tiles = copy.deepcopy(tiles)
                #print("tiles",tiles)
            elif len(tiles) == table[island.x][island.y]:
                #print("tiles",tiles)
                island.complete = True
            else:
                print("table looks like this:"); ns.printTableOld(table)
                print("Island",island.x,island.y,"too big, errored somewhere")
                print("Island",island.x,island.y,"tiles:",island.tiles)
                exit(420)

        # chosen island
        theChosenOne = None
        for island in consideredIslands:
            if not island.complete:
                theChosenOne = island
                break
        # if no islands exist, check if nurikabe complete, if not, go back. "Ah sh*t, here we go again." -Carl Johnson, Grand Theft Auto: San Andreas
        if theChosenOne == None:
            # wall everything that is null
            wall(table)
            # do the checks
            if doChecks(table):
                exit("success")
            else:
                print("All islands are complete but the Nurikabe is not solved. Returning from bad state")
                returningFromBadState = True
        #if there is an available island:
        else:
            #get all potential new tiles
            print("Finding potential new tiles for",theChosenOne.x,theChosenOne.y,", the current table looks like this:")
            ns.printTableOld(table)
            print("its impossible moves are:",currentState.impossibleMoves)
            #here I realized that instead of having the "table", I should have a state with impossible moves.
            potentialNewTiles = []
            for item in theChosenOne.tiles:
                # <editor-fold desc="Finding the tiles in all directions">
                if ns.neighbour2(table, item[0], item[1], "up") == 0:
                    table[item[0] - 1][item[1]] = -2
                    if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
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
                    if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
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
                    if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
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
                    if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
                        pass
                    elif not ns.checkWallIntegrityIncludingUndefined(table):
                        pass
                    elif (item[0], item[1] - 1) in currentState.impossibleMoves:
                        pass
                    else:
                        potentialNewTiles.append((item[0], item[1] - 1))
                    table[item[0]][item[1] - 1] = 0
                # </editor-fold>
            #if there are available potentialNewTiles:
            if len(potentialNewTiles) > 0:
                #doing the supposed move, backing up state before it.
                #Maybe it's here that I must pop the state list. idk
                if returningFromSameIsland:
                    print("Operating on the same island as before, not appending table to stateHistory")
                else:
                    print("Not operating on the same island as before, appending table to stateHistory")
                    stateHistory.append(ns.state(copy.deepcopy(table)))
                table[potentialNewTiles[0][0]][potentialNewTiles[0][1]] = -2
                lastMove = (potentialNewTiles[0][0], potentialNewTiles[0][1])
                islandHistory.append(theChosenOne)
                print("Found",potentialNewTiles[0][0],potentialNewTiles[0][1], "as a tile and appended to island",theChosenOne.x, theChosenOne.y)
                print("the table looks like this:")
                ns.printTableOld(table)
            #if there are no potentialNewTiles available:
            else:
                print("No available potentialNewTiles")
                print("table looks like this:"); ns.printTableOld(table)
                #check if nurikabe is complete
                wall(table)
                if doChecks(table):
                    exit(3)
                else:
                    returningFromBadState = True
#----------------------------------------------------------------------------------------------
    #returning from bad state
    else:
        #maybe pop here, who knows
        print("returning from a bad state, the table is like this:")
        ns.printTableOld(table)
        print("stateHistory:")
        printStates(table)
        #pop only if changing island. Or, maybe pop but before popping transfer all impossible moves to the one before last state. Only pass it the lastIsland does not change.
        #I guess there should be a check for island change here. Like, listing all possible moves again and seeing if there are any left.
        #FIRST: the last state should be reverted now because it makes no sense to do any potentialNewTiles checks now
        currentState = copy.deepcopy(stateHistory[len(stateHistory)-1])
        print("currentState is now the last element from the state history, it looks like this and its impossibleMoves follow:")
        ns.printTableOld(currentState.table)
        print(currentState.impossibleMoves)
        currentState.impossibleMoves.append(lastMove)
        print("appended last move,",lastMove,", to currentState.impossibleMoves")
        #Look for all possible moves for lastIsland:
        theChosenOne = copy.deepcopy(islandHistory[len(islandHistory) - 1])
        potentialNewTiles = []
        table = currentState.table
        for item in theChosenOne.tiles:
            # <editor-fold desc="Finding the tiles in all directions">
            if ns.neighbour2(table, item[0], item[1], "up") == 0:
                table[item[0] - 1][item[1]] = -2
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
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
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
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
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
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
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
                    pass
                elif not ns.checkWallIntegrityIncludingUndefined(table):
                    pass
                elif (item[0], item[1] - 1) in currentState.impossibleMoves:
                    pass
                else:
                    potentialNewTiles.append((item[0], item[1] - 1))
                table[item[0]][item[1] - 1] = 0
            # </editor-fold>
        if len(potentialNewTiles) > 0:
            returningFromSameIsland = True
            stateHistory[len(stateHistory)-1].impossibleMoves = copy.deepcopy(currentState.impossibleMoves)
            pass
        else:
            returningFromSameIsland = False
            stateHistory.pop()
        table = copy.deepcopy(stateHistory[len(stateHistory)-1].table)
        returningFromBadState = False
        wasInBadState = True



#----------------------------------------------
    dephth += 1
    print("going in dephth",dephth,"")

ns.printTableOld(table)
