# There's a backup of this script named "main_loop3copy - backup2 - beforeRestruct.py". It's just before "restructurization".
# Let's say I have two incomplete islands. I go through their first possibilties without a problem. Then, at the end, I do checks but they fail, because, for eg.,
# there are 2x2 tiles in the Nurikabe. Normally that happens: I go to the last island, I go to it last tile, blacklist it for the tile just before etc.
# Then, let's say, the 2x2 block is the first islands fault. So, the function hs to go back to it, BLACKLISTING EVERY MOVE FROM THE SECONS ISLAND. Because of
# that, if the first island gets his second, non-blacklisted move executed, no moves can be done on the second island. I must rethink this whole
# "impossibleIslands" thing or it's not gonna work at all. Maybe remember the states? Keep a SET, not a list, of nurikabe states. Then, before doing any
# move, I would check if that state doesn't have this movement forbidden. Must document it, teacher talked od rolling back, and it doesn't seem to
# be the easiest thing to do.
# OR, JUST link blacklists to states and if the state gets removed from stateHistory remove them with it
import nurikabe_solver as ns
import copy #answer from stack overflow by Sukrit Kalra, about how to do deepcopy

if __name__ == '__main__':
    table =[[1, 0, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 0],
            [2, 0, 2, 0],
            [0, 0, 0, 0]]
    table = [[0,0,0,0,0],
             [2,0,0,2,0],
             [0,0,0,0,0],
             [3,0,1,0,0],
             [0,0,0,0,1]]
    """table = [[0,0,0],
             [0,1,0],
             [0,0,0]]"""
    """table = [[0, 0, 0, 1],
             [2, 0, 0, 0],
             [0, 0, 0, 1]]"""

ns.printTableOld(table)

def solve(table, originalTable = None, firstRun = None, dephth = None, consideredIslands = None, stateHistory = None, islandHistory = None, returningFromBadSupposition = None, stateMovesRegistry = None):
    if firstRun == None:
        originalTable = copy.deepcopy(table)
        firstRun = False
        dephth = 0
        stateHistory = ns.state()
        islandHistory = []
        returningFromBadSupposition = False
        stateMovesRegistry = []
                #lastState = copy.deepcopy(table)
                #supposition = False
                #returningFromBadSup = False
        ns.elimAdj(table)
        ns.diagonal(table)
        #list of considered islands
        consideredIslands = []
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j] > 0:
                    if not ns.islandCheckNotTooBig(i, j, table, table[i][j]):
                        consideredIslands.append(ns.island(i, j, table[i][j], table))
                        #consideredIslands[len(consideredIslands) - 1].tiles = ns.returnTiles(i, j, table)
    #solving functions
    ns.wallAroundIslands(table)
    ns.addOneTileEverywhere(table)
    ns.surround(table)
    #-------------------------------------------------------------------
    #check if Nurikabe solved
    if ns.wallBlockCheck(table) == None and ns.checkWallIntegrity2(table) and ns.allIslCheck(table):
        print("Nurikabe complete")
        ns.printTableOld(table)
        return
    #check if dephth is not too big
    elif dephth >= 500:
        print("exceeded maximum recursion dephth set, exiting")
        ns.printTableOld(table)
        return
    #supposition
    elif not returningFromBadSupposition:
        #i need a whole table history but also each island should have its own list (it's generated each time) of possible moves and a history of such moves that can be reverted.
        #When the function arrives at a state where no further moves are possible, the function should go back of one state and also
        #remember which island was the last tampered with. That island should have a 2d array keeping moves impossible to do one after the other.
        #When the function goes back, it rerolls the state and also takes the last two added parts and adds the last to the one before last as impossible.

        # updating each considered island (mostly checking if complete) and choosing the first valid
        for island in consideredIslands:
            if len(ns.returnTiles(island.x, island.y, table)) < table[island.x][island.y]:
                island.complete = False
            elif len(ns.returnTiles(island.x, island.y, table)) == table[island.x][island.y]:
                island.complete = True
            else:
                print("Island too big, errored somewhere"); exit(420)

        #chosen island, TODO: handle the case where no islands are available. aka check if nurikabe complete, if not, go back one step
        theChosenOne = None
        for island in consideredIslands:
            if not island.complete:
                theChosenOne = island
                break
        #if no islands exist, check if nurikabe complete, if not, go back. "Ah sh*t, here we go again." -Carl Johnson, Grand Theft Auto: San Andreas
        if theChosenOne == None:
            #wall everything that is null
            x_len = len(table)
            y_len = len(table[0])
            for i in range(x_len):
                for j in range(y_len):
                    if table[i][j] == 0:
                        table[i][j] = -1
            #do the checks
            if ns.wallBlockCheck(table) == None and ns.checkWallIntegrity2(table) and ns.allIslCheck(table):
                print("Nurikabe complete2")
                ns.printTableOld(table)
                return
            else:
                print("fricked up")
                dephth += 1
                return solve(table, originalTable, firstRun, dephth, consideredIslands, stateHistory, islandHistory, True, stateMovesRegistry)
        #list possible tiles, the two checks should be included + if the combination is not forbidden
        #tiles = returnTiles(theChosenOne.x, theChosenOne.y, table)
        potentialNewTiles = []
        for item in theChosenOne.tiles:
            if ns.neighbour2(table, item.x, item.y, "up") == 0:
                table[item.x-1][item.y] = -2
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
                    pass
                elif not ns.checkWallIntegrityIncludingUndefined(table):
                    pass
                elif (item.x - 1, item.y, len(stateHistory.impossibleMoves)-1) in stateHistory.impossibleMoves:
                    pass
                else:
                    potentialNewTiles.append((item.x - 1, item.y))
                table[item.x - 1][item.y] = 0
            if ns.neighbour2(table, item.x, item.y, "right") == 0:
                table[item.x][item.y+1] = -2
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
                    pass
                elif not ns.checkWallIntegrityIncludingUndefined(table):
                    pass
                elif (item.x, item.y+1, len(stateHistory.impossibleMoves)-1) in stateHistory.impossibleMoves:
                    pass
                else:
                    potentialNewTiles.append((item.x, item.y + 1))
                table[item.x][item.y + 1] = 0
            if ns.neighbour2(table, item.x, item.y, "down") == 0:
                table[item.x + 1][item.y] = -2
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
                    pass
                elif not ns.checkWallIntegrityIncludingUndefined(table):
                    pass
                elif (item.x + 1, item.y, len(stateHistory.impossibleMoves)-1) in stateHistory.impossibleMoves:
                    pass
                else:
                    potentialNewTiles.append((item.x + 1, item.y))
                table[item.x + 1][item.y] = 0
            if ns.neighbour2(table, item.x, item.y, "left") == 0:
                table[item.x][item.y-1] = -2
                if len(ns.returnTiles(theChosenOne.x, theChosenOne.y, table)) > table[theChosenOne.x][theChosenOne.y]:
                    pass
                elif not ns.checkWallIntegrityIncludingUndefined(table):
                    pass
                elif (item.x, item.y-1, len(stateHistory.impossibleMoves)-1) in stateHistory.impossibleMoves:
                    pass
                else:
                    potentialNewTiles.append((item.x, item.y-1))
                table[item.x][item.y - 1] = 0
        #tiles selected:
        print("dephth is",dephth)
        if dephth == 13:
            print("len of potentialNewTiles is", len(potentialNewTiles))
        #hmmm if no tiles, going back. WCGW
        if len(potentialNewTiles) == 0:
            dephth += 1
            #going bacc from a bad supposition/state
            return solve(table, originalTable, firstRun, dephth, consideredIslands, stateHistory, islandHistory, True, stateMovesRegistry)
        tileX = potentialNewTiles[0][0]
        tileY = potentialNewTiles[0][1]

        #do a table backup, remember which island the supposition was from
        stateHistory.tables.append(copy.deepcopy(table))
        stateMovesRegistry.append((table, []))
        print("stateHistory:",stateHistory.tables)
        islandHistory.append(theChosenOne)
        #if the tile exists in ANY unusedTiles (from any island), move it to tiles of theChosenOne
        exists = False
        for element in consideredIslands:
            for element2 in element.unusedTiles:
                if element2.x == tileX and element2.y == tileY:
                    theChosenOne.tiles.append(element2)
                    theChosenOne.addedTilesHistory.append(element2)
                    element.unusedTiles.remove(element2)
                    exists = True
        #if it doesn't exist, create a new tile object and append it to theChosenOne tiles and its tiles
        if not exists:
            tempIsland = ns.tile(tileX, tileY)
            theChosenOne.addedTilesHistory.append(tempIsland)
            theChosenOne.tiles.append(tempIsland)
        #do the supposition
        table[tileX][tileY] = -2
        print("added", tileX, tileY, "to", theChosenOne.x, theChosenOne.y, ", table looks like this:")
        ns.printTableOld(table)
        #rerun the function, not returning from a bad supposition
        dephth += 1
        return solve(table, originalTable, firstRun, dephth, consideredIslands, stateHistory, islandHistory, False, stateMovesRegistry)
    #if returning from a bad supposition
    else:
        print("Returned from a bad supposition, stateHistory is",stateHistory.tables)

        print("table should be returned to this state:",stateHistory.tables[len(stateHistory.tables)-1])
        #print("the last island touched was:",islandHistory[len(stateHistory)-1].x,islandHistory[len(stateHistory)-1].y)
        lastIsland = None
        if len(islandHistory) > 0:
            lastIsland = islandHistory[len(islandHistory)-1]
        #print("its last tile added was:",islandHistory[len(stateHistory)-1].addedTilesHistory[len(islandHistory[len(stateHistory)-1].addedTilesHistory)-1].x, islandHistory[len(stateHistory)-1].addedTilesHistory[len(islandHistory[len(stateHistory)-1].addedTilesHistory)-1].y)

        #remove the latest stateHistory state while being able to restart the function with it (rerun the function with tempTable as the table argument)
        tempTable = copy.deepcopy(stateHistory.tables[len(stateHistory.tables)-1])
        stateHistory.tables.pop()
        if len(stateHistory.tables) == 0:
            stateHistory.tables.append(copy.deepcopy(originalTable))
            print("popped stateHistory")

        #move the latest tile from the latest islands tiles to its unusedTiles and mark it as impossible from the one tile before
        if lastIsland != None:
            for element in lastIsland.tiles:
                if element.x == lastIsland.addedTilesHistory[len(lastIsland.addedTilesHistory)-1].x and element.y == lastIsland.addedTilesHistory[len(lastIsland.addedTilesHistory)-1].y:
                    lastIsland.unusedTiles.append(element)
                    lastIsland.tiles.remove(element)
                    #put last tile in current table of stateHistory instead in the current island
                    ##lastIsland.tiles[len(lastIsland.tiles)-1].impossibleMoves.append((lastIsland.unusedTiles[len(lastIsland.unusedTiles)-1].x, lastIsland.unusedTiles[len(lastIsland.unusedTiles)-1].y))
                    impossibleX = lastIsland.unusedTiles[len(lastIsland.unusedTiles)-1].x
                    impossibleY = lastIsland.unusedTiles[len(lastIsland.unusedTiles)-1].y
                    index = len(stateHistory.impossibleMoves)-1
                    stateHistory.impossibleMoves.append((impossibleX, impossibleY, index))
        #pop the latest island
        if len(islandHistory) > 0:
            islandHistory.pop()

        #rerun the function and mark it as returning from a good state, cheeki breeki
        dephth += 1
        return solve(tempTable, originalTable, firstRun, dephth, consideredIslands, stateHistory, islandHistory, False, stateMovesRegistry)














if __name__ == '__main__':
    solve(table)
    print("------------")
    #ns.printTableOld(table)
