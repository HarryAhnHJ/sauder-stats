# from riotwatcher import LolWatcher
import pandas as pd
import requests
import json



class SauderStats():

    def __init__(self):
        
        self.my_api = "RGAPI-98f4fddc-16eb-4ebe-8933-cea5a9138969"
        self.my_region = "NA1"
        self.my_summoner_name = "UBC Sauder"
        self.header = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0",
                            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "https://developer.riotgames.com",
                            "X-Riot-Token": "RGAPI-98f4fddc-16eb-4ebe-8933-cea5a9138969"
                        }

    def get_summoner_data(self):
        summoner_data = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + self.my_summoner_name,headers=self.header)
        summoner_data_json = summoner_data.json()
        print(summoner_data.text)
        print('Name: ' + summoner_data_json['name'] + '\n' + 
              'Level: ' + str(summoner_data_json['summonerLevel']))
        



if __name__ == "__main__":
    s = SauderStats()
    s.get_summoner_data()
    
