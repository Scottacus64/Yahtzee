from YahtzeePackage.YahtzeeGUI import Ui_MainWindow
from YahtzeePackage.Dice import Dice
from YahtzeePackage.DieSet import DieSet
from PyQt5 import QtWidgets

dieGroup = []


class test(object):
    def __init__(self):
        pass

    def leftClick(self, row, column):
        print('left', row, column)

    def rightClick(self, row, column):
        print('right', row, column)


def main():
    import sys
    ds = DieSet()
    #ds.printDieSet()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()