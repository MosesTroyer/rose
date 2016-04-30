import rose as bot
import json
import requests

def get_config():
    config = {}
    config["man"] = "Get Dota 2 Match details"

    return config

def dota(command, config, bot_config):

    try:
        match = command["options"]["args"][0]
    except IndexError:
        return

    url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key???&match_id=" + match

    response = requests.get(url)

    if(response.ok):

        data = json.loads(response.content)

        data = data["result"]

        radiant_score = [0, 0, 0]
        dire_score = [0, 0, 0]

        for player in data["players"]:
            if player["player_slot"] > 100:
                dire_score[0] += player["kills"]
                dire_score[1] += player["deaths"]
                dire_score[2] += player["assists"]
            else:
                radiant_score[0] += player["kills"]
                radiant_score[1] += player["deaths"]
                radiant_score[2] += player["assists"]

        #say data to channel
        if data["radiant_win"]:
            sentence = "Radiant"
        else:   
            sentence = "Dire" 

        sentence += " victory! "

        sentence += str(radiant_score[0]) + "/" + str(radiant_score[1]) + "/" + str(radiant_score[2]) 
        sentence += " " + str(dire_score[0]) + "/" + str(dire_score[1]) + "/" + str(dire_score[2])

        bot.say(command["host"], command["channel"], sentence)

        
    else:
        myResponse.raise_for_status()    

    pass
