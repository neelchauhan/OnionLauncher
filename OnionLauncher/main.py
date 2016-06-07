import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		loadUi("ui_files/main.ui", self)

		self.tbAdd.clicked.connect(self.addRow)

	def addRow(self):
		rowPos = self.twSettings.rowCount()
		self.twSettings.insertRow(rowPos)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec_())
