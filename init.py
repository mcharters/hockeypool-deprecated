from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib2 import urlopen
import pprint

# set up the db
client = MongoClient()
db = client.hockeypool
players = db.players
teams = db.teams

players.remove()
teams.remove()

# set up a team dictionary
teamDict = {}

#parse teams
teamsURL = "http://sports.yahoo.com/nhl/stats/byteam?cat=teamstats"
soup = BeautifulSoup(urlopen(teamsURL), "lxml")
headerRow = soup.select(".ysptblthbody1")

for teamRow in headerRow[0].find_next_siblings("tr"):
	teamData = teamRow.find_all("td")
	
	team = {
		'name': teamData[0].a.get_text()
	}
	
	# insert team in the db, record the id for later use
	team_id = teams.insert(team)
	teamDict[teamData[0].a['href']] = team_id
	
	print 'Inserted team {0} with ID {1}'.format(team['name'], team_id)

# parse players
playersURL = "http://sports.yahoo.com/nhl/stats/byposition?pos=C,RW,LW,D&conference=NHL&year=season_2012&qualified=1"
soup = BeautifulSoup(urlopen(playersURL), "lxml")
headerRow = soup.select(".ysptblthbody1")

for playerRow in headerRow[0].find_next_siblings("tr"):
	playerData = playerRow.find_all("td")
	
	player = {
		'name': playerData[0].a.get_text(),
		'team': teamDict[playerData[1].a['href']], # this is the team's id in the db, not the team's name
		'games_played': playerData[2].get_text(),
		'goals': playerData[4].get_text(),
		'assists': playerData[6].get_text(),
		'points': playerData[8].get_text(),
		'plus_minus': playerData[10].get_text(),
		'picked': False
	}
	
	player_id = players.insert(player)
	
	print 'Inserted player {0} with ID {1}'.format(player['name'], player_id)
