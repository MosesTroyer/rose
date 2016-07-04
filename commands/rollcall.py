import rose as bot

def get_config():
    config = {}
    config["matches"] = ["roll call", "bot rollcall", "rollcall", "bot roll call"]
    config["postprocess"] = True
    config["man"] = ""

    return config

def rollcall(command, config, bot_config):
    pass

def postprocess(command, config, bot_config):
    if command["message"] in config["matches"]:
        if bot_config["nick"] == "buttbot":
            bot.say(command["host"], command["channel"], "Butt Roll Call")
        else:
            bot.say(command["host"], command["channel"], "What are you playing at?")

