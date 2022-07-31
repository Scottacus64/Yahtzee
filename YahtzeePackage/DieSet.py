from YahtzeePackage.Dice import *

diceGroup = []



class DieSet(object):
    def __init__(self):
        global diceGroup
        for i in range(5):
            diceGroup.append(Dice(0, "Dice/w0.jpg", 0))
        print("dg = " + str(diceGroup))
        for i in range(5):
            print(diceGroup[i].icon)

