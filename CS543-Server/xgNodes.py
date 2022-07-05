import pandas as pd
import matplotlib.pyplot as plt
from dataInfo import fixYCoordinate, reverseCoordinate
from pitch import createPitch
import seaborn as sns


def getXgNodes(data, fileName):
    xgArray = []
    xgDict = {}
    score = {}
    teamCode = []

    for index in range(len(data)):
        d = data[index]
        if "player" in d and "location" in d:

            actionType = d["type"]["name"]

            if actionType == "Shot" and "statsbomb_xg" in d["shot"]:
                team = d["team"]["name"]

                if team not in score:
                    score[team] = 0

                if d["shot"]["outcome"]["name"] == "Goal":
                    score[d["team"]["name"]] += 1

                if team not in xgDict:
                    xgDict[team] = 0

                if team not in teamCode:
                    teamCode.append(team)

                xgDict[team] += float(d["shot"]["statsbomb_xg"])

                timestampData = int(d["timestamp"][3:5])
                if timestampData > 45:
                    timestampData = 45
                timestamp = timestampData + (int(d["period"]) - 1) * 45

                location = fixYCoordinate(d["location"])

                if teamCode.index(team) == 1:
                    location = reverseCoordinate(location)

                xg = xgDict[team]
                sizePoint = float(d["shot"]["statsbomb_xg"]) * 1000

                xgArray.append([team, timestamp, location[0], location[1], sizePoint])

    dataFrame = pd.DataFrame(data=xgArray, columns=["Team", "Time", "X", "Y", "Size"])

    figureName = ""
    for team in xgDict:
        figureName += team + " : " + str(score[team]) + "(" + str(xgDict[team]) + ")"
        figureName += 2 * " "

    createPitch(figureName=figureName)
    p = sns.regplot(data=dataFrame, x="X", y="Y", fit_reg=False, marker="o", color="skyblue",
                    scatter_kws={'s': dataFrame['Size']})

    for line in range(0, dataFrame.shape[0]):
        p.text(dataFrame.X[line], dataFrame.Y[line], "{:.2f}".format(dataFrame.Size[line] / 1000),
               horizontalalignment='center', size='xx-small',
               color='black', weight='semibold', verticalalignment="center")

    plt.ylim(0, 80)
    plt.xlim(0, 120)

    plt.savefig(fileName, bbox_inches='tight')
    plt.close("all")


