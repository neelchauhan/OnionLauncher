import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from var import values

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
		if values["torEnabled"]:
			values["torEnabled"] = False
			self.btnSwitchTor.setText("Start Tor")
			self.lblSwitchTor.setText("Tor Not Running")
		else:
			values["torEnabled"] = True
			self.btnSwitchTor.setText("Stop Tor")
			self.lblSwitchTor.setText("Tor Running")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec_())
