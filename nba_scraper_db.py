#nba_scraper_db.py
#Author: Jules Nickerson

import sqlite3
import nba_scraper

db = sqlite3.connect('perGameStats')
cursor = db.cursor()

def create_team_perGame_stats_table(teamTableName):
	newTeamTable = "CREATE TABLE IF NOT EXISTS " + str(teamTableName) + " (rank INTEGER, name TEXT, age INTEGER, games INTEGER, gS INTEGER, mP INTEGER, fg INTEGER, fga INTEGER, fgp INTEGER,threeP INTEGER, threePA INTEGER, threePP INTEGER, twoP INTEGER, twoPA INTEGER, twoPP INTEGER, fT INTEGER, fTA INTEGER, fTP INTEGER, oRB INTEGER, dRB INTEGER, tRB INTEGER, aST INTEGER, sTL INTEGER, bLK INTEGER, tOV INTEGER, pF INTEGER, pTs INTEGER)"
	cursor.execute(newTeamTable)

def insert_into_team_perGame_table(teamTableName, statsToInsert):
	insertIntoTeamTable = "INSERT INTO " + str(teamTableName) + " (rank, name, age, games, gS, mP, fg, fga, fgp, threeP, threePA, threePP, twoP, twoPA, twoPP, fT, fTA, fTP, oRB, dRB, tRB, aST, sTL, bLK, tOV, pF, pTs) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
	print(statsToInsert)
	cursor.executemany(insertIntoTeamTable, statsToInsert)
	db.commit()

def retrieve_team_perGame_table(teamTableName):
	cursor.execute("SELECT * FROM " + teamTableName) #rank, name, age, games, gS, mP, fg, fga, fgp, threeP, threePA, threePP, twoP, twoPA, twoPP, fT, fTA, fTP, oRB, dRB, tRB, aST, sTL, bLK, tOV, pF, pTs
	return cursor.fetchall()

def scrape_teams():
	return nba_scraper.get_teams()

def scrape_team_data(teams, teamIndex):
	players = []
	teams[teamIndex].getTeamStats()
	for player in teams[teamIndex].players:
		sql_player_row = tuple(player.stats)
		players.append(sql_player_row)
	return players

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
	
	
if __name__=='__main__':
	
	

