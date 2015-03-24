# -*- coding: utf-8 -*-
"""
nba_scraper.py
Author: Gordon Nickerson
scrapes perGame team stats of NBA teams
"""

#toDo
# - Refactor to move Player and Team classes to nba_stats

import requests
import bs4

root_url = 'http://www.basketball-reference.com'

class Player:
    def __init__(self,stats):
        self.jersey_number = ''
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
        self.players = []
        self.team_url = str(team_url)
        self.division = str(division)
        self.conference = str(conference)

    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name       

    def scrape_team_stats(self):
        """scrapes a list of players from each team, creating Player object with scraped stats for each"""
        response = requests.get(root_url + self.team_url)
        soup = bs4.BeautifulSoup(response.content)
        roster = soup.find(id='per_game').tbody

        for player_number in range(1,len(roster),2):
            playerStatTable = roster.contents[player_number].contents
            perGameStats = []
            for stat in range(1,len(playerStatTable),2):
                perGameStats.append(playerStatTable[stat].string)
            self.players.append(Player(perGameStats))

#Unnecessary, but I want to keep as an example code  
#    def get_team_roster(self):
#        """populates a team roster, with player's URLs"""
#
#        response = requests.get(self.team_url)
#        soup = bs4.BeautifulSoup(response.content)
#        roster = soup.find(id='all_roster').tbody
#        
#        for player_number in range(1,len(roster),2):
#            player = roster.contents[player_number]
#            jersey_number = player.contents[1].string
#            name = player.contents[3].string
#            url = player.contents[3].next_element['href']
#            self.players.append(Player(jersey_number,name,url))


def scrape_teams():
    """scrapes a list of NBA teams, creating a Team object for each"""
    teams = []

    response = requests.get('http://www.basketball-reference.com/leagues/NBA_2015.html')
    soup = bs4.BeautifulSoup(response.content)
    team_soup = soup.find(id='all_standings').find(class_="valign_top")

    eastern_conference_soup = team_soup.tbody.contents
    for index in range(3,len(eastern_conference_soup),2): 
        if index > 11 and index < 15:
            pass
        elif index > 23 and index < 27:
            pass
        elif index > 35:
            pass
        else:
            if index <= 11:
                division =  'Atlantic'
            elif index > 12 and index <= 23:
                division = 'Central'
            elif index > 24 and index <35:
                division = 'Southeast'
            name = eastern_conference_soup[index].td.a.string               
            team_url = eastern_conference_soup[index].td.a['href']
            teams.append(Team(str(name),team_url,division,'Eastern'))


    western_conference_soup = team_soup.contents[3].tbody.contents
    for index in range(3,len(western_conference_soup),2):
        if index > 11 and index < 15:
            pass
        elif index > 23 and index < 27:
            pass
        elif index > 35:
            pass
        else:
            if index <= 11:
                division =  'Northwest'
            elif index > 12 and index <= 23:
                division = 'Pacific'
            elif index > 24 and index <35:
                division = 'Southwest'
            name = western_conference_soup[index].td.a.string               
            team_url = western_conference_soup[index].td.a['href']
            teams.append(Team(str(name),team_url,division,'Western'))

    return teams


def scrape_stat_template():
    """creates a template list of PerGame stat categories"""
    response = requests.get("http://www.basketball-reference.com/teams/POR/2015.html")
    soup = bs4.BeautifulSoup(response.content)
    categories = soup.find(id='per_game').thead.tr.contents

    stat_categories = []

    for index in range(1,len(categories),2):
        stat_categories.append(categories[index].string)
    return stat_categories

statTemplate = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']


if __name__ == '__main__':
    """uncomment below block to build list of teams/players/stats"""

    """
    teams = scrape_teams()
    for team in teams():
        team.scrape_team_stats()
    """




