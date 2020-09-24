import sys
import time
import math
import random

import settings
from robot import robot
from geometry_utils import position, pose
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QCheckBox, QLabel, QGroupBox, QHBoxLayout, QLineEdit)
from PyQt5 import QtCore

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()

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

		for x in range(settings.maxRange):
			for y in range(settings.maxRange):
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
		
		self.update_btn = QPushButton('GO!')
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
		self.input_EX = QLineEdit(str(settings.maxRange-1))
		label_EY = QLabel("End_Y:")
		self.input_EY = QLineEdit(str(settings.maxRange-1))
		self.topLeftLayout.addWidget(label_SX)
		self.topLeftLayout.addWidget(self.input_SX)
		self.topLeftLayout.addWidget(label_SY)
		self.topLeftLayout.addWidget(self.input_SY)
		self.topLeftLayout.addWidget(label_EX)
		self.topLeftLayout.addWidget(self.input_EX)
		self.topLeftLayout.addWidget(label_EY)
		self.topLeftLayout.addWidget(self.input_EY)

		self.sent_btn = QPushButton('Send')
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

	def restrictXY(self,val, min, max):
		if val<min:
			val = min
		if val>max:
			val=max
		return val

	def enviar(self):
		start_x = int(self.input_SX.text())
		start_y = int(self.input_SY.text())
		end_x = int(self.input_EX.text())
		end_y = int(self.input_EY.text())
		start_x = self.restrictXY(start_x,0,settings.maxRange-1)
		start_y = self.restrictXY(start_y,0,settings.maxRange-1)
		end_x = self.restrictXY(end_x,0,settings.maxRange-1)
		end_y = self.restrictXY(end_y,0,settings.maxRange-1)
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
		if self.start is None or self.end is None:
			self.distance.setText("No start or end specified! Press 'Send' to confirm positions")
			return
		settings.blocked.clear()
		if not self.update_btn.isChecked():
			for x in range(settings.maxRange):
				for y in range(settings.maxRange):
					self.pathGridLayout.itemAtPosition(x,y).widget().setText("_")
					if (x,y) !=  self.start.toTuple() and (x,y) != self.end.toTuple():
						widget = self.selectionGridLayout.itemAtPosition(x,y)
						chckbx = widget.widget()
						if chckbx.isChecked():
							settings.blocked.append((x,y))

		settings.path.clear()
		for point in settings.blocked:
			self.pathGridLayout.itemAtPosition(point[0],point[1]).widget().setText("X")

		settings.path.append(self.robot1.pose.__copy__())

		while 1:
			self.robot1.move(self.end)
			if self.robot1.pose.position.x == self.end.x and self.robot1.pose.position.y == self.end.y:
				string = "{:.1f}".format(self.robot1.distance)
				self.distance.setText(string)
				break
			if self.robot1.distance > int(self.maxDistance.text()):
				string = "{:.1f}".format(self.robot1.distance)
				self.distance.setText("Max. distance reached: "+ string)
				break

		for i,point in enumerate(settings.path):
			if(self.pathGridLayout.itemAtPosition(point.position.x,point.position.y) is not None):
				self.pathGridLayout.itemAtPosition(point.position.x,point.position.y).widget().setText(str(i))

		if self.start is not None:
			self.robot1 = robot(self.start.toTuple(), 'N')

	def reset(self):
		for x in range(settings.maxRange):
			for y in range(settings.maxRange):
				self.selectionGridLayout.itemAtPosition(x,y).widget().deleteLater()
				self.pathGridLayout.itemAtPosition(x,y).widget().setText("_")
				self.selectionGridLayout.addWidget(QCheckBox(), x, y)
		self.start = None
		self.end = None
