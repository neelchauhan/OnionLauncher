import stem.process
from PyQt5.QtWidgets import QMessageBox

def startTor(parent, config):
	process = None # Start with a blank process descriptor
	try:
		if config: # Start with a configuration
			process = stem.process.launch_tor_with_config(config, take_ownership = True)
		else: # Start with a default configuration if the values are blank
			default_config = {
				"SocksPort": "9050"
			}
			process = stem.process.launch_tor_with_config(default_config, take_ownership = True)
	except OSError as err_m: # Output error if one is encountered
		QMessageBox.critical(parent, "Error", str(err_m))

	return process

def stopTor(process):
	# Stop Tor if it is an option in the process descriptor
	if "kill" in dir(process):
		process.kill()
