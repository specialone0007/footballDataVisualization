import pandas as pd
import matplotlib.pyplot as plt
from pitch import createPitch, drawActionShot, drawActionPassDribble
from dataInfo import fixYCoordinate, getJerseyDict
import seaborn as sns


def drawAllActions(actionsBeforeAttempt, allActions, theGoalAttempt):
    for indexArray in range(len(actionsBeforeAttempt) - 1):
        i = actionsBeforeAttempt[indexArray]
        i_next = actionsBeforeAttempt[indexArray + 1]
        action = allActions[i]
        action_next = allActions[i_next]

        if action["type"] == "Pass":
            t = ":"
            c = "m"
            drawActionPassDribble(action["location"], action_next["location"], t, c)
        else:
            t = "-."
            c = "b"
            drawActionPassDribble(action["location"], action_next["location"], t, c)

    action = allActions[actionsBeforeAttempt[-1]]

    if action["type"] == "Pass":
        t = ":"
        c = "m"
    else:
        t = "-."
        c = "b"

    drawActionPassDribble(action["location"], theGoalAttempt["location"], t, c)

    drawActionShot(theGoalAttempt["location"], theGoalAttempt["end_location"], theGoalAttempt["xg"],
                   theGoalAttempt["outcome"])


def getJerseyNumber(action, jerseyDict, jerseyIndex):

    if action["player"] not in jerseyDict:
        jerseyIndex[0] -= 1
        jerseyDict[action["player"]] = jerseyIndex[0]
        return jerseyIndex[0]
    else:
        return jerseyDict[action["player"]]


def getAttemptArray(actionsBeforeAttempt, allActions, theGoalAttempt, jerseyDict, jerseyIndex):
    toBeReturned = []
    for i in actionsBeforeAttempt:
        action = allActions[i]
        toBeReturned.append([action["location"][0], action["location"][1], getJerseyNumber(action, jerseyDict,
                                                                                           jerseyIndex)])
    toBeReturned.append([theGoalAttempt["location"][0], theGoalAttempt["location"][1], getJerseyNumber(theGoalAttempt,
                                                                                                       jerseyDict,
                                                                                                       jerseyIndex)])
    return toBeReturned


def getAllShotsString(shotActions, team):
    resultingString = ""
    for index in range(len(shotActions)):
        shot = shotActions[index]
        if shot["team"] == team:
            resultingString += shot["timestamp"] + "-" + shot["outcome"] + "-Xg(" + str(shot["xg"])[0:5] + ")-" + \
                               str(index) + ","
    return resultingString[:-1]


def getAllImportantActionsOfPlayerString(team, player, allActions, shotActions):
    resultingString = ""
    for index in range(len(shotActions)):
        shot = shotActions[index]
        if shot["team"] == team:
            if shot["player"] == player:
                resultingString += "Shot" + "-" + shot["timestamp"] + "-" + shot["outcome"] + "-Xg(" + \
                                   str(shot["xg"])[0:5] + ")-" + str(index) + ","
            else:
                previousActionCounter = 0
                for previousActionId in shot["previous_events"]:
                    currentAction = allActions[previousActionId]
                    if currentAction["player"] != shot["player"]:
                        previousActionCounter += 1
                    if previousActionCounter == 1 and player == currentAction["player"]:
                        resultingString += "Assist" + "-" + shot["timestamp"] + "-" + shot["outcome"] + "-Xg(" + \
                                           str(shot["xg"])[0:5] + ")-" + str(index) + ","
                        break
                    elif player == currentAction["player"]:
                        resultingString += "Build Up" + "-" + shot["timestamp"] + "-" + shot["outcome"] + "-Xg(" + \
                                           str(shot["xg"])[0:5] + ")-" + str(index) + ","
                        break

    return resultingString[:-1]


def getShotAndAllActions(data):
    shotActions = []
    allActions = {}
    for index in range(len(data)):
        d = data[index]
        if "player" in d and "location" in d:

            actionType = d["type"]["name"]
            playerName = d["player"]["name"]
            if "-" in playerName:
                playerName = playerName.replace("-", " ")

            if actionType == "Shot" and "statsbomb_xg" in d["shot"]:
                timestamp = str(d["minute"]) + ":" + str(d["second"]).zfill(2)
                goalAttempt = {"timestamp": timestamp, "team": d["team"]["name"],
                               "player": playerName, "location": fixYCoordinate(d["location"]),
                               "previous_events": [], "xg": d["shot"]["statsbomb_xg"],
                               "end_location": fixYCoordinate(d["shot"]["end_location"][0:2]),
                               "outcome": d["shot"]["outcome"]["name"]}
                shotActions.append(goalAttempt)
                for reverseIndex in range(index - 1, -1, -1):
                    if goalAttempt["team"] != data[reverseIndex]["possession_team"]["name"]:
                        break
                    if data[reverseIndex]["type"]["name"] in ["Dribble", "Pass"] and goalAttempt["team"] == \
                            data[reverseIndex]["team"]["name"]:
                        goalAttempt["previous_events"].append(data[reverseIndex]["id"])
            actionDict = {"team": d["team"]["name"], "type": actionType,
                          "player": playerName, "location": fixYCoordinate(d["location"])}

            allActions[d["id"]] = actionDict

    return shotActions, allActions


def drawImportantAction(data, shotActions, allActions, attemptId, location, jerseyDict, jerseyIndex):

    theGoalAttempt = shotActions[attemptId]

    if not jerseyDict:
        jerseyDict = getJerseyDict(data, theGoalAttempt["team"])

    if not jerseyIndex:
        jerseyIndex = [100]

    actionsBeforeAttempt = list(reversed(theGoalAttempt["previous_events"]))
    actionsArray = getAttemptArray(actionsBeforeAttempt, allActions, theGoalAttempt, jerseyDict, jerseyIndex)
    dataFrame = pd.DataFrame(data=actionsArray, columns=["X", "Y", "Number"])

    createPitch()

    plt.ylim(-5, 85)
    plt.xlim(-5, 125)

    drawAllActions(actionsBeforeAttempt, allActions, theGoalAttempt)

    p = sns.regplot(data=dataFrame, x="X", y="Y", fit_reg=False, marker="o", color="skyblue", scatter_kws={'s': 350})

    for line in range(0, dataFrame.shape[0]):
        p.text(dataFrame.X[line], dataFrame.Y[line], dataFrame.Number[line], horizontalalignment='center', size='large',
               color='black', weight='semibold', verticalalignment="center")

    plt.savefig(location, bbox_inches='tight')
    plt.close("all")
