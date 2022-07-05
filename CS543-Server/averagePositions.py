import pandas as pd
import matplotlib.pyplot as plt
from pitch import createPitch
from dataInfo import fixYCoordinate, getJerseyDict
import seaborn as sns


def drawAveragePositions(data, plotName, averageDict, location):
    teamName = plotName.split("-")[0]
    jerseyDict = getJerseyDict(data, teamName)
    positionArray = []
    for key in jerseyDict.keys():
        toBeAdded = [averageDict[key][0] / averageDict[key][2], averageDict[key][1] / averageDict[key][2],
                     jerseyDict[key]]
        positionArray.append(toBeAdded)

    dataFrame = pd.DataFrame(data=positionArray, columns=["X", "Y", "Number"])

    createPitch()

    p = sns.regplot(data=dataFrame, x="X", y="Y", fit_reg=False, marker="o", color="skyblue", scatter_kws={'s': 400})

    for line in range(0, dataFrame.shape[0]):
        p.text(dataFrame.X[line], dataFrame.Y[line], dataFrame.Number[line], horizontalalignment='center',
               size='medium',
               color='black', weight='semibold', verticalalignment="center")

    plt.ylim(0, 80)
    plt.xlim(0, 120)

    plt.savefig(location, bbox_inches='tight')
    plt.close("all")


def getAveragePosDicts(data):
    averageInPositions = {}
    averageOutPositions = {}

    for d in data:
        if "player" in d and "location" in d:
            location = fixYCoordinate(d["location"])
            playerName = d["player"]["name"]
            team = d["team"]["name"]
            possessionTeam = d["possession_team"]["name"]

            if playerName not in averageInPositions:
                averageInPositions[playerName] = [0, 0, 0]
            if playerName not in averageOutPositions:
                averageOutPositions[playerName] = [0, 0, 0]

            if possessionTeam == team:
                averageInPositions[playerName][0] += location[0]
                averageInPositions[playerName][1] += location[1]
                averageInPositions[playerName][2] += 1
            else:
                averageOutPositions[playerName][0] += location[0]
                averageOutPositions[playerName][1] += location[1]
                averageOutPositions[playerName][2] += 1
    return averageInPositions, averageOutPositions
