import matplotlib.pyplot as plt
from matplotlib.patches import Arc


axKeeper = None


def createPitch(figureName=""):
    global axKeeper

    # Create figure
    fig = plt.figure()
    if figureName != "":
        fig.suptitle(figureName)
    fig.set_size_inches(9, 6)
    ax = fig.add_subplot(1, 1, 1)

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, 80], color="black")
    plt.plot([0, 120], [80, 80], color="black")
    plt.plot([120, 120], [80, 0], color="black")
    plt.plot([120, 0], [0, 0], color="black")
    plt.plot([60, 60], [0, 80], color="black")

    # Left Penalty Area
    plt.plot([18, 18], [18, 62], color="black")
    plt.plot([0, 18], [62, 62], color="black")
    plt.plot([18, 0], [18, 18], color="black")

    # Right Penalty Area
    plt.plot([120, 102], [62, 62], color="black")
    plt.plot([102, 102], [62, 18], color="black")
    plt.plot([102, 120], [18, 18], color="black")

    # Left 6-yard Box
    plt.plot([0, 6], [50, 50], color="black")
    plt.plot([6, 6], [50, 30], color="black")
    plt.plot([6, 0], [30, 30], color="black")

    # Right 6-yard Box
    plt.plot([120, 114], [50, 50], color="black")
    plt.plot([114, 114], [50, 30], color="black")
    plt.plot([114, 120], [30, 30], color="black")

    # Prepare Circles
    centreCircle = plt.Circle((60, 40), 9.15, color="black", fill=False)
    centreSpot = plt.Circle((60, 40), 0.6, color="black")
    leftPenSpot = plt.Circle((12, 40), 0.6, color="black")
    rightPenSpot = plt.Circle((108, 40), 0.6, color="black")

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    leftArc = Arc((12, 40), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color="black")
    rightArc = Arc((108, 40), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color="black")

    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis('off')
    axKeeper = ax


def drawActionShot(startPoint, endPoint, xg, outcome):
    plt.plot([startPoint[0], endPoint[0]], [startPoint[1], endPoint[1]], 'r', label="XG: " + str(xg))

    if outcome == "Saved":
        plt.plot(endPoint[0], endPoint[1], 'go')
    elif outcome == "Blocked":
        plt.plot(endPoint[0], endPoint[1], 'gx')
    elif outcome == "Goal":
        plt.plot(endPoint[0], endPoint[1], 'gD')
    else:
        plt.plot(endPoint[0], endPoint[1], 'gs')

    plt.plot([-10, -10], [-10, -10], 'go', label="Saved")
    plt.plot([-10, -10], [-10, -10], 'gx', label="Blocked")
    plt.plot([-10, -10], [-10, -10], 'gD', label="Goal")
    plt.plot([-10, -10], [-10, -10], 'gs', label="Out")
    plt.plot([-10, -10], [0, 0], ':m', label="Pass")
    plt.plot([-10, -10], [-10, -10], '-.b', label="Dribble")

    plt.legend(loc='best', fontsize='x-small')


def drawActionPassDribble(startPoint, endPoint, t, c):
    plt.plot([startPoint[0], endPoint[0]], [startPoint[1], endPoint[1]], t + c)


