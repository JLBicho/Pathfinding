import sys
import time
import math
import random
from astar_algoritm import robot
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QCheckBox, QLabel)
from PyQt5 import QtCore
from pyqt_gui import (obstaclesSelectionWindow,obstaclesWindow)

maxRange = 10
resolution = 10;


global path, blocked
blocked = []
path = []

if __name__ == '__main__':
	for x in range(maxRange):
		for y in range(maxRange):
			if x==y:
				path.append((x,y))
				
	app = QApplication(sys.argv)
	window1 = obstaclesSelectionWindow()
	window1.show()
	window2 = obstaclesWindow()
	window2.show()
	sys.exit(app.exec_())
	