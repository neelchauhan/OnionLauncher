import os
import stem.process
from PyQt5.QtWidgets import QMessageBox

def startTor(parent, config_dict):
	try:
		
		command = 'systemctl start tor'
		os.system(command)

	except: # Output error if one is encountered
		QMessageBox.critical(parent, "Error", str(err_m))


def stopTor():
	# Stop Tor if it is an option in the process descriptor
	command = 'systemctl stop tor'
	os.system(command)
