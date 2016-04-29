import rose as bot

def get_config():
    config = {}
    config["man"] = "Set the channel's topic."

    return config

def topic(command, config, bot_config):
    
    if len(command["options"]["args"]) > 0:
        bot.send_channel(command["host"], "TOPIC", command["channel"], " ".join(command["options"]["args"]))

