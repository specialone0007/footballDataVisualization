import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def getXgScatterPlot(data, location):

    xgArray = []
    xgDict = {}
    score = {}

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

                xgDict[team] += float(d["shot"]["statsbomb_xg"])

                timestampData = int(d["timestamp"][3:5])
                if timestampData > 45:
                    timestampData = 45
                timestamp = timestampData + (int(d["period"]) - 1) * 45

                xgArray.append([timestamp, xgDict[team], team])

    dataFrame = pd.DataFrame(data=xgArray, columns=["Time", "XG", "Team"])

    fig = plt.figure()
    fig.set_size_inches(7.17, 4.82)

    figureName = ""
    for team in xgDict:
        figureName += team + " : " + str(score[team]) + "(" + str(xgDict[team]) + ")"
        figureName += 2 * " "
    fig.suptitle(figureName)

    for key, grp in dataFrame.groupby('Team'):
        plt.plot(grp.Time, grp.XG, 'o-', label=key)
    plt.legend(loc='best')
    plt.xticks(np.arange(0, 100, 10.0))

    plt.savefig(location, bbox_inches='tight')
    plt.close("all")
