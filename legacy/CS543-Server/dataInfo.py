def printStartingEleven(data):
    print(50 * "*")
    print(data[0]["team"]["name"], "formation and line up:")
    print(data[0]["tactics"]["formation"])
    print(getStartingEleven(data[0]["tactics"]["lineup"]))
    print(50 * "*")
    print(data[1]["team"]["name"], "formation and line up:")
    print(data[1]["tactics"]["formation"])
    print(getStartingEleven(data[1]["tactics"]["lineup"]))
    print(50 * "*")


def getStartingEleven(data):
    returnArray = []
    for d in data:
        returnArray.append(
            {'name': d["player"]["name"], 'position': d["position"]["name"], 'jersey_number': d["jersey_number"]})
    return returnArray


def getStartingElevenPlayersString(data, team):
    if team == data[0]["team"]["name"]:
        relatedData = data[0]["tactics"]["lineup"]
    else:
        relatedData = data[1]["tactics"]["lineup"]
    resultingString = ""
    for d in relatedData:
        resultingString += str(d["jersey_number"]) + "-" + d["position"]["name"] + "-" + d["player"]["name"].\
            replace("-", " ") + ","

    return resultingString[:-1]


def fixYCoordinate(loc):
    return [loc[0], 80 - loc[1]]


def reverseCoordinate(loc):
    return [120 - loc[0], 80 - loc[1]]


def getJerseyDict(data, teamName):
    startingEleven = {}
    if data[0]["team"]["name"] == teamName:
        for d in data[0]["tactics"]["lineup"]:
            startingEleven[d["player"]["name"]] = d["jersey_number"]
    else:
        for d in data[1]["tactics"]["lineup"]:
            startingEleven[d["player"]["name"]] = d["jersey_number"]
    return startingEleven


def getReverseJerseyDict(data, teamName):
    startingEleven = {}
    if data[0]["team"]["name"] == teamName:
        for d in data[0]["tactics"]["lineup"]:
            startingEleven[d["jersey_number"]] = d["player"]["name"]
    else:
        for d in data[1]["tactics"]["lineup"]:
            startingEleven[d["jersey_number"]] = d["player"]["name"]
    return startingEleven


def getAvailableActionsString(locationDict, playerName):
    myList = list(locationDict[playerName].keys())
    resultingString = ""
    for item in myList:
        resultingString += item + ","
    return resultingString[:-1]
