import pandas as pd
import matplotlib.pyplot as plt
from pitch import createPitch
from dataInfo import fixYCoordinate
import seaborn as sns


def getPlayerActionLocations(inputData):
    playerLocations = {}

    for d in inputData:
        if "player" in d and "location" in d:
            location = fixYCoordinate(d["location"])
            playerName = d["player"]["name"]
            if "-" in playerName:
                playerName = playerName.replace("-", " ")
            actionType = d["type"]["name"]
            if playerName not in playerLocations:
                playerLocations[playerName] = {}
            if actionType not in playerLocations[playerName]:
                playerLocations[playerName][actionType] = []

            playerLocations[playerName][actionType].append(location)

    return playerLocations


def drawActionHeatMap(playerLocations, chosenPlayer, chosenAction, location):
    createPitch()
    playerLocation = playerLocations[chosenPlayer][chosenAction]
    dataFrame = pd.DataFrame(data=playerLocation, columns=["X", "Y"])

    if dataFrame.shape[0] > 2:
        sns.kdeplot(x=dataFrame["X"], y=dataFrame["Y"], fill=True, n_levels=20, color="r")
    sns.regplot(x=dataFrame["X"], fit_reg=False, y=dataFrame["Y"], color="g", scatter_kws={'s': 15})

    plt.ylim(0, 80)
    plt.xlim(0, 120)
    plt.savefig(location, bbox_inches='tight')
    plt.close("all")
