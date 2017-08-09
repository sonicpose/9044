import os
import core
import urllib.request
import urllib.parse
import re
import sys

def main():
	videoIDs = scrape('https://www.youtube.com/playlist?list=PLgPKmF5rEZ5pMxmluLP91GgrNt6WPLNnj')
	watchedCheck(playlistURL, videoIDs)

	return

def download(videoURL):
	cmd = 'youtube-dl ' + videoURL
	txt = "cmd = " + cmd
	log(txt)
	os.system(cmd)

	return True

def log(text):
	w = open('log', 'a')
	
	w.write(text + "\n")

	w.close

	return True

def scrape(playlistURL):
	query_string = urllib.parse.urlencode({"search_query" : PlaylistURL})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	print(search_results)

	return search_results

def watchedCheck(playlistURL, videoIDs):
	unwatchedVideoIDs = []
	watchedList = core.read(playlistURL)
	watchedIDs = core.split(watchedList)
	i = 0
	ii = 0
	while i < len(videoIDs):
		while ii < len(watchedIDs):
			if videoIDs[i] = watchedIDs[ii]:
				unwatchedVideoIDs.append(videoIDs[i])
			ii = ii + 1
		i = i + 1

	return unwatchedVideoIDs

main()