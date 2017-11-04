import requests
from ServerContact import *
import time
from datetime import timedelta
from calendar import monthrange
from parseJSON import *


"""Creates a game object based on user input and compiles statistics"""

class find_game():
	def __init__(self, game): #searchToken is the

		
		self.gameName = game
		#listAll(self.getGameName())
		self.root = contactServer(self.gameName)
		#printGameInfo(self.getRoot())
		#initialize request
		self.igdbID = getIGDBId(self.getGameName())
		self.id = getGameID(self.getRoot())
		self.platReleaseTable = getGamePlatAndRelease(self.getRoot())
		self.genre = getGameGenre(self.getRoot())
		self.setInitialReleaseDate()
		self.summary = getGameOverview(self.getRoot())
		self.alternativeTitles = getAlternativeTitles(self.getRoot())
		self.parseSalesData(openGameWebChart(self.getGameName()))
		self.esrb = getESRB(self.getRoot())
		self.coop = getCoop(self.getRoot())
		self.trailer = getIGDBTrailer(self.getIGDBId()) #new
		self.publisher = getPublisher(self.getRoot())
		self.developer = getDeveloper(self.getRoot())
		self.gameModes = getGameModes(self.getIGDBId()) #new, a list
		self.aggregatedRating = str(getAggregatedRating(self.getIGDBId())) + ": based on " + getNumberOfReviews(self.getIGDBId()) + " professional reviews." #new
		print(self.aggregatedRating)
		self.timeToBeat = getTimeToBeat(self.getIGDBId())
		self.IGDBSummary = getIGDBSummary(self.getIGDBId())
		self.IGDBStoryline = getIGDBStoryline(self.getIGDBId())
		self.metaRating = getReviewsAndRating(self.getGameName(), self.getPlatformList())
		print(self.metaRating)
		self.rundown()
		
	def setInitialReleaseDate(self):
		dist = 0
		earliest = datetime.now()
		for date in self.getReleaseTable().values():
			if (earliest > date):
				earliest = date
		self.releaseDate = earliest
	
	def getPlatforms(self):
		return self.platforms
	
	def retrievePublisher(self):
		return self.publisher
	
	def retrieveDeveloper(self):
		return self.developer
	
	def retrieveCoop(self):
		return self.coop
	
	def retrieveTrailer(self):
		return self.trailer
		
	def retrieveESRB(self):
		return self.esrb
	
	def getPlatformList(self):
		return list(self.getReleaseTable().keys())
	
	def getGameName(self):
		return self.gameName
	
	def getIGDBId(self):
		return self.igdbID
			
	def getGameDataBaseID(self):
		return self.id
	
	def getInitialRelease(self):
		return self.releaseDate
		
	def getRoot(self):
		return self.root
	
	def getReleaseDates(self):
		return self.releaseDates
	
	def printReleaseTable(self):
		for item in self.platReleaseTable:
			print("{platform} - {release}".format(platform = item, release = self.platReleaseTable[item]))
	\
	def getReleaseTable(self):
		return self.platReleaseTable
		
	def rundown(self):
		print(" -- {game} -- \n".format(game = self.getGameName()))
		print("Platforms and Release Dates: ")
		print("-----------------------------------------")
		for item in self.getReleaseTable():
			print("{platform:40}{release}".format(platform = item, release =self.getReleaseTable()[item].strftime("%B %d, %Y")))
		print("-----------------------------------------")
		print("Initial Release Date: {relDate}".format(relDate = self.getInitialRelease().strftime("%B %d, %Y")))
		print("Age: {age} years".format(age = self.getAge()))
		print("-----------------------------------------")
		print("Trailer: {trailer}".format(trailer = self.retrieveTrailer()))
		print("-----------------------------------------")
		print("ESRB: {esrb}".format(esrb = self.retrieveESRB()))
		print("-----------------------------------------")
		print("Publisher: {pub}".format(pub = self.retrievePublisher()))
		print("Developer: {dev}".format(dev = self.retrieveDeveloper()))
		print("-----------------------------------------")
		print("Genres: ")
		for genre in self.getGenre():
			print("{genre:15}".format(genre = genre))
		print("------------------------------------------")
		print("Co-Op Enabled: {coop}".format(coop = self.retrieveCoop()))
		print("Overview:")
		print("-----------------------------------------")
		print("{ov:5}".format(ov=self.getOverview()))
		print("-----------------------------------------")
		if(self.getTotalSales() != 0):
			print("Total Sales: {sales: <40}".format(sales = format((self.getTotalSales()), ",d")))
			print("-----------------------------------------")
			print("Sales by Platform: ")
			for item in self.getSalesByPlatform():
				print("{platform:40}{sales} copies".format(platform = item, sales = format(self.getSalesByPlatform()[item], ",d")))
			print("-----------------------------------------")
			print("Sales by Country: ")
			print("{:<40}".format("America:") + "{sales} copies".format(sales = format(self.america, ",d")))
			print("{:<40}".format("Europe:") + "{sales} copies".format(sales = format(self.europe, ",d")))
			print("{:<40}".format("Japan:") + "{sales} copies".format(sales = format(self.japan, ",d")))
			print("{:<40}".format("Rest of the World:") + "{sales} copies".format(sales = format(self.rest, ",d")))
			print("-----------------------------------------")
			print("{:<30}".format("Average Sales per Week:") + "{sales: <40}".format(sales = format(self.getSalesPerWeek(), ",d")))
			print("{:<30}".format("Average Sales per Month:") + "{sales: <40}".format(sales = format(self.getSalesPerMonth(), ",d")))
		else:
			print("No Sales Data Available.")
		
	
	def getGenre(self):
		return self.genre
	
	def getOverview(self):
		return self.summary
	
	def getAge(self):
		today = datetime.now()
		born = self.getInitialRelease()
		return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
	
	def getSalesPerWeek(self):
		today = datetime.now()
		born = self.getInitialRelease()
		monday1 = (born - timedelta(days=born.weekday()))
		monday2 = (today - timedelta(days=today.weekday()))
		
		return int(float(self.getTotalSales())/(monday2 - monday1).days/7)
	def getSalesPerMonth(self):
		today = datetime.now()
		born = self.getInitialRelease()
		delta = 0
		while True:
			mdays = monthrange(born.year, born.month)[1]
			born += timedelta(days=mdays)
			if born <= today:
				delta += 1
			else:
				break
		return int(float(self.getTotalSales())/float(delta))
		
	def getTotalSales(self):
		return self.totalSales
	
	def getSalesByPlatform(self):
		return self.salesByPlatform
	
	def listStats(self):
		openGameWebChart(self)
	
	def parseSalesData(self, salesList, num = 0):
		salesByPlat = {}
		total = 0
		americanSalesTotal = 0
		europeanSalesTotal = 0
		japaneseSalesTotal = 0
		restSalesTotal = 0
		for list in salesList:
			salesByPlat.update({list[0]: int(float(list[8])*1000000)})
			total += float(list[8])*1000000
			americanSalesTotal += float(list[4])
			europeanSalesTotal += float(list[5])
			japaneseSalesTotal += float(list[6])
			restSalesTotal += float(list[7])
		self.salesByPlatform = salesByPlat
		self.totalSales = int(total)
		self.america = int(americanSalesTotal*1000000)
		self.europe = int(europeanSalesTotal*1000000)
		self.japan = int(japaneseSalesTotal*1000000)
		self.rest = int(restSalesTotal*1000000)
		if(self.totalSales == 0):
			if(num != len(self.alternativeTitles)-1 and len(self.alternativeTitles) != 0):
				self.parseSalesData(openGameWebChart(self.alternativeTitles[num]), num + 1)
			
		
				
		



