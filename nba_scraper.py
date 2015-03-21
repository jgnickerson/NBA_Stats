# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 23:46:31 2014

@author: Gordon Nickerson

NBA Stats Scraper
Features to Add:
Sorting methods to list best player on each team (given certain criteria)

"""

import requests
import bs4

root_url = 'http://www.basketball-reference.com'
"""response = requests.get('http://www.basketball-reference.com/players/a/aldrila01.html')
soup = bs4.BeautifulSoup(response.text)"""



def createStatTemplate():
    """creates a template dictionary of PerGame stat categories"""
    response = requests.get("http://www.basketball-reference.com/teams/POR/2015.html")
    soup = bs4.BeautifulSoup(response.content)
    categories = soup.find(id='per_game').thead.tr.contents

    stat_categories = []

    for index in range(1,len(categories),2):
        stat_categories.append(categories[index].string)
    print(stat_categories)

statTemplate = ['Rk', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
#created with below method, relevant for perGame stats only

class Player:
    def __init__(self,jersey_number,name,url,stats):
        self.jersey_number = str(jersey_number)
        self.name = stats[1]
        self.url = 'http://www.basketball-reference.com' + str(url)
        self.stats = stats
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def find_player_stats(self):
        """populates a dictionary with a player's stats per game from the 2014-2015 season"""
        response = requests.get(root_url+self.url)
        soup = bs4.BeautifulSoup(response.content)
    
        stat_categories = []
        find_stat_categories = soup.find(id='all_per_game').tr.contents
        for index in range(1,len(find_stat_categories),2):
            stat_categories.append(find_stat_categories[index].string)

        stat_numbers = []
        find_stat_numbers = soup.find(id='per_game.2015').contents
        for index in range(1,len(find_stat_numbers),2):
            stat_numbers.append(find_stat_numbers[index].string)
        
        for index in range(len(stat_categories)):
            self.stats[stat_categories[index]] = stat_numbers[index]
        
class Team:

    def __init__(self,name,team_url,division,conference):
        self.name = str(name)
        self.players = []
        self.team_url = 'http://www.basketball-reference.com' + str(team_url)
        self.division = str(division)
        self.conference = str(conference)
        

    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name       

    def getTeamStats(self):
        """populates a team roster, with all player stats"""
        response = requests.get(self.team_url)
        soup = bs4.BeautifulSoup(response.content)
        roster = soup.find(id='per_game').tbody

        for player_number in range(1,len(roster),2):
            playerStatTable = roster.contents[player_number].contents
            perGameStats = []
            for stat in range(1,len(playerStatTable),2):
                perGameStats.append(playerStatTable[stat].string)
            self.players.append(Player('blah','blah','blah',perGameStats))

    def get_team_roster(self):
        """populates a team roster, with player's URLs"""

        response = requests.get(self.team_url)
        soup = bs4.BeautifulSoup(response.content)
        roster = soup.find(id='all_roster').tbody
        
        for player_number in range(1,len(roster),2):
            player = roster.contents[player_number]
            jersey_number = player.contents[1].string
            name = player.contents[3].string
            url = player.contents[3].next_element['href']
            self.players.append(Player(jersey_number,name,url))




#should change this to not be it's own class, rather just a standalone method which creates a list. 
# unnecessary if I'm only going to have one season
class Season:
    """a list of all NBA Teams in a given season"""
    def __init__(self,season_url):
        self.teams = []
        self.season_url = str(season_url)
        self.get_teams(self.season_url)

    def __str__(self):
        return str(self.teams)

    def __repr__(self):
        return str(self.teams)

    def get_teams(self,season_url):
        response = requests.get(season_url)
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
                self.teams.append(Team(str(name),team_url,division,'Eastern'))


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
                self.teams.append(Team(str(name),team_url,division,'Western'))


if __name__ == '__main__':
    

    a = Season('http://www.basketball-reference.com/leagues/NBA_2015.html')
    a.get_teams
    a.teams[15].getTeamStats()
    print(a.teams[15].players[0].stats)
    
    #a.teams[15].getTeamStats()

    """populates all team rosters"""
    
    #for index in range(0,len(a.teams)):
    #    a.teams[index].get_team_roster()
    """prints out information about each team"""
    #for team in a.teams:
     #   print(team.name)
      #  print(team.division)
       # for player in team.players:
        #    print(player)
        #print('')
    



