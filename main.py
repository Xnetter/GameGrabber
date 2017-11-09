from Game import *
from ServerContact import *

searchToken = input("Please enter the name of the game you'd like to research: ")
if(searchToken == "exit()"):
	exit()
game = getGame(searchToken)
initialize = input("Data will be compiled on {game}, is this correct? Y/N\n".format(game=game))
if(initialize == 'Y' or initialize == 'y'):
	pass
else:
	print("Here is a list of games with similar titles.")
	#Currently the code only returns the first result of the list.
	#TODO Cycle through the first 3 results then return 'Please try again' after all 3 have failed.
	gameList = getGameList(searchToken)
	count = 0
	for title in gameList:
		print("[{num}] {title}".format(num=count, title=title))
		count+=1
	gameIndex = int(input("Please enter the number of the title you wish to research, or -1 to escape: "))
	if(gameIndex == -1):
		exit()
	game = gameList[gameIndex]
print("Processing {game}\n".format(game = game))

GameResearcher = find_game(game)
#printGameInfo(GameResearcher.getGameName())
#GameResearcher.rundown()
#GameResearcher.listStats()