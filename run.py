import os
import core
import urllib.request
import urllib.parse
import re
import sys

def main():
	while True:
		downloadQueue = handleInput()
		queueDownloads(downloadQueue)
		playlistCheck()
		time.sleep(5)

	return

def handleInput():	#handleInput receives and sorts the information from the front end
	downloadQueue = []

	inputText = core.read('/opt/lampp/htdocs/data.txt')#data.txt is the file where the front end leaves the data for us
	print(inputText)
	core.write('/opt/lampp/htdocs/data.txt', '')
	inputArray = core.split(inputText)#inputText is split into an array so that we can interact with each line individually (Different URLs are put on different lines by the frontend).
	print(inputArray)

	i = 0#i is just an integer used for counting the times round a loop
	while i < len(inputArray):#This loop allows us to perform the same function on each line of the array. In this case it goes through each line and sorts it into a video url, a playlist url, or random text. And then the appropriate response is carried out
		inputData = inputArray[i]
		print(inputData)

		if 'list=' in inputData:#'list=' is unique to playlist urls
			core.log('playlists', inputData)
		if 'v=' in inputData:#v= is unique to video urls
			downloadQueue.append(inputData)

		i = i + 1

	return downloadQueue

def download(videoURL):#Download takes a video url and downloads the video
	cmd = 'youtube-dl -i ' + videoURL
	txt = "cd Downloads \n cmd = " + cmd
	log(txt)
	os.system(cmd)

	return True

def playlist(playlistURL):#Does all the playlist stuff
	videoIDs = scrape(playlistURL)#Scrapes the URL page and gets the video ids/urls
	print(videoIDs)
	playlistID = playlistURL.split('list=')[1]#converts playlist url into id for database
	unwatchedVideoIDs = watchedCheck(playlistID, videoIDs)#Checks what videos in playlist have already been downloaded

	i = 0
	while i < len(unwatchedVideoIDs):#Each iteration of the loop downloads a unwatched video in the playlist
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

def watchedCheck(playlistID, videoIDs):#Checks what videos in the playlist have already been downloaded (watched).
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

def queueDownloads(downloadQueue):#Runs a loop for every video not in a playlist that needs to be downloaded
	i = 0
	while i < len(downloadQueue):
		download(downloadQueue[i])
		i = i + 1

	return True

def playlistCheck():#Checks what playlists are being watched/should have new videos downloaded from then begins the playlist download process
	playlists = core.split(core.read('playlists'))

	i = 0
	while i < len(playlists):
		core.write(playlists[i].split('list=')[1], '')
		playlist(playlists[i])
		i = i + 1

	return

main()
