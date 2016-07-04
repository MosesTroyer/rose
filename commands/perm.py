import rose as bot
import json

def get_config():
    config = {}
    config["man"] = "Add or remove levels of permission"

    return config

def error(command):
    bot.say(command["host"], command["channel"], "Invalid use. Example: '!perm add whitelist rose'")

def not_auth(command):
    bot.say(command["host"], command["channel"], "Invalid permissions.")

def perm(command, config, bot_config):
    args = command["options"]["args"]    

    if len(args) != 3:
        error(command)
        return
       
    if args[0] not in ["whitelist", "admin", "blacklist"]:
        error(command)
        return

    if args[1] not in ["add", "remove"]:
        error(command)
        return

    perms = bot_config["perms"]

    if (args[0] == "whitelist" or args[0] == "blacklist") and command["user"] not in perms["whitelist"] and command["user"] not in perms["admin"]:
        not_auth(command)
        return
    elif args[0] == "admin" and command["user"] not in perms["admin"]:
        not_auth(command)
        return
 
    if args[1] == "add" and args[2] not in perms[args[0]]:
        perms[args[0]].append(args[2])
    elif args[1] == "remove" and args[2] in perms[args[0]]:
        perms[args[0]].remove(args[2])

    with open('perms.json', 'w') as perms_file:    
        json.dump(perms, perms_file)
