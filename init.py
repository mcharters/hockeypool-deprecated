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
		'name': teamData[0].a.get_text(),
		'gamesPlayed': teamData[2].get_text(),
		'goals': teamData[4].get_text(),
		'assists': teamData[6].get_text(),
		'wins': teamData[28].get_text(),
		'losses': teamData[30].get_text(),
		'otLosses': teamData[34].get_text()
	}
	
	# insert team in the db, record the id for later use
	team_id = teams.insert(team)
	teamDict[teamData[0].a['href']] = team_id
	
	print 'Inserted team {0} with ID {1}'.format(team['name'], team_id)

# parse defenders
playersURL = "http://sports.yahoo.com/nhl/stats/byposition?pos=D&conference=NHL&year=season_2012&qualified=1"
soup = BeautifulSoup(urlopen(playersURL), "lxml")
headerRow = soup.select(".ysptblthbody1")

for playerRow in headerRow[0].find_next_siblings("tr"):
	playerData = playerRow.find_all("td")
	
	player = {
		'name': playerData[0].a.get_text(),
		'team': teamDict[playerData[1].a['href']], # this is the team's id in the db, not the team's name
		'gamesPlayed': playerData[2].get_text(),
		'goals': playerData[4].get_text(),
		'assists': playerData[6].get_text(),
		'points': playerData[8].get_text(),
		'plusMinus': playerData[10].get_text(),
		'penaltyMinutes': playerData[12].get_text(),
		'hits': playerData[14].get_text(),
		'bks': playerData[16].get_text(),
		'fw': playerData[18].get_text(),
		'fl': playerData[20].get_text(),
		'fo': playerData[22].get_text(),
		'ppg': playerData[24].get_text(),
		'ppa': playerData[26].get_text(),
		'shg': playerData[28].get_text(),
		'sha': playerData[30].get_text(),
		'gw': playerData[32].get_text(),
		'sog': playerData[34].get_text(),
		'pct': playerData[36].get_text(),
		'isDefender': True
	}
	
	player_id = players.insert(player)
	
	print 'Inserted player {0} with ID {1}'.format(player['name'], player_id)

# parse forwards
playersURL = "http://sports.yahoo.com/nhl/stats/byposition?pos=C,RW,LW&conference=NHL&year=season_2012&qualified=1"
soup = BeautifulSoup(urlopen(playersURL), "lxml")
headerRow = soup.select(".ysptblthbody1")

for playerRow in headerRow[0].find_next_siblings("tr"):
	playerData = playerRow.find_all("td")
	
	player = {
		'name': playerData[0].a.get_text(),
		'team': teamDict[playerData[1].a['href']], # this is the team's id in the db, not the team's name
		'gamesPlayed': playerData[2].get_text(),
		'goals': playerData[4].get_text(),
		'assists': playerData[6].get_text(),
		'points': playerData[8].get_text(),
		'plusMinus': playerData[10].get_text(),
		'penaltyMinutes': playerData[12].get_text(),
		'hits': playerData[14].get_text(),
		'bks': playerData[16].get_text(),
		'fw': playerData[18].get_text(),
		'fl': playerData[20].get_text(),
		'fo': playerData[22].get_text(),
		'ppg': playerData[24].get_text(),
		'ppa': playerData[26].get_text(),
		'shg': playerData[28].get_text(),
		'sha': playerData[30].get_text(),
		'gw': playerData[32].get_text(),
		'sog': playerData[34].get_text(),
		'pct': playerData[36].get_text(),
		'isDefender': False
	}
	
	player_id = players.insert(player)
	
	print 'Inserted player {0} with ID {1}'.format(player['name'], player_id)
