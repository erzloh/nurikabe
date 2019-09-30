import functions as fn
import copy  # answer from stack overflow by Sukrit Kalra, about how to do deepcopy
# import numpy as np

def solve(table, currentState):
    depth = 0
    stateHistory = []
    fn.elimAdj(table)
    fn.diagonal(table)
    originalTable = copy.deepcopy(table)
    returningFromBadState = False
    lastMove = None
    islandHistory = []
    returningFromSameIsland = False
    lastTouchedIsland = None
    chosenIsland = None
    # list of considered islands
    consideredIslands = []
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] > 0:
                if not fn.islandCheckNotTooBig(i, j, table, table[i][j]):
                    consideredIslands.append(fn.island(i, j, table[i][j]))
    if len(consideredIslands) > 0:
        tableCopy = copy.deepcopy(table)
        fn.wall(tableCopy)
        if fn.doChecks(tableCopy):
            fn.wall(table)
            print("Nurikabe complete")
            fn.printTableOld(table)
            return table
    # main loop:
    while depth < 10000:
        if depth == 12:
            print("debug")
        fn.logicalMoves(table)
        tableCopy = copy.deepcopy(table)
        fn.wall(tableCopy)
        if fn.doChecks(tableCopy):
            fn.wall(table)
            print("Nurikabe complete")
            fn.printTableOld(table)
            return table
        if depth == 6106:
            print("debug")
        if returningFromBadState == False:
            print("Not returning from bad state, table:")
            fn.printTableOld(table)
            print("impossible moves:", currentState.impossibleMoves)
            # updating each considered island (mostly checking if complete) and choosing the first valid
            fn.updateIslands(consideredIslands, table)
            # Choosing island
            chosenIsland = fn.chooseIsland(consideredIslands, chosenIsland)
            # Handling case when all islands are complete
            if chosenIsland == None:
                fn.wall(table)
                if fn.doChecks(table):
                    print("Nurikabe complete")
                    ns.printTable(table)
                    return table
                else:
                    print("All islands complete but Nurikabe not solved")
                    returningFromBadState = True
            else:
                # Doing a supposition on the chosenIsland
                print("Searching tiles for", chosenIsland.x, chosenIsland.y)
                potentialTiles = fn.returnPotentialTiles(table, chosenIsland, currentState)
                if potentialTiles == None:
                    fn.wall(table)
                    if fn.doChecks(table):
                        print("Nurikabe complete")
                        fn.printTable(table)
                        return table
                    else:
                        print("No potential tiles for island, must go back")
                        returningFromBadState = True
                else:
                    currentState.lastMove = (potentialTiles[0][0], potentialTiles[0][1])
                    currentState.lastIsland = copy.deepcopy(chosenIsland)
                    if len(stateHistory) == 0:
                        stateHistory.append(copy.deepcopy(currentState))
                        print("appended to stateHistory before supposition:")
                    elif len(stateHistory) > 0 and table != stateHistory[len(stateHistory) - 1].table:
                        stateHistory.append(copy.deepcopy(currentState))
                        print("appended to stateHistory before supposition:")
                    stateHistory[len(stateHistory) - 1].lastMove = (potentialTiles[0][0], potentialTiles[0][1])
                    fn.printStates(stateHistory, table)
                    currentState.lastIsland = copy.deepcopy(chosenIsland)
                    lastMove = (potentialTiles[0][0], potentialTiles[0][1])
                    table[potentialTiles[0][0]][potentialTiles[0][1]] = -2
                    print("appended", potentialTiles[0][0], potentialTiles[0][1], "to", chosenIsland.x, chosenIsland.y,
                          "table looks like this:---------------")
                    fn.printTableOld(table)
        # Returning from a bad state
        else:
            print("coming back from a bad state")
            popped = False
            if depth == 12:
                print("debug")
            if fn.returnPotentialTiles(stateHistory[len(stateHistory) - 1].table,
                                       stateHistory[len(stateHistory) - 1].lastIsland,
                                       stateHistory[len(stateHistory) - 1]) == None:
                stateHistory.pop()
                popped = True
            # Take last move of this state and append it as impossible move to this state
            if depth == 115:
                print(len(stateHistory))
            stateHistory[len(stateHistory) - 1].impossibleMoves.append(stateHistory[len(stateHistory) - 1].lastMove)
            currentState = copy.deepcopy(stateHistory[len(stateHistory) - 1])
            table = currentState.table
            returningFromBadState = False
        depth += 1
        print("going in depth", depth)


if __name__ == '__main__':
    grid = [[0, 0, 0, 0, 0],
            [2, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 2, 0],
            [0, 0, 0, 0, 0]]

    """grid = [[0, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 6],
            [0, 0, 6, 0, 0, 0, 0]]"""

    """grid = [[1, 0, 2, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 4, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1]]"""

    currentState = fn.state(grid)
    table = currentState.table

    solve(table, currentState)
