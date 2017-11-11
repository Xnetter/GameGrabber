import requests
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from Game import *
import json
from MetaCritic import *


_gameDatabaseApi = "http://thegamesdb.net/api/"


userKey = "e00cb1ea9f34503dd51ce54daa14b295"
IGDBBaseUrl = "https://api-2445582011268.apicast.io/games/"
IGDBApi= "https://api-2445582011268.apicast.io/"


def IGDBSearch(gameName):
	r = requests.get("https://api-2445582011268.apicast.io/games/?search={game}&fields=name,total_rating".format(game = gameName), headers = {"user-key":"e00cb1ea9f34503dd51ce54daa14b295","Accept":"application/json"})
	siteSoup = BeautifulSoup(r.text, "html.parser")
	siteSoup.prettify()

def getIGDBId(gameName):
	url = IGDBBaseUrl + "?search={game}&fields=id".format(game = gameName)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	id = jObj[0]["id"]
	return id

def getIGDBTrailer(gameID):
	url = IGDBBaseUrl + "{id}?fields=videos".format(id = gameID)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	youSlug = jObj[0]
	try:
		return "https://www.youtube.com/watch?v=" + youSlug["videos"][0]["video_id"]
	except KeyError:
		return "No Trailers Found" 
		
def getGameModes(gameID):
	url = IGDBBaseUrl + "{id}?fields=game_modes".format(id = gameID)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	gameDict = jObj[0]
	try:
		gameModeIds = gameDict["game_modes"] #retrieves the game modes IDS
		gameModes = [] 
		for int in gameModeIds:
			url = IGDBApi + "game_modes/{int}?fields=name".format(int = int)
			modeSoup = igdbAPICaller(url)
			modeObj = json.loads(modeSoup.text)
			gameModes.append(modeObj[0]["name"])
		return gameModes
	except KeyError:
		# print("No Game Modes Available.")
		gamemodes = [] 
		return gamemodes

def getAggregatedRating(gameID):
	url = IGDBBaseUrl + "{id}?fields=aggregated_rating".format(id = gameID)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	try:
		rating = jObj[0]["aggregated_rating"]
		return rating
	except KeyError:
		return "Not Enough Critic Review Data Available for this Title."

def getTimeToBeat(gameID):
	url = IGDBBaseUrl + "{id}?fields=time_to_beat".format(id = gameID)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	speeds = []
	try:
		time = jObj[0]["time_to_beat"]
		for entry in time:
			time[entry] = float("{0:.2f}".format(time[entry]/60.0/60.0))
	except KeyError:
		# print("No Time To Beat Available.")
		return("No Time To Beat Available.")

def getIGDBSummary(gameID):
	url = IGDBBaseUrl + "{id}?fields=summary".format(id = gameID)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	try:
		summary = jObj[0]["summary"]
		# print(summary)
		return summary
	except KeyError:
		return "No Summary Available."
		# print("No summary available.")
		
def getIGDBStoryline(gameID):
	url = IGDBBaseUrl + "{id}?fields=storyline".format(id = gameID)
	soup = igdbAPICaller(url)
	jObj = json.loads(soup.text)
	try:
		summary = jObj[0]["storyline"]
		# print(summary)
		return summary
	except KeyError:
		return "No story line available."
	
		
def getNumberOfReviews(gameID):
	url = IGDBBaseUrl + "{id}?fields=aggregated_rating_count".format(id = gameID)
	soup = igdbAPICaller(url)
	# print(soup)
	jObj = json.loads(soup.text)
	try:
		ratingNumber = jObj[0]["aggregated_rating_count"]
		# print(ratingNumber)
		return str(ratingNumber)
	except KeyError:
		return "0"
	
def getGame(searchToken):
	url = apiCaller("GetGamesList", searchToken)
	r = requests.get(url)
	chartSoup = BeautifulSoup(r.text, "lxml")
	listings = chartSoup.findAll("gametitle", limit = 2)
	return listings[0].text

def listAll(searchToken):
	url = apiCaller("GetGamesList", searchToken)
	r = requests.get(url) 
	root = BeautifulSoup(r.text, "lxml")
	root.prettify()
	print(root)

def getGameList(searchToken):
	gameList = []
	url = apiCaller("GetGamesList", searchToken)
	r = requests.get(url)
	
	root = BeautifulSoup(r.text, "lxml")
	for child in root.findAll("gametitle"):
		if child.text not in gameList:
			gameList.append(child.text)
	return gameList

def getReviewsAndRating(gameName, platforms):
	siteRequest = MetaCritic(gameName, platforms)
	return siteRequest.pullRevRat()
	
	
def getGameID(root):
	id = root.findAll("id", limit = 1)
	if(len(id) > 0):
		return int(id[0].text)
	else:
		return None
def getGameGenre(root): #Modify this to return a list of all genres under game name
	stringItems = [item.text for item in root.findAll("genre")]
	genres = []
	for item in stringItems:
		if item not in genres:
			genres.append(item)
	return genres
	
def getGameOverview(root):
	overview = root.findAll("overview", limit = 1)
	return overview[0].text

def getESRB(root): 
	esrb = root.findAll("esrb", limit = 1)
	return esrb[0].text

def getCoop(root):
	coop = root.findAll("co-op", limit = 1)
	return coop[0].text

def getPublisher(root):
	publisher = root.findAll("publisher", limit = 1)
	return publisher[0].text
	
def getDeveloper(root):
	developer = root.findAll("developer", limit = 1)
	return developer[0].text
	
def printGameInfo(root):
	root.prettify()
	print(root)

		

def getGamePlatAndRelease(root):
	platforms = [term.text for term in root.findAll("platform")]
	releases = [term.text for term in root.findAll("releasedate")]
	formattedReleases = []
	for date in releases:
		formattedReleases.append(datetime.strptime(date, "%m/%d/%Y"))
	return dict(zip(platforms, formattedReleases))

def getAlternativeTitles(root):
	altTitles = root.findAll("title")
	altTitles = [term.text for term in altTitles]
	return altTitles

def contactServer(exactName):
	url = apiCaller("GetGame", exactName, True)
	r = requests.get(url)
	return BeautifulSoup(r.text, "lxml")
	
def apiCaller(functionName, searchToken=None, exact=False):
	if(not exact):
		return _gameDatabaseApi + functionName + ".php?name=" + searchToken
	else:
		return _gameDatabaseApi + functionName + ".php?exactname=" + searchToken

def igdbAPICaller(url):
	headers = {"user-key" : userKey, "Accept":"application/json"}
	r = requests.get(url, headers=headers)
	siteSoup = BeautifulSoup(r.text, "html.parser")
	siteSoup.prettify()
	return siteSoup
	
def openGameWebChart(searchName):
	url = "http://www.vgchartz.com/gamedb/?name={game}".format(game = searchName)
	r = requests.get(url)
	chartSoup = BeautifulSoup(r.text, "html.parser")
	listings = chartSoup.findAll('td')
	#limit = len(searchName) #instantiated a limit to keep results under 
	entries = 0                               #unnecessary numbers but didn't use it.
	dataList = []                            
	count = 0
	salesData = []
	for i in range(len(listings)):
		if(i < count):
			salesData.append(listings[i].text)
		if(i == count and count > 0):
			dataList.append(salesData)
			salesData = []
		if(listings[i].text == searchName):
			count = i + 10
			entries += 1
	# print(dataList)
	return dataList


	
	