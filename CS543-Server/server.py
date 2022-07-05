from flask import Flask
from flask_restful import Resource, Api
import json
from flask import request
from averagePositions import getAveragePosDicts, drawAveragePositions
import os
from dataInfo import getStartingElevenPlayersString, getAvailableActionsString
from action_heatmaps import getPlayerActionLocations, drawActionHeatMap
from preProcessing import uploadAllAveragePositions, uploadAllHeatMaps, uploadAllImportantActions, uploadXgScatter, \
    uploadXgNodes
from importantActionSequences import getShotAndAllActions, getAllShotsString, drawImportantAction, \
    getAllImportantActionsOfPlayerString
from xgScatterPlot import getXgScatterPlot
from xgNodes import getXgNodes
from importantActionsHeatmap import drawImportantActionsHeatmap

uploadAllAveragePositions()
uploadAllHeatMaps()
uploadAllImportantActions()
uploadXgScatter()
uploadXgNodes()

with open('exampleMatch.json') as f:
    data = json.load(f)

pngLocation = 'C:/Users/furka/OneDrive/Documents/visual studio 2015/Projects/CS543-GUI/CS543-GUI/bin/Debug/Images/'

averageInPositionsDict, averageOutPositionsDict = getAveragePosDicts(data)
playerActionLocations = getPlayerActionLocations(data)
shotActionsArray, allActionsDict = getShotAndAllActions(data)

app = Flask(__name__)
api = Api(app)


class TeamNames(Resource):
    @staticmethod
    def get():
        return data[0]["team"]["name"] + "," + data[1]["team"]["name"]


class AveragePositions(Resource):
    @staticmethod
    def get():
        teamAndFilter = request.args.get("var").replace("\n", "")
        fileLocation = pngLocation + teamAndFilter + ".png"

        if not os.path.isfile(fileLocation):
            visualFilter = teamAndFilter.split("-")[1]
            if visualFilter == "In Position":
                drawAveragePositions(data, teamAndFilter, averageInPositionsDict, fileLocation)
            else:
                drawAveragePositions(data, teamAndFilter, averageOutPositionsDict,  fileLocation)
        return teamAndFilter + ".png"


class PlayerNames(Resource):
    @staticmethod
    def get():
        teamName = request.args.get("var").replace("\n", "")
        startingEleven = getStartingElevenPlayersString(data, teamName)
        return startingEleven


class AvailableActions(Resource):
    @staticmethod
    def get():
        playerName = request.args.get("var").replace("\n", "").split("-")[2]
        availableActions = getAvailableActionsString(playerActionLocations, playerName)
        return availableActions


class ActionHeatMap(Resource):
    @staticmethod
    def get():
        requestString = request.args.get("var").replace("\n", "").split("-")
        player = requestString[2]
        action = requestString[3]
        actionString = action
        if action == "Ball Receipt*":
            actionString = "Ball Receipt"
        fileLocation = pngLocation + player + "-" + actionString + " Heat Map" + ".png"
        if not os.path.isfile(fileLocation):
            print(fileLocation)
            drawActionHeatMap(playerActionLocations, player, action, fileLocation)
        return player + "-" + actionString + " Heat Map" + ".png"


class PossibleImportantActions(Resource):
    @staticmethod
    def get():
        requestString = request.args.get("var").replace("\n", "").split("-")
        controlString = requestString[0]

        if controlString == "Continue Without Selected Player":
            team = requestString[1]
            resultString = getAllShotsString(shotActionsArray, team)
        else:
            team = requestString[3]
            player = requestString[2]
            resultString = getAllImportantActionsOfPlayerString(team, player, allActionsDict, shotActionsArray)
            if resultString == "":
                resultString = "!"
        return resultString


class ImportantAction(Resource):
    @staticmethod
    def get():
        attemptIndex = request.args.get("var").replace("\n", "")
        fileLocation = pngLocation + "Important Action " + attemptIndex + ".png"
        if not os.path.isfile(fileLocation):
            drawImportantAction(data, shotActionsArray, allActionsDict, int(attemptIndex), fileLocation, {}, [])
        return "Important Action " + attemptIndex + ".png"


class XgScatterPlot(Resource):
    @staticmethod
    def get():
        fileLocation = pngLocation + "xgScatterPlot" + ".png"
        if not os.path.isfile(fileLocation):
            getXgNodes(data, fileLocation)
        return "xgScatterPlot" + ".png"


class XgNodes(Resource):
    @staticmethod
    def get():
        fileLocation = pngLocation + "XgNodes" + ".png"
        if not os.path.isfile(fileLocation):
            getXgScatterPlot(data, fileLocation)
        return "XgNodes" + ".png"


class ImportantActionsHeatmap(Resource):
    @staticmethod
    def get():
        fileLocation = pngLocation + "XgNodes" + ".png"
        if not os.path.isfile(fileLocation):
            getXgScatterPlot(data, fileLocation)
        return "XgNodes" + ".png"


class ImportantActionHeatMap(Resource):
    @staticmethod
    def get():
        team = request.args.get("var").replace("\n", "")
        fileLocation = pngLocation + "Important Actions Heatmap - " + team + ".png"
        if not os.path.isfile(fileLocation):
            drawImportantActionsHeatmap(shotActionsArray, allActionsDict, fileLocation, team)
        return "Important Actions Heatmap - " + team + ".png"


api.add_resource(TeamNames, '/team_names')
api.add_resource(AveragePositions, '/average_positions')
api.add_resource(PlayerNames, '/player_names')
api.add_resource(AvailableActions, '/available_actions')
api.add_resource(ActionHeatMap, '/action_heatmap')
api.add_resource(PossibleImportantActions, '/possible_important_actions')
api.add_resource(ImportantAction, '/important_action')
api.add_resource(XgScatterPlot, '/xg_scatter')
api.add_resource(XgNodes, '/xg_nodes')
api.add_resource(ImportantActionHeatMap, '/important_actions_heatmap')

if __name__ == '__main__':
    app.run(debug=True)
