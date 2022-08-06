import os
from PyQt5.QtWidgets import QMessageBox

def startTor(parent, config_dict):

	torrc_path = "/etc/tor/torrc"

	eliminated_directive = ["UseBridges", "ClientTransportPlugin", "ClientTransportPlugin", "bridge", "Bridge", "HTTPSProxy", "HTTPSProxyAuthenticator", "Socks4Proxy", "Socks5Proxy", "Socks5ProxyUsername", "Socks5ProxyPassword"]

	try:

		if os.path.exists(torrc_path) and os.path.isfile(torrc_path):
				
			with open(torrc_path, "r") as f:
				torrc_textlist = f.readlines()

			mod_torrc_textlist = [tmp for tmp in torrc_textlist if all(map(lambda x: not tmp.startswith(x) , eliminated_directive))]

			mod_torrc_textlist.extend(config_dict["bridges_list"]).extend(config_dict["proxies_list"])

			with open(torrc_path, "w") as f:
				f.writelines(mod_torrc_textlist)

			command = "systemctl start tor"
			os.system(command)

		else:
			QMessageBox.critical(parent, "Error", "torrc file does not exist.")

	except: # Output error if one is encountered
		QMessageBox.critical(parent, "Error", "an error happened.")


def stopTor():
	# Stop Tor if it is an option in the process descriptor
	command = "systemctl stop tor"
	os.system(command)
