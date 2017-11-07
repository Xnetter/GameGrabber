import requests
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import json

class MetaCritic():
	def __init__(self, exactName, platforms):
		urls = []
		self.platforms = platforms
		self.toMetaPlatforms = self.generateMetaPlatformTags()
		for platform in self.getMetacriticPlatforms():
			urls.append("http://www.metacritic.com/game/" + platform + "/" + exactName.lower().replace(":", "").replace(" ", "-"))
			#test the url here before adding it to the list to make sure it exists.
		self.urlBank = urls #Append every metacritic page for each individual platform, and store them
		
	
	def generateMetaPlatformTags(self):
		nonexistant = ["Commodore 64", "Nintendo Entertainment System (NES)"]
		convertor = {"Sony Playstation 4":"playstation-4",
		"Microsoft Xbox One":"xbox-one",
		"PC":"pc",
		"Nintendo Switch":"switch",
		"Nintendo Wii U": "wii-u",
		"Nintendo 3DS":"3ds",
		"Sony Playstation 3":"playstation-3",
		"Microsoft Xbox 360":"xbox-360",
		"Nintendo DS":"ds",#
		"Sony Playstation Vita":"playstation-vita",
		"Nintendo 64":"nintendo-64",
		"Gameboy Advance":"game-boy-advance",
		"Nintendo 64":"n64"}
		converted = []
		for platform in self.getPlatforms():
			try:
				converted.append(convertor[platform])
			except KeyError:
				#Do nothing
				if platform not in nonexistant:
					print("Error with this platform: " + platform)
				else:
					print("Metacritic does not have entries for the " + platform + " platform.")
		return converted
	
	def getMetacriticPlatforms(self):
		return self.toMetaPlatforms
	
	
	
	def pullRevRat(self): #TODO Clean Up
		overallRate = 0
		count = 0
		platformAndReviews = {}
		for url in self.getUrlBank():
			reviewData = []
			headers = {'User-Agent':'Mozilla/5.0'}
			r = requests.get(url, headers = headers)
			siteSoup = BeautifulSoup(r.text, "html.parser")
			siteSoup.prettify()
			try:
				reviewsList = siteSoup.find("ol", class_="reviews critic_reviews")
				numReviews = reviewsList.findAll("li", class_="review critic_review")
				if len(numReviews) == 0:
					reviews = siteSoup.findAll("li", class_="review critic_review first_review last_review")
				else:
					reviews = siteSoup.findAll("li", class_="review critic_review")
					firstReview = siteSoup.find("li", class_="review critic_review first_review")
					lastReview = siteSoup.find("li", class_="review critic_review last_review")
					reviews.append(firstReview)
					reviews.append(lastReview)
				for item in reviews:
					auth = item.find("a", class_="external").text.strip().replace("\n", "")
					rev = item.find("div", class_="review_body").text.strip().replace("\n", "")
					date = item.find("div", class_="date").text.strip().replace("\n", "")
					score = item.find("div", class_="review_grade").text.strip().replace("\n", "")
					reviewData.append({"author":auth, "review":rev, "date":date, "score":score})
			except AttributeError:
				reviewData.append("None")
			# print("Review Data:")
			# print(reviewData)
			platformAndReviews.update({self.getPlatforms()[count]:reviewData})
			rating = siteSoup.findAll("span", itemprop = "ratingValue")
			for item in rating:
				overallRate += int(item.text)
			count += 1
		if len(self.getUrlBank())>0:
			overallRate = float(overallRate)/len(self.getUrlBank())
		else:
			overallRate = "No Ratings Available"
		platformAndReviews.update({"rating":overallRate})
		return platformAndReviews
	
	def getUrlBank(self):
		return self.urlBank
	
	
	def getPlatforms(self):
		return self.platforms
		
		