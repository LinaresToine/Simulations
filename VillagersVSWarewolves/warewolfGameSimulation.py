import numpy as np
import random
import matplotlib.pyplot as plt
import sys
def createPlayers(n_villagers, n_warewolves):
    """
    Creates array with players.
    n_villagers represented by False values
    n_warewolves represented by True values
    """
    players = np.array([True]*n_warewolves + [False]*n_villagers)
    return players

def shufflePlayers(players):
    """
    Shuffles the players into a new order
    """
    random.shuffle(players)

def chooseIndex(playerIndices = None, villagerIndices = None, warewolfAttack = False):
    """
    Randomly selects an index that represents a player spot in array players
    Returns index
    """
    if warewolfAttack:
        chosenIndex = np.random.choice(villagerIndices)
    else:
        chosenIndex = np.random.choice(playerIndices)
    return chosenIndex


def updateIndices(chosenIndex, villagerIndices = None, playerIndices = None):
    """
    """
    villagerIndices = villagerIndices[villagerIndices != chosenIndex]
    playerIndices = playerIndices[playerIndices != chosenIndex]
    return villagerIndices, playerIndices

def game(n_games, n_villagers, n_warewolves):
    """
    This function runs the game.
    At night, the warewolves decide who to kill.
    During the day, the villagers argue on who could be a warewolf and kill him
    The villagers win if all warewolves are killed
    The warewolves win if only two villagers are remaining
    """
    players = createPlayers(n_villagers, n_warewolves)

    villagerPoints = 0
    warewolfPoints = 0

    warewolf = True
    villager = False
    gamesPlayed = 0

    while gamesPlayed < n_games:

        shufflePlayers(players=players)

        villagerIndices = np.where(players == villager)[0]
        warewolfIndices = np.where(players == warewolf)[0]
        playerIndices = np.append(villagerIndices, warewolfIndices)

        chosenIndices = np.array([])
        winner = False
        gamesPlayed += 1

        while winner == False:
            """
            First, warewolves kill a villager
            """
            chosenVillagerIndex = chooseIndex(playerIndices=playerIndices, villagerIndices=villagerIndices, warewolfAttack=True)
            villagerIndices, playerIndices = updateIndices(chosenIndex=chosenVillagerIndex, villagerIndices=villagerIndices, playerIndices=playerIndices)

            """
            Now villagers choose to kill one player randomly, in hopes it is a warewolf      
            """
            chosenPlayerIndex = chooseIndex(playerIndices=playerIndices, villagerIndices=villagerIndices, warewolfAttack=False)
            villagerIndices, playerIndices = updateIndices(chosenIndex=chosenPlayerIndex, villagerIndices=villagerIndices, playerIndices=playerIndices)
            
            """
            Now we keep track of the chosen indices to evaluate that all none are chosen twice
            """
            chosenIndices = np.append(chosenIndices, chosenVillagerIndex)
            chosenIndices = np.append(chosenIndices, chosenPlayerIndex)

            """
            Now we evaluate for winners
            """
            if len(playerIndices) == len(villagerIndices) or not np.isin(warewolfIndices, playerIndices).any():
                villagerPoints += 1
                winner = True

            elif len(villagerIndices) <= n_warewolves and np.isin(warewolfIndices, playerIndices).any():
                warewolfPoints += 1
                winner = True

            else:
                continue

    return villagerPoints, warewolfPoints

def ratioStudy(n_games, n_warewolves, n_villagers, n_tests): 
    warewolfVictories = np.zeros(n_tests)
    villagerVictories = np.zeros(n_tests)

    for i in range(n_tests):
        villagerPoints, warewolfPoints = game(n_games, n_villagers, n_warewolves)
        warewolfVictories[i] = warewolfPoints
        villagerVictories[i] = villagerPoints

    return warewolfVictories, villagerVictories


def createPlot(n_games, min_villagers, max_villagers, n_warewolves):
    space = int(((max_villagers - min_villagers)/2) + 1)
    x_villagers = np.int64(np.linspace(min_villagers, max_villagers, space))
    warewolfVictory = np.zeros(space)
    villagerVictory = np.zeros(space)
    for i in range(len(x_villagers)):
        villagerVictory[i], warewolfVictory[i] = game(n_games = n_games, n_villagers = x_villagers[i], n_warewolves = n_warewolves)
    plt.figure(figsize = (10,7))
    plt.grid()
    plt.scatter(x_villagers, warewolfVictory, label = 'Warewolves Victory')
    plt.scatter(x_villagers, villagerVictory, label = 'Villagers Victory')
    plt.xlabel('Number of Villagers')
    plt.ylabel('Number of Wins')
    plt.title('{} Warewolves'.format(n_warewolves))
    plt.legend()
    plt.savefig('{}_Warewolves'.format(n_warewolves))

def main():
    """
    Main function. Runs the program and creates plots
    """
    n_games = int(sys.argv[1])
    min_villagers = int(sys.argv[2])
    max_villagers = int(sys.argv[3])
    n_warewolves = int(sys.argv[4])

    createPlot(n_games, min_villagers, max_villagers, n_warewolves)

if __name__ == "__main__":
    main()