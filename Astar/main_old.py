import sys
import time
import math
import random
from astar_algorithm import robot,position,pose
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QCheckBox, QLabel)
from PyQt5 import QtCore
from pyqt_gui import (obstaclesSelectionWindow,obstaclesWindow)




if __name__ == '__main__':


	maxRange = 15
	resolution = 1

	borders = []
	for i in range(-1,maxRange):
		borders.append((-resolution, i*resolution))
	for i in range(-1,maxRange):
		borders.append(((maxRange-1)*resolution, i*resolution))
	for i in range(-1,maxRange):
		borders.append((i*resolution, -resolution))
	for i in range(-1,maxRange):
		borders.append((i*resolution, (maxRange-1)*resolution))

	blocked = []
	path = []
	
	
	
	start = position((9, 9))
	end = position((1, 1))
	robot = robot(start.toTuple(), 'N', resolution=resolution, blocked=blocked)
	path.append(robot.pose.__copy__())	
	
	while 1:
		#robot.move(end)
		path.append(robot.move(end))	
		if robot.pose.position.x == end.x and robot.pose.position.y == end.y:
			break	

	for p in path:
		p.print(log=True)
	
	print(" ====== ====== ======")	
	app = QApplication(sys.argv)
	window1 = obstaclesSelectionWindow(maxRange,blocked)
	window1.show()
	window2 = obstaclesWindow(maxRange, path, blocked)
	window2.show()
	sys.exit(app.exec_())
	