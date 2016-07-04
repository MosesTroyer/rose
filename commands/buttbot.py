import rose as bot
import random, re

def get_config():
    config = {}
    config["man"] = "Transform the World with Butt"
    config["postprocess"] = True
    config["activated"] = False
    config["replace"] = "butt"
    config["chance"] = .30
    config["alt_nick"] = "buttbot"
    config["nick"] = ""

    return config

def postprocess(command, config, bot_config):

    if not config["activated"]:
        return

    try:
        if command["user"] == bot_config["user"]: 
            return
    except KeyError:
        pass

    words = command["message"].split(' ')
    sentence = ""

    if len(words) < 3:
        return
    
    for i in range(0, len(words)):
        if random.random() < config["chance"]:
            word = re.findall(r"[\w']+|[.,!?;]", words[i])
            if len(word) > 0:
                if word[0].isupper():
                    word[0] = config["replace"].upper()
                else:
                    word[0] = config["replace"]
                words[i] = "".join(word)

    sentence = " ".join(words)
    if sentence != command["message"]:
        bot.say(command["host"], command["channel"], sentence)

def buttbot(command, config, bot_config):
    if command["user"] not in config["perms"]["admin"]:
        return #manually done here because postprocess should be for everyone    

    config["activated"] = not config["activated"]
    
    if(config["activated"]):
        #TODO doesn't check for errors
        config["nick"] = bot_config["nick"]
        bot_config["nick"] = config["alt_nick"]
        bot.send(command["host"], "NICK " + config["alt_nick"])
    else:
        bot_config["nick"] = config["nick"]
        bot.send(command["host"], "NICK " + bot_config["nick"])

