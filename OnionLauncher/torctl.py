import os
from PyQt5.QtWidgets import QMessageBox

def startTor(parent, config_dict):

	TORRC_PATH = "/etc/tor/torrc"

	eliminated_directive = ["UseBridges", "ClientTransportPlugin", "ClientTransportPlugin", "bridge", "Bridge", "HTTPSProxy", "HTTPSProxyAuthenticator", "Socks4Proxy", "Socks5Proxy", "Socks5ProxyUsername", "Socks5ProxyPassword"]

	try:

		if os.path.exists(TORRC_PATH) and os.path.isfile(TORRC_PATH):
				
			with open(TORRC_PATH, "r") as f:
				torrc_textlist = f.readlines()

			mod_torrc_textlist = [tmp for tmp in torrc_textlist if all(map(lambda x: not tmp.startswith(x) , eliminated_directive))]

			

			with open(TORRC_PATH, "w") as f:
				f.writelines(mod_torrc_textlist)

			command = 'systemctl start tor'
			os.system(command)

	except: # Output error if one is encountered
		QMessageBox.critical(parent, "Error", "dummy")


def stopTor():
	# Stop Tor if it is an option in the process descriptor
	command = 'systemctl stop tor'
	os.system(command)
