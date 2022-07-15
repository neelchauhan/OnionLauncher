import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from var import values, version
import torctl
from fn_handle import detect_filename

class MainWindow(QMainWindow):
	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		# Load .ui file
		loadUi(detect_filename("ui_files/main.ui"), self)

		# Define buttons
		buttons = {
			self.btnSwitchTor: self.switchTor,
			self.btnAbout: self.showAbout
		}

		# Define Checkbox
		checkboxes = {
			self.CheckIsUseBridge: self.useBridge

		}

		self.evAddClick(buttons)
		self.evSwitchCheck(checkboxes)

	# Function to connect objects from dictionary
	def evAddClick(self, obj_dict):
		for obj in obj_dict:
			obj.clicked.connect(obj_dict[obj])

	def evSwitchCheck(self, obj_check):
		for obj in obj_check:
			obj.stateChanged.connect(obj_check[obj])
		

	# Function to set objects enabled or not
	def evSetListEnabled(self, lst, state):
		for item in lst:
			item.setEnabled(state)

	def useBridge(self, state):
		if state == Qt.Checked:
			self.RadioUseBuiltin.setEnabled(True)
			self.RadioUseCustom.setEnabled(True)
		else:
			self.RadioUseBuiltin.setEnabled(False)
			self.RadioUseCustom.setEnabled(False)


	# Function to add a blank row
	#def addRow(self):
	#	rowPos = self.twSettings.rowCount() # Get position
	#	self.twSettings.insertRow(rowPos)

	# Function to delete a selected row
	#def removeRow(self):
	#	rows = sorted(set(index.row() for index in self.twSettings.selectedIndexes())) # Get selected rows
	#	rows.reverse() # Reverse rows (we're deleting from last->first)

	#	for row in rows:
	#		self.twSettings.removeRow(row)

	def optToDict(self): # Function to conert options in a QTableWidget to a Python Dictionary
		rows = self.twSettings.rowCount() # Row count (we're iterating the hard way)
		output_dict = {}
		for row in range(rows):
			# Get values in two variables
			setting = self.twSettings.item(row, 0)
			parameter = self.twSettings.item(row, 1)
			# Add them to dictionary
			if setting is not None and parameter is not None:
				output_dict[setting.text()] = parameter.text().split()
		return output_dict

	def switchTor(self): # Enable (or Disable) Tor
		modList = [

			self.CheckIsUseBridge
			self.RadioUseBuiltin,
			self.RadioUseCustom
			self.EditorOfBridge

			self.CheckIsUseProxy
			self.EditorOfProxy

		]
		if values["torEnabled"]: # Turn off if Tor is on
			values["torEnabled"] = False
			self.btnSwitchTor.setText("Start Tor")
			self.lblSwitchTor.setText("Tor Not Running")
			self.evSetListEnabled(modList, True)
			torctl.stopTor()
		else: # Turn on Tor
			torctl.startTor(self, self.optToDict())
			# If Tor started correctly, then mark as "on"
			values["torEnabled"] = True
			self.btnSwitchTor.setText("Stop Tor")
			self.lblSwitchTor.setText("Tor Running")
			self.evSetListEnabled(modList, False)
		# Refresh elements
		QApplication.processEvents()

	def showAbout(self): # Show about dialog
		message = "About OnionLauncher " + version + "\n\n" \
				"Copyright 2016 Neel Chauhan\n" \
				"This Version is modified by @infoengine1337\n" \
				"https://github.com/infoengine1337/OnionLauncher"

		QMessageBox.information(self, "Information", message)

def main_loop():
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main_loop()
