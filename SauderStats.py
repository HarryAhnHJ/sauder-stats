
import pandas as pd
import requests
import json
import codecs
import numpy
from matplotlib import pyplot as plt


class SauderStats(str):

    def __init__(self, summoner_name: str):
        api_dev = ""
        api_prod = ""
        with open("api.txt") as api:
            lines = api.readlines()
        
            api_dev = lines[0].replace("\n","")
            api_prod = lines[1]

        #variables used for requests
        self.my_api = api_dev
        self.my_region = "NA1"
        self.my_summoner_name = summoner_name
        self.my_puuid = ""
        self.my_summid = ""
        
        #required header for url request, change API key until app is approved
        self.header = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0",
                            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "https://developer.riotgames.com",
                            "X-Riot-Token": api_dev
                        }

        self.platform_url = "https://na1.api.riotgames.com"
        self.region_url = "https://americas.api.riotgames.com"

    def get_summoner_data(self):
        summoner_data = requests.get(self.platform_url + '/lol/summoner/v4/summoners/by-name/' + self.my_summoner_name,headers=self.header)
        summoner_data_json = summoner_data.json()
        self.my_puuid = summoner_data_json['puuid']
        self.my_summid = summoner_data_json['id']

        rank_data = requests.get(self.platform_url + '/lol/league/v4/entries/by-summoner/' + self.my_summid, headers=self.header)
        rank_data_json = rank_data.json()
        print(rank_data_json)
        #basic info
        print('Name: ' + summoner_data_json['name'] + '\n' + 
              'Level: ' + str(summoner_data_json['summonerLevel']) + '\n' + 
              'Rank: ' +  rank_data_json[0]['tier'] + ' ' + rank_data_json[0]['rank']
              )

        
    def get_match_data(self,role: str,num_games: int):
        #filter for ranked, queueid=420 = soloq
        x=0
        past_matches = requests.get(self.region_url + '/lol/match/v5/matches/by-puuid/' + self.my_puuid + '/ids' + '?queue=420&start=' + str(x) + '&count=' + str(num_games),headers=self.header)
        past_matches_json = past_matches.json()

        #this is a list of data dto of games where the player is playing their main role in solo queue
        solo_queue_match_stats= []

        y=1
        for match in past_matches_json:
            
            print(match)
            match_data = requests.get(self.region_url + '/lol/match/v5/matches/' + match, headers=self.header)
            match_data_json = match_data.json()

            match_info = match_data_json['info']

            #already filtered out soloq from matches by puuid
            # match_type = match_info['queueId']

            # need to find stats for 1 player out of 10, find summoner name in loop
            my_part_index = 0
            participants = match_info['participants']
            index = 0
            for part in participants:
                if part['summonerName'] == self.my_summoner_name:
                    my_part_index = index
                index = index+1

            #finding out the role of player
            my_role_in_match = participants[my_part_index]['teamPosition']

            #filtering out matches where the player was not playing their main role
            if  my_role_in_match == role:
                print("This game was solo queue, and the role of " + self.my_summoner_name + " was " + role)
                solo_queue_match_stats.append(participants[my_part_index])

            print("match" + str(y))
            y=y+1
            
        #collecting data from matches where player is playing their main role

        print("now analyzing in-game stats where " + self.my_summoner_name + " played " + role)
        num_matches = len(solo_queue_match_stats)
        print("analyzing " + str(num_matches) + " games:")
        champs = []

        for match_stat in solo_queue_match_stats:

            # match_data = requests.get(self.region_url + '/lol/match/v5/matches/' + match, headers=self.header)
            # match_timeline = requests.get(self.region_url + '/lol/match/v5/matches/' + match + '/timeline', headers=self.header)
            # match_data_json = match_data.json()
            # match_stats = match_data_json['info']['participants']
            champs.append(match_stat['championName'])
        
        champs.sort(reverse=True)
        plt.hist(champs)
        plt.show()

        


if __name__ == "__main__":
    player = ["", ""]
    s = SauderStats(player[0])
    s.get_summoner_data()
    s.get_match_data(player[1],20)
    
