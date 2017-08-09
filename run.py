import os
import core
import urllib.request
import urllib.parse
import re
import sys

def main():
	playlist('https://www.youtube.com/playlist?list=PLDSOKOxxjY4TwbUiMFn0Ghn5ulOThjDZb')

	return

def download(videoURL):
	cmd = 'youtube-dl ' + videoURL
	txt = "cmd = " + cmd
	log(txt)
	os.system(cmd)

	return True

def playlist(playlistURL):
	videoIDs = scrape(playlistURL)
	playlistID = playlistURL.split('list=')[1]
	unwatchedVideoIDs = watchedCheck(playlistID, videoIDs)

	i = 0
	while i < len(unwatchedVideoIDs):
		videoURL = 'http://www.youtube.com/watch?v='+unwatchedVideoIDs[i]
		print(videoURL)
		if download(videoURL):
			core.log(playlistURL, unwatchedVideoIDs[i])

	return True

def scrape(playlistURL):
	query_string = urllib.parse.urlencode({"search_query" : playlistURL})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
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

main()