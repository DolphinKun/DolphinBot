# DolphinBot
DolphinBot is a GPL-licensed Python-based bot for CyTube, that's fast and easy-to-use.

Unlike many other bots, it has a 100% modular plugin system, so you can easily write plugins. An example plugin could look like this (plugin function is the same name as the file):  
```
commands = ["!test"]
pm = False

# data = message data
# data["msg"] = message contents
# data["username"] = called by user
def test(dolphinbot, data):
    dolphinbot.send_message("Test!", data["username"])
```

# Installation
To use DolphinBot, you must install the below dependencies (pip is needed):
- bs4 (for account login)
- requests
- python-socketio[client] 
- lxml  

Installation steps:
- Edit the config.py file and set your settings.  
- Install the dependencies, with (if pip3 is not found, try pip instead): `pip3 install requirements.txt`  
- Run the bot from the bot's folder: `python3 run.py`
# Compatibility 
DolphinBot needs Python 3+ or higher. Python 2 is untested.  
DolphinBot has been tested under GNU/Linux only. It may work under Windows, but it hasn't been confirmed yet.
# Plugins
Go get them here: https://github.com/DolphinKun/DolphinBotPlugins
# Contributing
Fork this repository, add your changes to your repository, then open a merge request for this repository to merge your repository with this repository.
