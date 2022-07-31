from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import *
from YahtzeePackage.DieSet import *
import time
import random

# global variables
buttonList = []  # list of die button objects with dieGroup icon value applied
buttonDie = {}  # dictionary with push button objects and corresponding die objects
sortedDiceList = [] # list with dice sorted from low to high
yTableList = [] # master list of all yahtzee table cells that have been filled
tableClicked = False # toggle flag for knowing if rolls should be stopped because of table entry
diceRolled = False # toggle flag to know if any rolling has taken place
dieRolls = 0 # number of times the dice have been rolled
gameOver = False # variable to know if the game is over
yahtzeeBonus = 0 # keeps track of number of yahtzees, if greater than 3 then yahtzee bonus rules apply
# if all three yahtzee cells are filled with 50's then the yahtzee must go into a upper section cell of the
# same pip value.  If those are filled then the yahtzee can be used as a "joker" to fill in any full house,
# small or large straight for full point values (25, 30 or 40).  The yahtzee bonus of 100 is filled into
# the column of the score and multiplied by the column's multiple factor
yahtzeeJoker = False # flag to know if a "joker" situation is true
yahtzeeBonusList = [0, 0, 0] # list of the yahtzee bonus values
autoFill = False # used to prevent player cell entry if yahtzee bonus is in plan and upper section can be filled

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global diceGroup
        global buttonList
        global buttonDie
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 830)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Dice/y6.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off) #icon for menu bar
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # button to roll dice
        self.rollButton = QtWidgets.QPushButton(self.centralwidget)
        self.rollButton.setGeometry(QtCore.QRect(170, 280, 110, 50))
        self.rollButton.setObjectName("rollButton")
        self.rollButton.clicked.connect(self.rollDice)
        self.dieButtonGroup = QtWidgets.QButtonGroup()
        # makes the five dice that are push buttons
        for i in range(5):
            die = ("die" + str(i))
            self.die = QtWidgets.QPushButton(self.centralwidget)
            self.die.setGeometry(QtCore.QRect(50, 50 + (i * 100), 81, 81))
            self.die.setIcon(QIcon(diceGroup[i].icon))
            self.die.setIconSize(QSize(81, 81))
            buttonDie[self.die] = diceGroup[i] # dictionary of pairs of die buttons and die objectss
            buttonList.append(self.die) # list of die buttons
            self.dieButtonGroup.addButton(self.die, i) # group of die buttons
        self.dieButtonGroup.buttonClicked.connect(self.dieClicked) # if clicked go to dieClicked
        #set up for yahtzee table of entries
        self.yahtzeeTable = QtWidgets.QTableWidget(self.centralwidget)
        self.yahtzeeTable.setGeometry(QtCore.QRect(340, 10, 541, 775))
        self.yahtzeeTable.setAutoFillBackground(False)
        self.yahtzeeTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.yahtzeeTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.yahtzeeTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.yahtzeeTable.setWordWrap(False)
        self.yahtzeeTable.setCornerButtonEnabled(False)
        self.yahtzeeTable.setRowCount(20)
        self.yahtzeeTable.setColumnCount(3)
        self.yahtzeeTable.setObjectName("yahtzeeTable")
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        # sets up the 20 rows of the table
        for i in range(20):
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            if i < 7:  # first rows get icons in the header
                iconName = ("icon" + str(i))
                iconFile = ("Dice/y" + str(i) + ".jpg")
                iconName = QtGui.QIcon()
                iconName.addPixmap(QtGui.QPixmap(iconFile), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(iconName)
            item = QtWidgets.QTableWidgetItem()
            self.yahtzeeTable.setVerticalHeaderItem(i, item)
        # sets up the three columns
        for i in range(3):
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            item = QtWidgets.QTableWidgetItem()
            self.yahtzeeTable.setHorizontalHeaderItem(i, item)
        # format the headers
        self.yahtzeeTable.horizontalHeader().setVisible(True)
        self.yahtzeeTable.horizontalHeader().setMinimumSectionSize(125)
        self.yahtzeeTable.horizontalHeader().setStretchLastSection(True)
        self.yahtzeeTable.verticalHeader().setVisible(True)
        self.yahtzeeTable.verticalHeader().setStretchLastSection(True)
        # makes a label for the grand total
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 600, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        # makes a push button that is normally hidden to start a new game
        self.playAgain = QtWidgets.QPushButton(self.centralwidget)
        self.playAgain.setGeometry(QtCore.QRect(70, 700, 162, 49))
        self.playAgain.setIcon(QIcon("Dice/playAgain.jpg"))
        self.playAgain.setIconSize(QSize(162, 49))
        self.playAgain.hide()
        self.playAgain.clicked.connect(self.newGame)
        # formats lines at the top of the first row
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(480, 30, 401, 20))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        """self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)"""
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.yahtzeeTable.clicked.connect(self.yahtzeeTableClick)

    def retranslateUi(self, MainWindow): # this sets up the material displayed in the widgets
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yahtzee"))
        self.rollButton.setText(_translate("MainWindow", "Roll"))
        yahtzeeList = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Total", "Bouns", "UPPER TOTAL           ",
                       "", "Three of a Kind", "Four of a Kind", "Full House", "Small Straight", "Large Straight",
                       "Yahtzee", "Chance", "Yahtzee Bonus", "LOWER TOTAL", "GRAND TOTAL"]
        # makes 20 rows and uses the list to populate them
        for i in range(20):
            itemRow = self.yahtzeeTable.verticalHeaderItem(i)
            itemRow.setText(_translate("MainWindow", yahtzeeList[i]))
        yahtzeeTopList = ["x1", "x2", "x3"]
        # makes three columns and uses the list to populate them
        for i in range(3):
            itemCol = self.yahtzeeTable.horizontalHeaderItem(i)
            itemCol.setText(_translate("MainWindow", yahtzeeTopList[i]))
        self.label.setText(_translate("MainWindow", "Grand Total = 0"))

    def yahtzeeTableClick(self, item):
        global diceRolled
        global tableClicked
        global diceClicked
        global sortedDiceList
        global yahtzeeBonus
        global yahtzeeJoker
        global autoFill

        diceRolled = False # set to false to show that the dice rolling is over
        _translate = QtCore.QCoreApplication.translate
        self.rollButton.setText(_translate("MainWindow", "Roll")) # put roll back on the button
        row = item.row()
        col = item.column()
        pipValue = 0
        inTableList = False # flag to know if the player has clicked on a cell that is already filled

        if autoFill == False: # checks to see if a yahtzee bonus autofill has already occurred
            if yahtzeeBonus > 2 and diceGroup[0].pip == diceGroup[1].pip == diceGroup[2].pip == diceGroup[3].pip == diceGroup[4].pip:
                # Note this is a yahtzee bonus situation and special rules apply to the cell to be filled
                columnList = []
                for entry in yTableList: # look at each table cell entry to see if the upper cell corresponding to pip is filled
                    pipValue = (diceGroup[0].pip -1)
                    if entry[0] == pipValue:
                        columnList.append(entry[1]) # make a list of columns already filled in
                columnList.sort() # sort the column numbers from 0 to 2
                if len(columnList) < 3: # if the column's upper section pip rows are not already all filled in
                    for i in range(2,-1,-1): # step backwards through the list
                        if i not in columnList: # pick the largest value from the list
                            entryColumn = i
                            break  # get out of here
                    bonus = yahtzeeBonusList[entryColumn] # see if any yahtzee bonus exists already
                    bonus += 100 # increase that value by 100
                    yahtzeeBonusList[entryColumn] = bonus # update the list
                    pointValue = ((pipValue + 1) * 5) # total points to be filled in
                    yTableList.append((pipValue, entryColumn, pointValue))  # append the tuple with row, col and total
                    item = QTableWidgetItem(str(pointValue)) # make the point value 5 times the pip value
                    self.yahtzeeTable.setItem((pipValue), entryColumn, item) #fill in the cell
                    item = QTableWidgetItem(str(bonus))  # set the yahtzee bonus value
                    self.yahtzeeTable.setItem((17), entryColumn, item)  # fill in the cell
                    autoFill = True
                else:
                    yahtzeeJoker = True
                    print(yahtzeeJoker)
            for entry in yTableList: # look through the tuples in yTableList and see if the cell has been filled already
                print(yahtzeeJoker)
                if entry[0] == row and entry[1] == col:
                    inTableList = True
            if inTableList == False and autoFill == False: # next line makes sure that the player didn't click on a "total" cell
                if tableClicked == True and row >= 0 and row <= 5 or tableClicked == True and row >= 10 and row <= 16:
                    lastCell = yTableList[-1] # get the last tuple in the the list
                    lastRow = lastCell[0]
                    lastColumn = lastCell[1]
                    if yahtzeeJoker == True: # undo the yahtzee bonus from the last iteration
                        previousBonus = yahtzeeBonusList[lastColumn]
                        print(yahtzeeBonusList)
                        previousBonus -= 100
                        yahtzeeBonusList[lastColumn] = previousBonus
                        print(yahtzeeBonusList)
                        item = QTableWidgetItem(str(previousBonus))  # set the yahtzee bonus value
                        self.yahtzeeTable.setItem((17), lastColumn, item)  # fill in the cell
                    yTableList.pop() # pop removes the last element in the list
                    item = QTableWidgetItem(str("")) # put a blank fill in the formerly populated cell
                    self.yahtzeeTable.setItem(lastRow, lastColumn, item)
                dieTotal = 0
                if yahtzeeJoker == True: # if a yahtzee joker situation exists
                    print("ybl = " + str(yahtzeeBonusList))
                    bonus = yahtzeeBonusList[col]  # see if any yahtzee bonus exists already
                    print(bonus)
                    bonus += 100  # increase that value by 100
                    print(bonus)
                    yahtzeeBonusList[col] = bonus  # update the list
                    item = QTableWidgetItem(str(bonus))  # set the yahtzee bonus value
                    self.yahtzeeTable.setItem((17), col, item)  # fill in the cell

                #check to see if the selection is in the upper cells
                if row >= 0 and row <= 5:
                    for i in range(5):
                        if diceGroup[i].pip == (row + 1): # if the die pip matches the row selected
                            dieTotal += (row + 1) # add that die to the total
                    item = QTableWidgetItem(str(dieTotal))
                    self.yahtzeeTable.setItem(row, col, item)
                    yTableList.append((row, col, dieTotal)) #append the touple with row, col and total
                    tableClicked = True # set the tableClicked flag to true
                    self.totalUp() # call total up to sum the columns
                    if len(yTableList) == 39: # if all the cells are filled, end the game
                        self.endGame()
                # if the player clicked on the lower section of the table
                if row >= 10 and row <= 16:
                    sortedDiceGroup = []
                    sortedDiceList = []
                    sortedDiceGroup = diceGroup.copy() # important to copy not set equal, copy makes the original not change
                    sortedDiceGroup.sort(key=lambda x: x.pip) #sort the group based upon pip value
                    for i in range(5):
                        sortedDiceList.append(sortedDiceGroup[i].pip) #append the die objects
                    #If three of a kind is selected
                    if row == 10:
                        total = self.threeOfaKind() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            self.endGame()
                    # if four of a kind is selected
                    if row == 11:
                        total = self.fourOfaKind() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            self.endGame()
                    # if full house is selected
                    if row == 12:
                        total = self.fullHouse() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            self.endGame()
                    # if small straight is selected
                    if row == 13:
                        total = self.smallStraight() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            self.endGame()
                    # if large straight is selected
                    if row == 14:
                        total = self.largeStraight() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            self.endGame()
                    # if yahtzee is selected
                    if row == 15:
                        total = self.yahtzee() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            self.endGame()
                    # if chance is selected
                    if row == 16:
                        total = self.chance() # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzeeTable.setItem(row, col, item)
                        yTableList.append((row, col, total))
                        tableClicked = True
                        self.totalUp()
                        if len(yTableList) == 39:
                            print("End of Game")
                            self.endGame()

    # these are the helper methods for summing up the lower section totals
    def threeOfaKind(self):
        for i in range(3): #look at the first three dice that have been sorted
            if sortedDiceList[i] == sortedDiceList[i + 2]: # if the first is equal to the third then three of a kind
                total = 0
                for j in range(5):
                    total += sortedDiceList[j]
                return total # NOTE return ends the method so no need to try to break out
        return 0 # if no three of a kind return a zero

    def fourOfaKind(self):
        for i in range(2):
            if sortedDiceList[i] == sortedDiceList[i + 3]: #if the first is equal to the fourth then four of a kind
                total = 0
                for j in range(5):
                    total += sortedDiceList[j]
                return total
        return 0

    def fullHouse(self): #checks if the first three and last two are the same and first two and last three sorted dice
        if yahtzeeJoker == True:
            return 25
        if sortedDiceList[0] == sortedDiceList[2] and sortedDiceList[3] == sortedDiceList[4] or sortedDiceList[0] == \
                sortedDiceList[1] and sortedDiceList[2] == sortedDiceList[4]:
            return 25
        else:
            return 0

    def smallStraight(self):
        if yahtzeeJoker == True:
            return 30
        newList = []
        newList = [*set(sortedDiceList)] # sort the dice and remove duplicate pip values
        if len(newList) < 4: # if there are fewer than four dice in the list there can be no small straight
            return 0
        if len(newList) < 5: # if there are only four dice then go through the loop once (prevents read past end of list)
            stepTo = 1
        else:
            stepTo = 2 # otherwise go through twice to get all five dice checked out
        for i in range(stepTo): # check and see if each die is one more than the preceeding die
            if newList[i + 3] == (newList[i + 2] + 1) and newList[i + 2] == (newList[i + 1] + 1) and newList[i + 1] == (
                    newList[i] + 1):
                return 30
        return 0

    def largeStraight(self): #same logic as above but all five must be in sequence
        if yahtzeeJoker == True:
            return 40
        if sortedDiceList[4] == (sortedDiceList[3] + 1) and sortedDiceList[3] == (sortedDiceList[2] + 1) and \
                sortedDiceList[2] == (sortedDiceList[1] + 1) and sortedDiceList[1] == (sortedDiceList[0] + 1):
            return 40
        else:
            return 0

    def yahtzee(self): # just checks if all die pip values are the same
        global yahtzeeBonus
        if sortedDiceList[0] == sortedDiceList[1] == sortedDiceList[2] == sortedDiceList[3] == sortedDiceList[4]:
            yahtzeeBonus += 1 # if this gets to three then the yahtzee bonus rules apply
            return 50
        else:
            return 0

    def chance(self): # just adds all five die pip values together
        total = sortedDiceList[0] + sortedDiceList[1] + sortedDiceList[2] + sortedDiceList[3] + sortedDiceList[4]
        return total

    def dieClicked(self, button): # this is called if a die is clicked
        clickedDie = buttonDie[button]  # sets clickedDie = to the die object dictionary pair to the button pressed
        if clickedDie.isClicked == 1: # toggles the isClicked value
            clickedDie.isClicked = 0
            clickedDie.icon = ("Dice/w" + str(clickedDie.pip) + ".jpg") # makes the die white
        else:
            clickedDie.isClicked = 1
            clickedDie.icon = ("Dice/y" + str(clickedDie.pip) + ".jpg") # makes the die yellow
        for i in range(5):
            if buttonList[i] == button:
                buttonList[i].setIcon(QIcon(clickedDie.icon))
        QApplication.processEvents() # MUST HAVE THIS to update the dice icons

    def totalUp(self): # helper function to total up the columns
        topTotal0 = 0
        topTotal1 = 0
        topTotal2 = 0
        bonus0 = 0
        bonus1 = 0
        bonus2 = 0
        topGrandTotal0 = 0
        topGrandTotal1 = 0
        topGrandTotal2 = 0
        bottomTotal0 = 0
        bottomTotal1 = 0
        bottomTotal2 = 0
        grandTotal0 = 0
        grandTotal1 = 0
        grandTotal2 = 0
        yGrandTotal = 0

        for yTuple in yTableList: # look through the tuple list
            for i in range(3): # look at each column
                if yTuple[1] == i: # if the tuple's column matches the column being summed
                    if yTuple[0] <= 5: # if it is in the top section
                        if yTuple[1] == 0: # if in the first column
                            topTotal0 += yTuple[2] # incremet the top first column total by the value stored
                            if topTotal0 >= 63: # if the top total is > 63 then add the 35 point bonus
                                bonus0 = 35
                            else:
                                bonus0 = 0
                            topGrandTotal0 = topTotal0 + bonus0 # sum the top grand total
                            grandTotal0 = bottomTotal0 + topGrandTotal0 # sum the top and bottom grand totals
                        elif yTuple[1] == 1: # repeat for column 1
                            topTotal1 += yTuple[2]
                            if topTotal1 >= 63:
                                bonus1 = 35
                            else:
                                bonus1 = 0
                            topGrandTotal1 = topTotal1 + bonus1
                            grandTotal1 = bottomTotal1 + topGrandTotal1
                        else: # repeat for column 2
                            topTotal2 += yTuple[2]
                            if topTotal2 >= 63:
                                bonus2 = 35
                            else:
                                bonus2 = 0
                            topGrandTotal2 = topTotal2 + bonus2
                            grandTotal2 = bottomTotal2 + topGrandTotal2
                    else: # we are in the lower section
                        if yTuple[1] == 0: # add the value to the lower total for column 0
                            bottomTotal0 += yTuple[2]
                            grandTotal0 = bottomTotal0 + topGrandTotal0 + yahtzeeBonusList[0]
                        elif yTuple[1] == 1: # same for column 1
                            bottomTotal1 += yTuple[2]
                            grandTotal1 = bottomTotal1 + topGrandTotal1 + yahtzeeBonusList[1]
                        else: # same for column 2
                            bottomTotal2 += yTuple[2]
                            grandTotal2 = bottomTotal2 + topGrandTotal2 + yahtzeeBonusList[2]
        yGrandTotal = grandTotal2 * 3 + grandTotal1 * 2 + grandTotal0 # multiply col two by 3 and col two by 2, add
        self.label.setText("Grand Total = " + str(yGrandTotal))
        # this section updates the table with the values generated above
        item = QTableWidgetItem(str(topTotal0))
        self.yahtzeeTable.setItem(6, 0, item)
        item = QTableWidgetItem(str(topTotal1))
        self.yahtzeeTable.setItem(6, 1, item)
        item = QTableWidgetItem(str(topTotal2))
        self.yahtzeeTable.setItem(6, 2, item)
        item = QTableWidgetItem(str(bonus0))
        self.yahtzeeTable.setItem(7, 0, item)
        item = QTableWidgetItem(str(bonus1))
        self.yahtzeeTable.setItem(7, 1, item)
        item = QTableWidgetItem(str(bonus2))
        self.yahtzeeTable.setItem(7, 2, item)
        item = QTableWidgetItem(str(topGrandTotal0))
        self.yahtzeeTable.setItem(8, 0, item)
        item = QTableWidgetItem(str(topGrandTotal1))
        self.yahtzeeTable.setItem(8, 1, item)
        item = QTableWidgetItem(str(topGrandTotal2))
        self.yahtzeeTable.setItem(8, 2, item)
        item = QTableWidgetItem(str(bottomTotal0))
        self.yahtzeeTable.setItem(18, 0, item)
        item = QTableWidgetItem(str(bottomTotal1))
        self.yahtzeeTable.setItem(18, 1, item)
        item = QTableWidgetItem(str(bottomTotal2))
        self.yahtzeeTable.setItem(18, 2, item)
        item = QTableWidgetItem(str(grandTotal0))
        self.yahtzeeTable.setItem(19, 0, item)
        item = QTableWidgetItem(str(grandTotal1))
        self.yahtzeeTable.setItem(19, 1, item)
        item = QTableWidgetItem(str(grandTotal2))
        self.yahtzeeTable.setItem(19, 2, item)

    def endGame(self): # helper function to end the game
        gameOver = True # set the flag for game over to true
        self.playAgain.show() # show the play again button

    def newGame(self): # helper function to start a new game
        global yTableList
        global yahtzeeBonus
        self.playAgain.hide() # hide the play again button
        for i in range(5): # reset all of the die objects to 0 and white
            dieObject = diceGroup[i]
            dieObject.icon = ("Dice/w0.jpg")
            dieObject.isClicked = 0
            iconName = dieObject.icon
            buttonList[i].setIcon(QIcon(iconName))
            QApplication.processEvents()
        yTableList = [] # clear the ytabledList for a new game
        yahtzeeBonus = 0
        for col in range(3): # reset each column
            for row in range(20): # and row
                item = QTableWidgetItem(str("")) # to blank
                self.yahtzeeTable.setItem(row, col, item)

    def rollDice(self): # helper method to roll the dice
        global dieRolls
        global diceRolled
        global tableClicked
        global yahtzeeJoker
        global autoFill

        if gameOver == False: # if not in a game over state
            if diceRolled == False: # if the dice have not been rolled yet
                yahtzeeJoker = False
                autoFill = False
                tableClicked = False # toggle these flag values
                diceRolled = True
                dieRolls = 0 # reset die rolls to zero
                for i in range(5): # since this is the first roll turn all yellow dice to white and
                    dieObject = diceGroup[i]
                    dieObject.icon = ("Dice/w" + str(dieObject.pip) + ".jpg")
                    dieObject.isClicked = 0 # reset the isClicked value to 0
                    iconName = dieObject.icon
                    buttonList[i].setIcon(QIcon(iconName)) # update the buttons tha actually display the dice
                    QApplication.processEvents() # again without this the incons will not update

            if dieRolls < 3: # if not pas the end of dice rolls
                for i in range(10): # we're goining to go through 10 different dice values to simulate a roll
                    for j in range(5): # go through each die
                        if diceGroup[j].isClicked == 0: # if the die can be rolled (ie not clicked)
                            lastTime = 0 # set the lastTime flag to zero
                            if i == 9: # on the last of the 10 rolls
                                lastTime = 1 # set last time to 1 to set the die button values
                            self.showDie(diceGroup[j], j, lastTime) # call show dice to display the icons
                    time.sleep(.07) # short sleep to slow down the roll 70 ms
                #dieRolls += 1 # increment dieRolls toward three
                rollsLeft = 3-dieRolls # rolls left will be displayed on the roll button
                _translate = QtCore.QCoreApplication.translate
                if dieRolls == 2: # if there is one roll left mahe roll singular
                    self.rollButton.setText(_translate("MainWindow", (str(rollsLeft) + " Roll Left")))
                else: # otherwise make plural
                    self.rollButton.setText(_translate("MainWindow", (str(rollsLeft) + " Rolls Left")))


    def showDie(self, dieObject, rollingDie, lastTime): #helper method to display the dice
        pip = random.randint(1, 6) # generate a random number between 1 and 6
        #pip = 6 #for testing yahtzee bonus logic
        dieObject.icon = ("Dice/w" + str(pip) + ".jpg") #set the icon image
        iconName = dieObject.icon
        buttonList[rollingDie].setIcon(QIcon(iconName))
        QApplication.processEvents() # again must be called to update the icon images
        if lastTime == 1: # if this is the last roll then
            dieObject.pip = pip # set the die object's pip value to the random number for use later
