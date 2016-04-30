import rose as bot

def get_config():
    config = {}
    config["man"] = "Say the given message"

    return config

def say(command, config, bot_config):
    if len(command["options"]["args"]) > 0:
        bot.say(command["host"], command["channel"], " ".join(command["options"]["args"]))
