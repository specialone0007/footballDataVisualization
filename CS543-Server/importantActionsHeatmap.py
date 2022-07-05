import pandas as pd
import matplotlib.pyplot as plt
from pitch import createPitch
import seaborn as sns


def drawImportantActionsHeatmap(shotActions, allActions, filename, team):
    createPitch()
    coordinates = []
    for shotAction in shotActions:
        if shotAction["team"] == team:
            coordinates.append([shotAction["location"][0], shotAction["location"][1]])
            counter = 0
            for i in shotAction["previous_events"]:
                action = allActions[i]
                coordinates.append([action["location"][0], action["location"][1]])
                counter += 1
                if counter == 2:
                    break
    dataFrame = pd.DataFrame(data=coordinates, columns=["X", "Y"])

    if dataFrame.shape[0] > 2:
        sns.kdeplot(x=dataFrame["X"], y=dataFrame["Y"], fill=True, n_levels=20, color="r")
    sns.regplot(x=dataFrame["X"], fit_reg=False, y=dataFrame["Y"], color="g", scatter_kws={'s': 15})

    plt.ylim(0, 80)
    plt.xlim(0, 120)
    plt.savefig(filename, bbox_inches='tight')
    plt.close("all")
