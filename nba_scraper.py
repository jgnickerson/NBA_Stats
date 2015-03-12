# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 23:46:31 2014

@author: jgnickerson

Basketball Stats Scraper
Features to Add:
-Find player URLs, possibly by making team rosters
-Scrape team rosters and populate team dictionaries with the individual player dictionaries
-Comparisons between players

"""

import requests
import bs4

root_url = 'http://www.basketball-reference.com'
response = requests.get('http://www.basketball-reference.com/players/a/aldrila01.html')
soup = bs4.BeautifulSoup(response.text)


class Player:
    def __init__(self,jersey_number,name,url):
        self.jersey_number = str(jersey_number)
        self.name = str(name)
        self.url = str(url)
        self.stats = {}
        
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
    a.teams[15].get_team_roster()
    a.teams[15].players[1].find_player_stats()
    print(a.teams[15].name)
    print(a.teams[15].players[1].stats)



