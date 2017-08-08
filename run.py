import os
import core

def main():

	return

def download(videoURL):
	cmd = 'youtube-dl ' + videoURL
	core.log("cmd = " + cmd)
	os.system(cmd)

	return
