import socket, logging, os, random

"""
Rosencrantz, the IRC Bot
Moses Troyer 2016
"""

#TODO Load config - may not work because of method implementation
#TODO possible to load different imports, depending on slack vs irc?
#TODO for example, import slack / import irc for these global methods and overhead methods
#TODO use YASP.co for dota sheit + ?json=1
#TODO trigger on certain words

SERVER = "localhost"
PORT = 6667
NICK = "rose"
USER = NICK
CHAN = "#moses"

PREFIX = "!"

COMMANDS = {}
COMMANDS_CONFIG = {}
COMMANDS_POSTPROCESS = {}

##### GLOBAL METHODS #####

def send(host, message):
    host.send("{}\r\n".format(message).encode('utf-8'))
    log(message)

def sendSilent(host, message): #sends that don't need logging
    IRC.send("{}\r\n".format(message).encode('utf-8')) 

def say(host, channel, message):
    send(host, "PRIVMSG " + channel + " :" + message)

def send_channel(host, command, channel, message):
    send(host, command + " " + channel + " :" + message)

def join(host, channel):
    send(host, "JOIN " + channel)

def log(message):
    print message
    logging.info(message)

def get_config():
    #TODO: Make into a real setting config object dealio
    config = {}
    config["server"] = SERVER
    config["port"] = PORT
    config["nick"] = NICK
    config["chan"] = CHAN
    config["prefix"] = PREFIX

    return config

##### OVERHEAD METHODS #####

def connect():
    log("Connecting...")

    IRC.connect((SERVER, PORT))

    send(IRC, "NICK " + NICK)
    send(IRC, "USER " + USER + " " + SERVER + " moses :" + NICK)

def import_commands():
    command_list = [f for f in os.listdir("commands")]

    command_list.remove("__init__.py")

    for command in command_list:
        if command[-4:] != ".pyc":
            command = command[:-3]

            log("Importing " + command + "...")

            module = getattr(__import__("commands." + command), command)
           
            COMMANDS_CONFIG[command] = getattr(module, "get_config")()

            try:
                if COMMANDS_CONFIG[command]["postprocess"]:
                    COMMANDS_POSTPROCESS[command] = getattr(module, "postprocess")
            except KeyError:
                pass          

            COMMANDS[command] = getattr(module, command)

def parse_message():
    messages = (IRC.recv(2048).decode('utf-8')) 

    #log(messages)

    messages = messages.strip("\r")
    messages = messages.split("\n")
    messages.pop() #get rid of extra value  
 
    for message in messages:
        if(message[0] == ":"):
            message = message[1:] #remove first character for easier parse
        message = message.split(":", 1)       
 
        # Special Checks
        if message[0] == "PING ":
            sendSilent(IRC, "PONG")
            continue

        if message[0] == "ERROR ":
            log(message[1])
            exit()

        #test to see if system notice
        meta = message[0]
        meta = meta.split("!")
        if len(meta) > 1: 
            #extract meta data in this hideous fashion
            command = {}
            command["host"] = IRC
            command["nick"] = meta[0]
            meta = meta[1].split("@")
            command["user"] = meta[0]
            meta = meta[1].split(" ")
            #error check for messages that are nasty
            if len(meta) > 2 and len(message) > 1: 
                command["message_type"] = meta[1]
                command["channel"] = meta[2]
                command["message"] = message[1].rstrip()  
                message = message[1].split(" ")

                command["options"] = parse_args(command["message"])

                if command["message"][0] == PREFIX:
                    command["command"] = message[0][1:].rstrip() 
                    handle_command(command)
                else:
                    message_alternate(command)

        else: #system
            if len(message) > 1: #protect against bad motd 
                log(message[1])

#If the message is not a command, other things may still need to be done
def message_alternate(command):

    for key in COMMANDS_POSTPROCESS:
        COMMANDS_POSTPROCESS[key](command, COMMANDS_CONFIG[key], get_config())

#many commands, handle it!
def handle_command(command):
    log(command["channel"] + " " + command["nick"]
            + "(" + command["user"] + "): " 
            + command["message"]
    )
    try:
        COMMANDS[command["command"]](command, COMMANDS_CONFIG[command["command"]], get_config())
    except KeyError:
        pass

#parse the arguments of the command and return an object
def parse_args(command):
    nodes = command.split(" ")
    args = [] #optionless args
    options = {} # - options
    initial_args = True
    option_next = False
    for i in range(1, len(nodes)):
        if nodes[i][0] == "-":
            initial_args = False
            option_next = True
        if initial_args:
            args.append(nodes[i])
        else:
            if option_next and i < len(nodes) - 1:
                options[nodes[i][1:]] = nodes[i + 1]
                option_next = False
            elif option_next:
                options[nodes[i][1:]] = True
                option_next = False

    options["args"] = args
    return options

### COMMANDS ###

if __name__ == "__main__":

    logging.basicConfig(filename=NICK + '.log', level=logging.DEBUG, format="%(message)s")

    import_commands()

    IRC = socket.socket() #defined here so other methods can see
    connect()
    join(IRC, CHAN)

    while(True):
        parse_message()
