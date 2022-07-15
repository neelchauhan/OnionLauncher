import os, sys, time
import re
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from var import values, version
import torctl
from fn_handle import detect_filename

import stem
import stem.control
import stem.socket
from stem.connection import connect

control_cookie_path = '/var/lib/tor/control.authcookie'
control_socket_path = '/run/tor/control'




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
		if self.CheckIsUseBridge.isChecked():
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

		builtin_torbridges_list = [
         "Bridge obfs4 144.217.20.138:80 FB70B257C162BF1038CA669D568D76F5B7F0BABB cert=vYIV5MgrghGQvZPIi1tJwnzorMgqgmlKaB77Y3Z9Q/v94wZBOAXkW+fdx4aSxLVnKO+xNw iat-mode=0",
         "Bridge obfs4 85.31.186.26:443 91A6354697E6B02A386312F68D82CF86824D3606 cert=PBwr+S8JTVZo6MPdHnkTwXJPILWADLqfMGoVvhZClMq/Urndyd42BwX9YFJHZnBB3H0XCw iat-mode=0",
         "Bridge obfs4 37.218.245.14:38224 D9A82D2F9C2F65A18407B1D2B764F130847F8B5D cert=bjRaMrr1BRiAW8IE9U5z27fQaYgOhX1UCmOpg2pFpoMvo6ZgQMzLsaTzzQNTlm7hNcb+Sg iat-mode=0",
         "Bridge obfs4 193.11.166.194:27025 1AE2C08904527FEA90C4C4F8C1083EA59FBC6FAF cert=ItvYZzW5tn6v3G4UnQa6Qz04Npro6e81AP70YujmK/KXwDFPTs3aHXcHp4n8Vt6w/bv8cA iat-mode=0",
         "Bridge obfs4 [2a0c:4d80:42:702::1]:27015 C5B7CD6946FF10C5B3E89691A7D3F2C122D2117C cert=TD7PbUO0/0k6xYHMPW3vJxICfkMZNdkRrb63Zhl5j9dW3iRGiCx0A7mPhe5T2EDzQ35+Zw iat-mode=0",
         "Bridge obfs4 45.145.95.6:27015 C5B7CD6946FF10C5B3E89691A7D3F2C122D2117C cert=TD7PbUO0/0k6xYHMPW3vJxICfkMZNdkRrb63Zhl5j9dW3iRGiCx0A7mPhe5T2EDzQ35+Zw iat-mode=0",
         "Bridge obfs4 209.148.46.65:443 74FAD13168806246602538555B5521A0383A1875 cert=ssH+9rP8dG2NLDN2XuFw63hIO/9MNNinLmxQDpVa+7kTOa9/m+tGWT1SmSYpQ9uTBGa6Hw iat-mode=0",
         "Bridge obfs4 85.31.186.98:443 011F2599C0E9B27EE74B353155E244813763C3E5 cert=ayq0XzCwhpdysn5o0EyDUbmSOx3X/oTEbzDMvczHOdBJKlvIdHHLJGkZARtT4dcBFArPPg iat-mode=0",
         "Bridge obfs4 193.11.166.194:27015 2D82C2E354D531A68469ADF7F878FA6060C6BACA cert=4TLQPJrTSaDffMK7Nbao6LC7G9OW/NHkUwIdjLSS3KYf0Nv4/nQiiI8dY2TcsQx01NniOg iat-mode=0",
         "Bridge obfs4 51.222.13.177:80 5EDAC3B810E12B01F6FD8050D2FD3E277B289A08 cert=2uplIpLQ0q9+0qMFrK5pkaYRDOe460LL9WHBvatgkuRr/SL31wBOEupaMMJ6koRE6Ld0ew iat-mode=0",
         "Bridge obfs4 38.229.33.83:80 0BAC39417268B96B9F514E7F63FA6FBA1A788955 cert=VwEFpk9F/UN9JED7XpG1XOjm/O8ZCXK80oPecgWnNDZDv5pdkhq1OpbAH0wNqOT6H6BmRQ iat-mode=1",
         "Bridge obfs4 193.11.166.194:27020 86AC7B8D430DAC4117E9F42C9EAED18133863AAF cert=0LDeJH4JzMDtkJJrFphJCiPqKx7loozKN7VNfuukMGfHO0Z8OGdzHVkhVAOfo1mUdv9cMg iat-mode=0",
         "Bridge obfs4 192.95.36.142:443 CDF2E852BF539B82BD10E27E9115A31734E378C2 cert=qUVQ0srL1JI/vO6V6m/24anYXiJD3QP2HgzUKQtQ7GRqqUvs7P+tG43RtAqdhLOALP7DJQ iat-mode=1",
         "Bridge obfs4 38.229.1.78:80 C8CBDB2464FC9804A69531437BCF2BE31FDD2EE4 cert=Hmyfd2ev46gGY7NoVxA9ngrPF2zCZtzskRTzoWXbxNkzeVnGFPWmrTtILRyqCTjHR+s9dg iat-mode=1",
         "Bridge obfs4 146.57.248.225:22 10A6CD36A537FCE513A322361547444B393989F0 cert=K1gDtDAIcUfeLqbstggjIw2rtgIKqdIhUlHp82XRqNSq/mtAjp1BIC9vHKJ2FAEpGssTPw iat-mode=0"
        ]

		output_dict = {}
		bridges_list = []
		proxies_list =  []

		if self.CheckIsUseBridge.isChecked():

			bridges_list.extend(["UseBridges 1","ClientTransportPlugin obfs2,obfs3 exec /usr/bin/obfsproxy managed","ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy managed"])

			if self.RadioUseBuiltin.isChecked():
				bridges_list.extend(builtin_torbridges_list)
			else:
				bridges_list.extend(self.EditorOfBridge.toPlainText().split("\n"))

		else:
			bridges_list.extend(["UseBridges 0"])

			
		if self.CheckIsUseBridge.isChecked():
			proxies_list = self.EditorOfProxy.toPlainText().split("\n")

		output_dict.update[("bridges_list", bridges_list), ("proxies_list", proxies_list)]
		
		return output_dict


	def switchTor(self): # Enable (or Disable) Tor
		
		modList = [

			self.CheckIsUseBridge,
			self.RadioUseBuiltin,
			self.RadioUseCustom,
			self.EditorOfBridge,

			self.CheckIsUseProxy,
			self.EditorOfProxy

		]

		tag_phase = {'starting': 'Starting',
                    'conn': 'Connecting to a relay',
                    'conn_dir': 'Connecting to a relay directory',
                    'conn_done_pt': "Connected to pluggable transport",
                    'handshake_dir': 'Finishing handshake with directory server',
                    'onehop_create': 'Establishing an encrypted directory connection',
                    'requesting_status': 'Retrieving network status',
                    'loading_status': 'Loading network status',
                    'loading_keys': 'Loading authority certificates',
                    'enough_dirinfo': 'Loaded enough directory info to build circuits',
                    'ap_conn': 'Connecting to a relay to build circuits',
                    'ap_conn_done': 'Connected to a relay to build circuits',
                    'ap_conn_done_pt': 'Connected to pluggable transport to build circuits',
                    'ap_handshake': 'Finishing handshake with a relay to build circuits',
                    'ap_handshake_done': 'Handshake finished with a relay to build circuits',
                    'requesting_descriptors': 'Requesting relay information',
                    'loading_descriptors': 'Loading relay information',
                    'conn_or': 'Connecting to the Tor network',
                    'conn_done': "Connected to a relay",
                    'handshake': "Handshaking with a relay",
                    'handshake_or': 'Finishing handshake with first hop',
                    'circuit_create': 'Establishing a Tor circuit',
                    'done': 'Connected to the Tor network!'
					}


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

			count=0
			while not os.path.exists(control_socket_path) and count < 5:
				count += 0.2
				time.sleep(0.2)

			tor_controller = stem.control.Controller.from_socket_file(control_socket_path)
			tor_controller.authenticate(control_cookie_path)


			bootstrap_percent = 0
			while bootstrap_percent < 100:
				bootstrap_status = tor_controller.get_info("status/bootstrap-phase")

				if bootstrap_status != previous_status:
					bootstrap_percent = int(re.match('.* PROGRESS=([0-9]+).*', bootstrap_status).group(1))
					bootstrap_tag = re.search(r'TAG=(.*) +SUMMARY', bootstrap_status).group(1)

					if bootstrap_tag in tag_phase:
						bootstrap_phase = tag_phase[bootstrap_tag]

					previous_status = bootstrap_status
				
				self.TorProgress.setValue(bootstrap_percent)
				self.textBrowser.setText(self.textBrowser.toPlainText() + "{}\n".format(bootstrap_tag))

				QApplication.processEvents()
				time.sleep(0.2)

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
