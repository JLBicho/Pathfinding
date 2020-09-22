import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QCheckBox, QLabel)
from PyQt5 import QtCore
import time

maxRange = 10
resolution = 1;
borders = []
blocked = []

for i in range(-1,maxRange):
	borders.append((-resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append(((maxRange-1)*resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, -resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, (maxRange-1)*resolution))

path = []

class obstaclesSelectionWindow(QWidget):
	def __init__(self, maxRange, blocked):
		super().__init__()
		self.obstacle_layout = QGridLayout()
		self.setLayout(self.obstacle_layout)

		self.Xlabel = QLabel('X')
		self.Slabel = QLabel(' ')

		self.boton = QPushButton('Aceptar')
		self.obstacle_layout.addWidget(self.boton, maxRange+1, maxRange+1)
		self.boton.clicked.connect(self.confirm)
		self.blocked = blocked

		for x in range(maxRange):
			for y in range(maxRange):
				checkBox = QCheckBox()
				self.obstacle_layout.addWidget(checkBox, x, y)

		self.setWindowTitle('Basic Grid Layout')

	def confirm(self):
		self.blocked.clear()
		if not self.boton.isChecked():
			for x in range(maxRange):
				for y in range(maxRange):
					widget = self.obstacle_layout.itemAtPosition(x,y)
					chckbx = widget.widget()
					if chckbx.isChecked():
						self.blocked.append((x,y))
		
			
			

class obstaclesWindow(QWidget):
	def __init__(self,maxRange,path,blocked):
		super().__init__()
		self.obstacle_layout = QGridLayout()
		self.setLayout(self.obstacle_layout)

		self.boton = QPushButton('Actualizar')
		self.obstacle_layout.addWidget(self.boton, maxRange+1, maxRange+1)
		self.boton.clicked.connect(self.update)
		self.path = path
		self.blocked = blocked

		for x in range(maxRange):
			for y in range(maxRange):
				Slabel = QLabel('_')
				self.obstacle_layout.addWidget(Slabel,x,y)
				
		self.setWindowTitle('Obstacles Map')

	def update(self):
		for x in range(maxRange):
			for y in range(maxRange):
				self.obstacle_layout.itemAtPosition(x,y).widget().setText("_")

		for point in self.blocked:
			self.obstacle_layout.itemAtPosition(point[0],point[1]).widget().setText("X")

		for i,point in enumerate(self.path):
			if(self.obstacle_layout.itemAtPosition(point.position.x,point.position.y) is not None):
				self.obstacle_layout.itemAtPosition(point.position.x,point.position.y).widget().setText(str(i))
			

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
	
