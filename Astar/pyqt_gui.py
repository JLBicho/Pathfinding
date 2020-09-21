import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QCheckBox, QLabel)
from PyQt5 import QtCore
import time

maxRange = 10
resolution = 10;

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

		self.setWindowTitle('Basic Grid Layout')

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
	def __init__(self):
		super().__init__()
		self.obstacle_layout = QGridLayout()
		self.setLayout(self.obstacle_layout)

		self.boton = QPushButton('Actualizar')
		self.obstacle_layout.addWidget(self.boton, maxRange+1, maxRange+1)
		self.boton.clicked.connect(self.update)

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
			#self.obstacle_layout.removeWidget(self.obstacle_layout.itemAtPosition(point[0],point[1]).widget());
			#self.obstacle_layout.addWidget(Xlabel,point[0],point[1])

		for i,point in enumerate(path):
			self.obstacle_layout.itemAtPosition(point[0],point[1]).widget().setText(str(i))
			




		


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
	
