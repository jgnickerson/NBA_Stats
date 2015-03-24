"""
nba_scraper_db.py
Author: Gordon Nickerson
creates and accesses the database of NBA team players and their stats
"""

import sqlite3
import nba_scraper

def create_team_perGame_stats_table(teamTableName):
	newTeamTable = "CREATE TABLE IF NOT EXISTS " + str(teamTableName) + " (rank INTEGER, name TEXT, age INTEGER, games INTEGER, gS INTEGER, mP INTEGER, fg INTEGER, fga INTEGER, fgp INTEGER,threeP INTEGER, threePA INTEGER, threePP INTEGER, twoP INTEGER, twoPA INTEGER, twoPP INTEGER, fT INTEGER, fTA INTEGER, fTP INTEGER, oRB INTEGER, dRB INTEGER, tRB INTEGER, aST INTEGER, sTL INTEGER, bLK INTEGER, tOV INTEGER, pF INTEGER, pTs INTEGER)"
	cursor.execute(newTeamTable)
	db.commit()

def insert_into_team_perGame_table(teamTableName, statsToInsert):
	insertIntoTeamTable = "INSERT INTO " + str(teamTableName) + " (rank, name, age, games, gS, mP, fg, fga, fgp, threeP, threePA, threePP, twoP, twoPA, twoPP, fT, fTA, fTP, oRB, dRB, tRB, aST, sTL, bLK, tOV, pF, pTs) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
	cursor.executemany(insertIntoTeamTable, statsToInsert)
	db.commit()

def retrieve_team_perGame_table(teamTableName):
	db = sqlite3.connect('pergame.db')
	cursor = db.cursor()
	cursor.execute("SELECT * FROM " + teamTableName) #rank, name, age, games, gS, mP, fg, fga, fgp, threeP, threePA, threePP, twoP, twoPA, twoPP, fT, fTA, fTP, oRB, dRB, tRB, aST, sTL, bLK, tOV, pF, pTs
	return cursor.fetchall()


def create_teams_table():
	db = sqlite3.connect('teams.db')
	cursor = db.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS teams(team TEXT, name TEXT, conference TEXT, division TEXT, url TEXT)")
	db.commit()

def insert_into_teams_table():
	db = sqlite3.connect('teams.db')
	cursor = db.cursor()

	teams = scrape_teams()
	teamsList = []
	for team in teams:
		teamsList.append((str(team).replace(" ","_"),str(team),team.conference,team.division,team.team_url,))
	cursor.executemany("""INSERT INTO teams(team, name, conference, division, url) VALUES(?,?,?,?,?)""", teamsList)
	db.commit()

def retrieve_teams_table():
	db = sqlite3.connect('teams.db')
	cursor = db.cursor()

	cursor.execute("""SELECT * FROM teams""")
	table = cursor.fetchall()
	teams = []
	for index in range(len(table)):
		teams.append(table[index])
	return teams


def scrape_teams():
	return nba_scraper.scrape_teams()


def scrape_team_data(teams, teamIndex):
	"""creates a list of tuples of player stats to place in db"""
	players = []
	teams[teamIndex].scrapeTeamStats()
	for player in teams[teamIndex].players:
		sql_player_row = tuple(player.stats)
		players.append(sql_player_row)
	return players

def initialize_teams_table():
	"""creates and fills database with team names, which are also the names of each team's stat tables"""
	create_teams_table()
	insert_into_teams_table()


def initialize_and_populate_team_perGame_tables():
	"""creates team tables, scrapes team's perGame player data, and inserts data into team tables"""
	teams = scrape_teams()
	for teamIndex in range(len(teams)):
		team = teams[teamIndex]
		teamName = team.underscored_name
		create_team_perGame_stats_table(teamName)

		players = scrape_team_data(teams,teamIndex)
		insert_into_team_perGame_table(team.underscored_name,players)
		

def retrieve_and_assemble_team_perGame():
	teams = retrieve_teams_table()

	perGameStats = []
	for index in range(len(teams)):
		perGameStats.append(retrieve_team_perGame_table(teams[index][0]))
	return perGameStats


if __name__=='__main__':
	#initialize_teams_table()

	#initialize_and_populate_team_perGame_tables()
	pass
