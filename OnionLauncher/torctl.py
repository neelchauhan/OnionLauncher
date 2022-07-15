import os
from PyQt5.QtWidgets import QMessageBox

def startTor(parent, config_dict):

	TORRC_PATH = "/etc/tor/torrc"

	try:

		if os.path.exists(TORRC_PATH) and os.path.isfile(TORRC_PATH):
				
			with open(TORRC_PATH, "r") as f:
				torrc_textlist = f.readlines()

			
			with open(TORRC_PATH, "w") as f:
				f.writelines(torrc_textlist)

			command = 'systemctl start tor'
			os.system(command)

	except: # Output error if one is encountered
		QMessageBox.critical(parent, "Error", "dummy")


def stopTor():
	# Stop Tor if it is an option in the process descriptor
	command = 'systemctl stop tor'
	os.system(command)
