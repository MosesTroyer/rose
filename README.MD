Rose is an IRC bot written to do whatever functions I randomly want.

Some code liberally borrowed from github.com/ccowmu/botler , cclub++

All commands are placed in the commands directory. Every command should have 2 methods: 1 with the same name as the file itself, and get_config() to store information about the command.

The command method should accept an object with information about the command given, along with the configuration object.

get_config() should return an object with the following fields, if it needs them:
    man: documentation about the method to display 
    postprocess: boolean on whether this command has a postprocess method, defined as postprocess(command, config)
