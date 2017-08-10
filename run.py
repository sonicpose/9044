import os
import core
import urllib.request
import urllib.parse
import re
import sys

def main():
	downloadQueue = handleInput()
	queueDownloads(downloadQueue)
	playlistCheck()
	time.sleep(5)

	return

def handleInput():
	downloadQueue = []

	inputText = core.read('lampp/htdocs/data.txt')
	print(inputText)
	#core.write('data.txt', '')
	inputArray = core.split(inputText)
	print(inputArray)

	i = 0
	while i < len(inputArray):
		inputData = inputArray[i]
		print(inputData)

		if 'list=' in inputData:
			core.log('playlists', inputData)
		if 'v=' in inputData:
			downloadQueue.append(inputData)

		i = i + 1

	return downloadQueue

def download(videoURL):
	cmd = 'youtube-dl -i ' + videoURL
	txt = "cmd = " + cmd
	log(txt)
	os.system(cmd)

	return True

def playlist(playlistURL):
	videoIDs = scrape(playlistURL)
	print(videoIDs)
	playlistID = playlistURL.split('list=')[1]
	unwatchedVideoIDs = watchedCheck(playlistID, videoIDs)

	i = 0
	while i < len(unwatchedVideoIDs):
		videoURL = 'http://www.youtube.com/watch?v='+unwatchedVideoIDs[i]
		print(videoURL)
		if download(videoURL):
			core.log(playlistID, unwatchedVideoIDs[i])
		i = i + 1

	return True

def scrape(playlistURL):
	query_string = urllib.parse.urlencode({"search_query" : playlistURL})
	html_content = urllib.request.urlopen(playlistURL)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

	return search_results

def watchedCheck(playlistID, videoIDs):
	unwatchedVideoIDs = []
	watchedList = core.read(playlistID)
	watchedIDs = core.split(watchedList)
	i = 0
	while i < len(videoIDs):
		if videoIDs[i] not in watchedIDs:
			unwatchedVideoIDs.append(videoIDs[i])
		i = i + 1

	return unwatchedVideoIDs

def log(text):
	w = open('log', 'a')
	
	w.write(text + "\n")

	w.close

	return True

def queueDownloads(downloadQueue):
	i = 0
	while i < len(downloadQueue):
		download(downloadQueue[i])
		i = i + 1

	return True

def playlistCheck():
	playlists = core.split(core.read('playlists'))

	i = 0
	while i < len(playlists):
		core.write(playlists[i].split('list=')[1], '')
		playlist(playlists[i])
		i = i + 1

	return

main()
