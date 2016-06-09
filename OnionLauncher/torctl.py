import stem.process

def startTor(config):
	if config:
		process = stem.process.launch_tor_with_config(config, take_ownership = True)
	else:
		default_config = {
			"SocksPort": "9050"
		}
		process = stem.process.launch_tor_with_config(default_config, take_ownership = True)

	return process

def stopTor(process):
	if "kill" in dir(process):
		process.kill()
