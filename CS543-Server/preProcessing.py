import json
import os
from dataInfo import getStartingElevenPlayersString, getAvailableActionsString, getJerseyDict
from action_heatmaps import getPlayerActionLocations, drawActionHeatMap
from averagePositions import getAveragePosDicts, drawAveragePositions
from importantActionSequences import getShotAndAllActions, drawImportantAction
from xgScatterPlot import getXgScatterPlot
from xgNodes import getXgNodes
from importantActionsHeatmap import drawImportantActionsHeatmap

with open('exampleMatch.json') as f:
    data = json.load(f)

pngLocation = 'C:/Users/furka/OneDrive/Documents/visual studio 2015/Projects/CS543-GUI/CS543-GUI/bin/Debug/Images/'


def uploadAllHeatMaps():
    playerActionLocations = getPlayerActionLocations(data)

    for team in ["Manchester City WFC", "Chelsea LFC"]:
        startingEleven = getStartingElevenPlayersString(data, team).split(",")
        for player in startingEleven:
            playerName = player.split("-")[2]
            availableActions = getAvailableActionsString(playerActionLocations, playerName).split(",")
            for action in availableActions:
                actionString = action
                if action == "Ball Receipt*":
                    actionString = "Ball Receipt"
                fileLocation = pngLocation + playerName + "-" + actionString + " Heat Map" + ".png"
                if not os.path.isfile(fileLocation):
                    drawActionHeatMap(playerActionLocations, playerName, action, fileLocation)


def uploadAllAveragePositions():
    averageInPositionsDict, averageOutPositionsDict = getAveragePosDicts(data)
    for team in ["Manchester City WFC", "Chelsea LFC"]:
        for typeAverage in ["In Position", "Out Position"]:
            teamAndFilter = team + "-" + typeAverage
            fileLocation = pngLocation + teamAndFilter + ".png"
            if not os.path.isfile(fileLocation):
                if typeAverage == "In Position":
                    drawAveragePositions(data, teamAndFilter, averageInPositionsDict, fileLocation)
                else:
                    drawAveragePositions(data, teamAndFilter, averageOutPositionsDict, fileLocation)


def uploadAllImportantActions():
    shotActionsArray, allActionsDict = getShotAndAllActions(data)
    team1 = data[0]["team"]["name"]
    team2 = data[1]["team"]["name"]

    fileLocation1 = pngLocation + "Important Actions Heatmap - " + team1 + ".png"
    fileLocation2 = pngLocation + "Important Actions Heatmap - " + team2 + ".png"
    if not os.path.isfile(fileLocation1):
        drawImportantActionsHeatmap(shotActionsArray, allActionsDict, fileLocation1, team1)
    if not os.path.isfile(fileLocation2):
        drawImportantActionsHeatmap(shotActionsArray, allActionsDict, fileLocation2, team2)

    jerseyDict1 = getJerseyDict(data, team1)
    jerseyDict2 = getJerseyDict(data, team2)
    jerseyIndex1 = [100]
    jerseyIndex2 = [100]
    for index in range(len(shotActionsArray)):
        attemptIndex = str(index)
        team = shotActionsArray[index]["team"]
        fileLocation = pngLocation + "Important Action " + attemptIndex + ".png"
        if not os.path.isfile(fileLocation):
            if team == team1:
                drawImportantAction(data, shotActionsArray, allActionsDict, index, fileLocation, jerseyDict1,
                                    jerseyIndex1)
            else:
                drawImportantAction(data, shotActionsArray, allActionsDict, index, fileLocation, jerseyDict2,
                                    jerseyIndex2)


def uploadXgScatter():
    fileLocation = pngLocation + "xgScatterPlot" + ".png"
    if not os.path.isfile(fileLocation):
        getXgScatterPlot(data, fileLocation)


def uploadXgNodes():
    fileLocation = pngLocation + "XgNodes" + ".png"
    if not os.path.isfile(fileLocation):
        getXgNodes(data, fileLocation)

