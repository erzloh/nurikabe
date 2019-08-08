import nurikabeNumbers as ns
import copy #answer from stack overflow by Sukrit Kalra

def returnPotentialTiles(table, x, y): #not used
    tiles = ns.returnTiles(x, y, table)
    tiles = ns.returnTiles(x, y, table)
    potentialNewTiles = []
    for item in tiles:
        if ns.neighbour(table, x, y, "up") == 0:
            potentialNewTiles.append((x, y - 1))
        if ns.neighbour(table, x, y, "right") == 0:
            potentialNewTiles.append((x + 1, y))
        if ns.neighbour(table, x, y, "down") == 0:
            potentialNewTiles.append((x, y + 1))
        if ns.neighbour(table, x, y, "left") == 0:
            potentialNewTiles.append((x-1, y))
    return potentialNewTiles

table =[[1, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [2, 0, 2, 0],
        [0, 0, 0, 0]]

print("--------------------------------------")

def solve(table, depth = 0, max_depth = 500, firstRun = None, returningArray = None, cachedLastRun = None, returningFromBadSupposition = None, currentIsland = None, consideredIslands = None):
    # first launch functions:
    if firstRun == None:
        consideredIslands = []
        class island:
            def __init__(self, x, y, size):
                self.x = x
                self.y = y
                self.size = size
                self.lastTouched = False
                self.triedFailedTiles = []
                self.addedTilesHistory = []
                self.complete = False
                self.potentialNewTiles = returnPotentialTiles(table, self.x, self.y)
                self.tiles = ns.returnTiles(x, y, table)
        x_len = len(table)
        y_len = len(table[0])
        for i in range(x_len):
            for j in range(y_len):
                if table[i][j] > 0:
                    if len(ns.returnTiles(i, j, table)) < table[i][j]:
                        consideredIslands.append(island(i, j, table[i][j]))
        firstRun = False
        returningFromBadSupposition = False
        ns.elimAdj(table)
        ns.diagonal(table)
        print("hmm")
    if cachedLastRun == None:
        cachedLastRun = copy.deepcopy(table)
    #repetitive-use functions
    ns.wallAroundIslands(table)
    ns.addOneTileEverywhere(table)
    ns.surround(table)
    if cachedLastRun == table and depth < max_depth:
        if currentIsland == None:
            for item in consideredIslands:
                if not item.complete:
                    currentIsland = (item)
                    break
            if currentIsland == None:
                print("Should initiate an all-walling operation and a final check")
                x_len = len(table)
                y_len = len(table[0])
                for i in range(x_len):
                    for j in range(y_len):
                        if table[i][j] == 0:
                            table [i][j] = -1
                if ns.wallBlockCheck(table) == None and ns.checkWallIntegrity2(table) and ns.allIslCheck(table):
                    print("Nurikabe complete")
                else:
                    print("fricked up")
                return
        #add one tile randomly to the current island and check for errors. If none, relaunch the function.
        #There must be a list of all uncomplete islands. Each island should be an object with the following properties: x, y, alreadyTriedCoordsList.
        #here --->
        foundPotentialTile = False
        for item in currentIsland.potentialNewTiles:
            if item not in currentIsland.triedFailedTiles:
                #hmm already mark the field as part of the island. WCGW?
                table[item[0]][item[1]] = -2
                # run a consistency check on the island to know if it hasn't been merged with another one, bruh
                if len(ns.returnTiles(currentIsland.x, currentIsland.y, table)) > table[currentIsland.x][
                    currentIsland.y]:
                    print("merged with another island, removing that island tile")
                    table[item[0]][item[1]] = 0
                    currentIsland.triedFailedTiles.append(item)
                #check if some wall has been excluded from the rest, for now using my own *so proud* wall continuity algorithm. It also accepts "0" as wall.
                elif not ns.checkWallIntegrityIncludingUndefined(table):
                    print("blocked access to the rest of the wall, removing that island tile")
                    table[item[0]][item[1]] = 0
                    currentIsland.triedFailedTiles.append(item)
                #regenerate the potentialTiles list for the island:
                else:
                    currentIsland.potentialNewTiles = returnPotentialTiles(table, currentIsland.x, currentIsland.y)
                currentIsland.lastTouched = True
                foundPotentialTile = True
                break
        if not foundPotentialTile:
            currentIsland.complete = True
            currentIsland.lastTouched = False
            currentIsland = None
        #########################################
        depth += 1
        print("depth", depth)
        cachedLastRun = copy.deepcopy(table)
        return solve(table, depth, max_depth, firstRun, returningArray, cachedLastRun, returningFromBadSupposition, currentIsland, consideredIslands)
    elif depth < max_depth and cachedLastRun != table:
        depth += 1
        print("depth", depth)
        cachedLastRun = copy.deepcopy(table)
        return solve(table, depth, max_depth, firstRun, returningArray, cachedLastRun, returningFromBadSupposition, currentIsland, consideredIslands)
    elif depth >= max_depth:
        print("exceeded max_depth, exiting")
        return
    elif ns.wallBlockCheck(table) == None and ns.checkWallIntegrity2(table) and ns.allIslCheck(table):
        print("Nurikabe complete")
        return


solve(table)
ns.printTableOld(table)
