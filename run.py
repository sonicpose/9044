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

#handleInput receives and sorts the information from the front end
def handleInput():
	downloadQueue = []

	#data.txt is the file where the front end leaves the data for us
	inputText = core.read('/opt/lampp/htdocs/data.txt')
	print(inputText)
	core.write('/opt/lampp/htdocs/data.txt', '')
	#inputText is split into an array so that we can interact with each line
	#individually (Different URLs are put on different lines by the frontend).
	inputArray = core.split(inputText)
	print(inputArray)

	i = 0
	#This loop allows us to perform the same function
	#on each line of the array. In this case it goes through each line and sorts
	#it into a video url, a playlist url, or random text. And then the
	#appropriate response is carried out
	while i < len(inputArray):
		inputData = inputArray[i]
		print(inputData)

		if 'list=' in inputData:#'list=' is unique to playlist urls
			core.log('playlists', inputData)
		if 'v=' in inputData:#v= is unique to video urls
			downloadQueue.append(inputData)

		i = i + 1

	return downloadQueue

#Runs a loop for every video not in a playlist that needs to be downloaded
def queueDownloads(downloadQueue):
	i = 0
	while i < len(downloadQueue):
		download(downloadQueue[i])
		i = i + 1

	return True

def download(videoURL):#Download takes a video url and downloads the video
	cmd = 'cd Downloads \n youtube-dl -i ' + videoURL
	txt = "cmd = " + cmd
	log(txt)
	os.system(cmd)

	return True

#Checks what playlists are being watched/should have new videos downloaded from
#then begins the playlist download process
def playlistCheck():
	playlists = core.split(core.read('playlists'))

	i = 0
	while i < len(playlists):
		if len(playlists[0]) > 2:
			core.write(playlists[i].split('list=')[1], '')
			playlist(playlists[i])
		i = i + 1

	return

def playlist(playlistURL):#Does all the playlist stuff

	#Scrapes the URL page and gets the video ids/urls
	videoIDs = scrape(playlistURL)
	print(videoIDs)

	#converts playlist url into id for database
	playlistID = playlistURL.split('list=')[1]

	#Checks what videos in playlist have already been downloaded
	unwatchedVideoIDs = watchedCheck(playlistID, videoIDs)

	i = 0
	#Each iteration of the loop downloads a unwatched video in the playlist
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

#Checks what videos in the playlist have already been downloaded (watched).
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

#Log was made for logging variables and marking points in the code for bugfixing
#It is almost unused in the final version
def log(text):
	w = open('log', 'a')
	
	w.write(text + "\n")

	w.close

	return True

main()
