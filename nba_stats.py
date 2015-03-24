"""
nba_stats.py
Author: Gordon Nickerson
sorting and comparison for stats stored in pergame.db
"""

import nba_scraper as scraper
import nba_scraper_db as db

class Player:
    def __init__(self,stats):
        self.name = stats[1]
        self.stats = stats

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Team:
    def __init__(self,name,team_url,division,conference):
        self.name = str(name)
        self.underscored_name = self.name.replace(" ","_")
        self.team_url = str(team_url)
        self.division = str(division)
        self.conference = str(conference)
        self.players = []

    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name  


def rebuild_Team_Player_tree():
    teams = db.retrieve_teams_table()
    teamPlayerTree = []
    for team in teams:
        teamPlayerTree.append(Team(team[1],team[4],team[3],team[2]))

    perGameStats = db.retrieve_and_assemble_team_perGame()
    for teamIndex in range(len(perGameStats)):
        players = perGameStats[teamIndex]
        for playerIndex in range(len(players)):
            teamPlayerTree[teamIndex].players.append(Player(players[playerIndex]))
    return teamPlayerTree


statTemplate = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

teamPlayerTree = rebuild_Team_Player_tree()

print(teamPlayerTree[15].players[0].stats)

