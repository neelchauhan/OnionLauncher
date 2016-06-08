import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from var import values
import torctl

class MainWindow(QMainWindow):
	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		loadUi("ui_files/main.ui", self)

		buttons = {
			self.tbAdd: self.addRow,
			self.tbRemove: self.removeRow,
			self.btnSwitchTor: self.switchTor,
			self.btnAbout: self.showAbout
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

	def optToDict(self):
		rows = self.twSettings.rowCount()
		output_dict = {}
		for row in range(rows):
			setting = self.twSettings.item(row, 0)
			parameter = self.twSettings.item(row, 1)
			output_dict[setting.text()] = parameter.text().split()
		return output_dict

	def switchTor(self):
		if values["torEnabled"]:
			values["torEnabled"] = False
			self.btnSwitchTor.setText("Start Tor")
			self.lblSwitchTor.setText("Tor Not Running")
			torctl.stopTor(values["process_desc"])
		else:
			values["torEnabled"] = True
			self.btnSwitchTor.setText("Stop Tor")
			self.lblSwitchTor.setText("Tor Running")
			values["process_desc"] = torctl.startTor(self.optToDict())
		QApplication.processEvents()

	def showAbout(self):
		message = "About OnionLauncher\n\n" \
				"Copyright 2016 Neel Chauhan\n" \
				"https://github.com/neelchauhan/OnionLauncher"
		QMessageBox.information(self, "Information", message)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec_())
