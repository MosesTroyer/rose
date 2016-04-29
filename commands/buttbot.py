import rose as bot
import random

def get_config():
    config = {}
    config["man"] = "Transform the World with Butt"
    config["postprocess"] = True
    config["activated"] = False

    return config

def postprocess(command, config, bot_config):

    if not config["activated"]:
        return

    words = command["message"].split(" ")
    sentence = ""

    if len(words) < 2:
        return

    try:
        if command["user"] == bot_config["user"]: 
            return
    except KeyError:
        pass

    for i in range(0, len(words)):
        if random.random() < .30:
            words[i] = "butt"
            #print words

    sentence = " ".join(words)
    #print sentence
    if sentence != command["message"]:
        bot.say(command["host"], command["channel"], sentence)

def buttbot(command, config, bot_config):
    config["activated"] = not config["activated"]
    
    if(config["activated"]):
        bot.send(command["host"], "NICK buttbot")
    else:
        bot.send(command["host"], "NICK rose")

