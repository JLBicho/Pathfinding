import sys
import time
import math
import random

from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QCheckBox, QLabel, QGroupBox, QHBoxLayout, QLineEdit)
from PyQt5 import QtCore

maxRange = 20
resolution = 1
borders = []

for i in range(-1,maxRange):
	borders.append((-resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append(((maxRange)*resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, -resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, (maxRange)*resolution))

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
			if check2 not in blocked and check2 not in borders:
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
		self.obstacle_layout.addWidget(self.boton, maxRange+1 , maxRange+2)
		self.boton.clicked.connect(self.confirm)

		self.reset_btn = QPushButton('Reset')
		self.obstacle_layout.addWidget(self.reset_btn, maxRange+2 , maxRange+2)
		self.reset_btn.clicked.connect(self.reset)
		

		for x in range(maxRange):
			for y in range(maxRange):
				if (x,y) == start.toTuple():
					self.obstacle_layout.addWidget(QLabel("S"),x,y)
				elif (x,y) == end.toTuple():
					self.obstacle_layout.addWidget(QLabel("E"),x,y)
				else:
					checkBox = QCheckBox()
					self.obstacle_layout.addWidget(checkBox, x, y)

		self.setWindowTitle('Select obstacles position')

	def confirm(self):
		blocked.clear()
		if not self.boton.isChecked():
			for x in range(maxRange):
				for y in range(maxRange):
					if (x,y) !=  start.toTuple() and (x,y) != end.toTuple():
						widget = self.obstacle_layout.itemAtPosition(x,y)
						chckbx = widget.widget()
						if chckbx.isChecked():
							blocked.append((x,y))
		
	def reset(self):
		for x in range(maxRange):
			for y in range(maxRange):
				#self.obstacle_layout.removeWidget(self.obstacle_layout.itemAtPosition(x,y).widget())
				self.obstacle_layout.itemAtPosition(x,y).widget().deleteLater()
				if (x,y) == start.toTuple():
					self.obstacle_layout.addWidget(QLabel("S"),x,y)
				elif (x,y) == end.toTuple():
					self.obstacle_layout.addWidget(QLabel("E"),x,y)
				else:
					checkBox = QCheckBox()
					self.obstacle_layout.addWidget(checkBox, x, y)
			
			

class obstaclesWindow(QWidget):
	def __init__(self,robot1):
		super().__init__()
		self.obstacle_layout = QGridLayout()
		self.setLayout(self.obstacle_layout)

		self.update_btn = QPushButton('Actualizar')
		self.obstacle_layout.addWidget(self.update_btn, maxRange+1, maxRange+1)
		self.update_btn.clicked.connect(self.update)

		self.robot = robot1

		for x in range(maxRange):
			for y in range(maxRange):
				Slabel = QLabel('_')
				self.obstacle_layout.addWidget(Slabel,x,y)
				
		self.setWindowTitle('Obstacles Map')

	def update(self):
		path.clear()
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
			if self.robot.distance > 500:
				print(" ====== ====== ======")
				print(" MAX DISTANCE REACHED")
				print(" ====== ====== ======")
				break

		print(" ====== ====== ======")
		print("Distance = " + str(round(self.robot.distance)))
		'''
		print("Followed path: ")
		for p in path:
			p.print(log=True)
		'''
		print(" ====== ====== ======")

		for i,point in enumerate(path):
			if(self.obstacle_layout.itemAtPosition(point.position.x,point.position.y) is not None):
				self.obstacle_layout.itemAtPosition(point.position.x,point.position.y).widget().setText(str(i))

		if start is not None:
			self.robot = robot(start.toTuple(), 'N')

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		#self.robot = robot1
		self.setWindowTitle("Main Window")

		self.selectionGroup = QGroupBox("Selection")
		self.PathGroup = QGroupBox("Path")
		self.TopGroup = QGroupBox("Input Data")
		self.BottomGroup = QGroupBox("Control")
		self.SubBottomGroup = QGroupBox("Outputs")

		self.selectionGridLayout = QGridLayout()
		self.pathGridLayout = QGridLayout()
		self.buttonsLayout = QHBoxLayout()
		self.topLeftLayout = QHBoxLayout()
		self.outputsLayout = QHBoxLayout()

		for x in range(maxRange):
			for y in range(maxRange):
				checkBox = QCheckBox()
				self.selectionGridLayout.addWidget(checkBox, x, y)
				self.pathGridLayout.addWidget(QLabel('_'),x,y)
		
		self.selectionGroup.setLayout(self.selectionGridLayout)
		self.PathGroup.setLayout(self.pathGridLayout)
		self.TopGroup.setLayout(self.topLeftLayout)
		self.BottomGroup.setLayout(self.buttonsLayout)
		self.SubBottomGroup.setLayout(self.outputsLayout)

		mainLayout = QGridLayout()
		mainLayout.addWidget(self.TopGroup, 0, 0, 1, 2)
		mainLayout.addWidget(self.selectionGroup, 1, 0)
		mainLayout.addWidget(self.PathGroup, 1, 1)
		mainLayout.addWidget(self.BottomGroup, 2, 0, 1, 2)
		mainLayout.addWidget(self.SubBottomGroup, 3, 0, 1, 2)
		
		self.update_btn = QPushButton('Actualizar')
		self.buttonsLayout.addWidget(self.update_btn)
		self.update_btn.clicked.connect(self.update)

		self.reset_btn = QPushButton('Reset')
		self.buttonsLayout.addWidget(self.reset_btn)
		self.reset_btn.clicked.connect(self.reset)
		
		label_SX = QLabel("Start_X:")
		self.input_SX = QLineEdit('0')
		label_SY = QLabel("Start_Y:")
		self.input_SY = QLineEdit('0')
		label_EX = QLabel("End_X:")
		self.input_EX = QLineEdit(str(maxRange-1))
		label_EY = QLabel("End_Y:")
		self.input_EY = QLineEdit(str(maxRange-1))
		self.topLeftLayout.addWidget(label_SX)
		self.topLeftLayout.addWidget(self.input_SX)
		self.topLeftLayout.addWidget(label_SY)
		self.topLeftLayout.addWidget(self.input_SY)
		self.topLeftLayout.addWidget(label_EX)
		self.topLeftLayout.addWidget(self.input_EX)
		self.topLeftLayout.addWidget(label_EY)
		self.topLeftLayout.addWidget(self.input_EY)
		self.sent_btn = QPushButton('Enviar')
		self.topLeftLayout.addWidget(self.sent_btn)
		self.sent_btn.clicked.connect(self.enviar)

		self.start = None
		self.end = None

		distanceLabel = QLabel("Distance: ")
		self.distance = QLineEdit(" ")
		self.distance.setReadOnly(True)
		self.distance.setAlignment(QtCore.Qt.AlignCenter)
		maxDistanceLabel = QLabel("Max Distance: ")
		self.maxDistance = QLineEdit(str(500))
		self.maxDistance.setAlignment(QtCore.Qt.AlignCenter)
		self.outputsLayout.addWidget(distanceLabel)
		self.outputsLayout.addWidget(self.distance)
		self.outputsLayout.addWidget(maxDistanceLabel)
		self.outputsLayout.addWidget(self.maxDistance)
		self.outputsLayout

		self.setLayout(mainLayout)

	def enviar(self):
		start_x = int(self.input_SX.text())
		start_y = int(self.input_SY.text())
		end_x = int(self.input_EX.text())
		end_y = int(self.input_EY.text())
		start_x = restrictXY(start_x,0,maxRange-1)
		start_y = restrictXY(start_y,0,maxRange-1)
		end_x = restrictXY(end_x,0,maxRange-1)
		end_y = restrictXY(end_y,0,maxRange-1)
		self.input_SX.setText(str(start_x))
		self.input_SY.setText(str(start_y)) 
		self.input_EX.setText(str(end_x))
		self.input_EY.setText(str(end_y))

		if self.start is None and self.end is None:
			self.start = position((start_x, start_y))
			self.selectionGridLayout.itemAtPosition(start_x, start_y).widget().deleteLater()
			self.selectionGridLayout.addWidget(QLabel("S"),start_x,start_y)
			self.end = position((end_x, end_y))
			self.selectionGridLayout.itemAtPosition(end_x, end_y).widget().deleteLater()
			self.selectionGridLayout.addWidget(QLabel("E"),end_x, end_y)

		if self.start.toTuple() != (start_x, start_y):
			self.selectionGridLayout.itemAtPosition(self.start.x, self.start.y).widget().deleteLater()
			self.selectionGridLayout.addWidget(QCheckBox(), self.start.x, self.start.y)
			self.start = position((start_x, start_y))
			self.selectionGridLayout.itemAtPosition(start_x, start_y).widget().deleteLater()
			self.selectionGridLayout.addWidget(QLabel("S"),start_x,start_y)
			
		
		if self.end.toTuple() != (end_x, end_y):
			self.selectionGridLayout.itemAtPosition(self.end.x, self.end.y).widget().deleteLater()
			self.selectionGridLayout.addWidget(QCheckBox(), self.end.x, self.end.y)
			self.end = position((end_x, end_y))
			self.selectionGridLayout.itemAtPosition(end_x, end_y).widget().deleteLater()
			self.selectionGridLayout.addWidget(QLabel("E"),end_x, end_y)

		self.robot1 = robot(self.start.toTuple(), 'N')

	def update(self):
		blocked.clear()
		if not self.update_btn.isChecked():
			for x in range(maxRange):
				for y in range(maxRange):
					self.pathGridLayout.itemAtPosition(x,y).widget().setText("_")
					if (x,y) !=  self.start.toTuple() and (x,y) != self.end.toTuple():
						widget = self.selectionGridLayout.itemAtPosition(x,y)
						chckbx = widget.widget()
						if chckbx.isChecked():
							blocked.append((x,y))

		path.clear()
		for point in blocked:
			self.pathGridLayout.itemAtPosition(point[0],point[1]).widget().setText("X")

		path.append(self.robot1.pose.__copy__())

		while 1:
			self.robot1.move(self.end)
			if self.robot1.pose.position.x == self.end.x and self.robot1.pose.position.y == self.end.y:
				self.distance.setText(str(self.robot1.distance))
				break
			if self.robot1.distance > int(self.maxDistance.text()):
				self.distance.setText("Max. distance reached: "+ str(self.robot1.distance))
				'''
				print(" ====== ====== ======")
				print(" MAX DISTANCE REACHED")
				print(" ====== ====== ======")
				'''
				break
		'''
		print(" ====== ====== ======")
		print("Distance = " + str(round(self.robot1.distance)))
		
		print("Followed path: ")
		for p in path:
			p.print(log=True)
		
		print(" ====== ====== ======")
		'''
		for i,point in enumerate(path):
			if(self.pathGridLayout.itemAtPosition(point.position.x,point.position.y) is not None):
				self.pathGridLayout.itemAtPosition(point.position.x,point.position.y).widget().setText(str(i))

		if self.start is not None:
			self.robot1 = robot(self.start.toTuple(), 'N')

	def reset(self):
		for x in range(maxRange):
			for y in range(maxRange):
				self.selectionGridLayout.itemAtPosition(x,y).widget().deleteLater()
				self.pathGridLayout.itemAtPosition(x,y).widget().setText("_")
				self.selectionGridLayout.addWidget(QCheckBox(), x, y)



			

def restrictXY(val, min, max):
	if val<min:
		val = min
	if val>max:
		val=max
	return val

if __name__ == '__main__':
	'''
	start_x = int(input("Select start x: "))
	start_y = int(input("Select start y: "))
	start_x = restrictXY(start_x,1,maxRange-1)
	start_y = restrictXY(start_y,1,maxRange-1)
	start = position((start_x,start_y))
	end_x = int(input("Select end x: "))
	end_y = int(input("Select end y: "))
	end_x = restrictXY(end_x,1,maxRange-1)
	end_y = restrictXY(end_y,1,maxRange-1)
	end = position((end_x,end_y))
	robot1 = robot(start.toTuple(), 'N')
	
	start = position((0,0))
	end = position((maxRange-1,maxRange-1))
	robot1 = robot(start.toTuple(), 'N')
	'''

	app = QApplication(sys.argv)
	mainwindow = MainWindow()
	mainwindow.resize(1200, 900)
	mainwindow.show()
	#window1 = obstaclesSelectionWindow()
	#window1.show()
	#window2 = obstaclesWindow(robot1)
	#window2.show()
	sys.exit(app.exec_())

	