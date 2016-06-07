import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		loadUi("ui_files/main.ui", self)

		buttons = {
			self.tbAdd: self.addRow,
			self.tbRemove: self.removeRow,
			self.btnSwitchTor: self.switchTor,
		}

		self.evAddClick(buttons)

	def evAddClick(self, obj_dict):
		for obj in obj_dict:
			obj.clicked.connect(obj_dict[obj])

	def addRow(self):
		rowPos = self.twSettings.rowCount()
		self.twSettings.insertRow(rowPos)

	def removeRow(self):
		rows = sorted(set(index.row() for index in self.twSettings.selectedIndexes()))
		rows.reverse()

		for row in rows:
			self.twSettings.removeRow(row)

	def switchTor(self):
		pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec_())
