import stem.process

def startTor(config):
	process = stem.process.launch_tor_with_config(config, take_ownership = True)

	return process

def stopTor(process):
	if "kil" in dir(process):
		process.kill()
