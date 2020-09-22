import sys
import time
import math
import random

from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QCheckBox, QLabel)
from PyQt5 import QtCore

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

path = []
blocked = []

class position:
	def __init__(self,pos):
		self.x = pos[0]
		self.y = pos[1]

	def print(self):
		print(str(self.x) + " " + str(self.y))

	def toTuple(self):
		return (self.x, self.y)

class pose:
	def __init__(self, pos, orientation):
		self.position = position(pos)
		self.orientation = orientation

	def print(self, log):
		if log:
			print(str(self.position.x) + " " + str(self.position.y) + " " + str(self.orientation))
		else:
			return str(self.position.x) + " " + str(self.position.y) + " " + str(self.orientation)

	def __copy__(self):
		self.normalizeArgs()
		return pose((self.position.x, self.position.y), self.orientation)

	def normalizeArgs(self):
		if not hasattr(self, "position"):
			self.position = None
		if not hasattr(self, "orientation"):
			self.orientation = None

class robot:
	def __init__(self, position, orientation):
		self.pose = pose(position, orientation)
		self.distance = 0
		self.visited = []
		self.visited.append(self.pose.position.toTuple())
		self.last_bisection = None
		self.previous_pose = self.pose

	def printPoseAndDistance(self):
		print(self.pose.print(log=False) +" "+ str(round(self.distance)))

	def move(self, goal):
		#print(blocked)
		dist2robot = [resolution, math.sqrt(2)*resolution]
		x_sgn = [0, 1, 1, 1, 0, -1, -1, -1]
		y_sgn = [1, 1, 0, -1, -1, -1, 0, 1]
		direction = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
		
		around = [0, 0, 0, 0, 0, 0, 0, 0]
		check = position((0,0))
		for i in range(8):
			check.x = self.pose.position.x + x_sgn[i] * resolution
			check.y = self.pose.position.y + y_sgn[i] * resolution
			check2 = check.toTuple()
			if check2 in self.visited:
				penalizacion = self.visited.count(check2)*resolution*5
			else:
				penalizacion = 0
			if check2 not in blocked:
				around[i] = dist2robot[i%2] + math.sqrt(pow(check.x-goal.x,2)+pow(check.y-goal.y,2)) + penalizacion
			else:
				around[i] = float("inf")
			for i in (0, 2, 4, 6):
				if i == 6:
					j = 0
				else: 
					j = i+2
				if around[i] == float("inf") and around[(j)] == float("inf"):
					around[i+1] = float("inf")
		
		minimum = float("inf")	
		for a in around:
			if a < minimum and a != float("inf"):
				minimum = a

		if around.count(minimum) > 1:
			min_idx = [i for i, value in enumerate(around) if value == minimum]
			idx = min_idx[random.randint(0,1)]
			self.last_bisection = self.pose.position
		else:
			idx = around.index(minimum)

		self.previous_pose = self.pose.__copy__()

		self.pose.position.x = self.pose.position.x + x_sgn[idx]*resolution
		self.pose.position.y = self.pose.position.y + y_sgn[idx]*resolution
		self.pose.orientation = direction[idx]
		self.distance = self.distance + dist2robot[idx%2]
		#self.printPoseAndDistance()
		self.visited.append(self.pose.position.toTuple())
		path.append(self.pose.__copy__())
		#return(self.pose.__copy__())

class obstaclesSelectionWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.obstacle_layout = QGridLayout()
		self.setLayout(self.obstacle_layout)

		self.Xlabel = QLabel('X')
		self.Slabel = QLabel(' ')

		self.boton = QPushButton('Aceptar')
		self.obstacle_layout.addWidget(self.boton, maxRange+1, maxRange+1)
		self.boton.clicked.connect(self.confirm)

		for x in range(maxRange):
			for y in range(maxRange):
				checkBox = QCheckBox()
				self.obstacle_layout.addWidget(checkBox, x, y)

		self.setWindowTitle('Select obstacles position')

	def confirm(self):
		blocked.clear()
		if not self.boton.isChecked():
			for x in range(maxRange):
				for y in range(maxRange):
					widget = self.obstacle_layout.itemAtPosition(x,y)
					chckbx = widget.widget()
					if chckbx.isChecked():
						blocked.append((x,y))
		
			
			

class obstaclesWindow(QWidget):
	def __init__(self,robot):
		super().__init__()
		self.obstacle_layout = QGridLayout()
		self.setLayout(self.obstacle_layout)

		self.boton = QPushButton('Actualizar')
		self.obstacle_layout.addWidget(self.boton, maxRange+1, maxRange+1)
		self.boton.clicked.connect(self.update)
		self.robot = robot

		for x in range(maxRange):
			for y in range(maxRange):
				Slabel = QLabel('_')
				self.obstacle_layout.addWidget(Slabel,x,y)
				
		self.setWindowTitle('Obstacles Map')

	def update(self):
		for x in range(maxRange):
			for y in range(maxRange):
				self.obstacle_layout.itemAtPosition(x,y).widget().setText("_")

		for point in blocked:
			self.obstacle_layout.itemAtPosition(point[0],point[1]).widget().setText("X")

		path.append(self.robot.pose.__copy__())

		while 1:
			self.robot.move(end)
			if self.robot.pose.position.x == end.x and self.robot.pose.position.y == end.y:
				break

		print(" ====== ====== ======")
		print("Distance = " + str(round(self.robot.distance)))
		print("Followed path: ")
		for p in path:
			p.print(log=True)
		print(" ====== ====== ======")

		for i,point in enumerate(path):
			if(self.obstacle_layout.itemAtPosition(point.position.x,point.position.y) is not None):
				self.obstacle_layout.itemAtPosition(point.position.x,point.position.y).widget().setText(str(i))


if __name__ == '__main__':
	start = position((1, 1))
	end = position((10, 13))
	robot = robot(start.toTuple(), 'N')

	app = QApplication(sys.argv)
	window1 = obstaclesSelectionWindow()
	window1.show()
	window2 = obstaclesWindow(robot)
	window2.show()
	sys.exit(app.exec_())

	