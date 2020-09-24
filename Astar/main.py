import sys
import time
import math
import random

import settings

from gui import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainwindow = MainWindow()
	mainwindow.resize(1200, 900)
	mainwindow.show()
	sys.exit(app.exec_())

	