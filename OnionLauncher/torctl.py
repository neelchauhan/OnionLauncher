import stem.process
from PyQt5.QtWidgets import QMessageBox

def startTor(parent, config):
	process = None
	try:
		if config:
			process = stem.process.launch_tor_with_config(config, take_ownership = True)
		else:
			default_config = {
				"SocksPort": "9050"
			}
			process = stem.process.launch_tor_with_config(default_config, take_ownership = True)
	except OSError as err_m:
		QMessageBox.critical(parent, "Error", str(err_m))

	return process

def stopTor(process):
	if "kill" in dir(process):
		process.kill()
