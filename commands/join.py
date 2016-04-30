import rose as bot

def get_config():
    config = {}
    config["man"] = "Join the given Channel"

    return config

def join(command, config, bot_config):
    if len(command["options"]["args"]) > 0:
        bot.join(command["host"], command["options"]["args"][0])
