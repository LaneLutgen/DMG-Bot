
# DMG-Bot

A helpful bot for [r/gameboy's](https://old.reddit.com/r/Gameboy/) discord.
Currently provides the following features:

* Dice roller
* Currency converter (using http://currencyconverterapi.com)
* Google Image search (using Google CSE)
* 
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.6+
```

### Installing


First, clone this project and create a venv on top of the folder.

```
$ git clone https://github.com/GameboyDiscord/DMG-Bot
$ python3 -m venv DMG-Bot && cd DMG-Bot
$ source bin/activate
```
Install the required python packages with pip.
```
$ pip install -r requirements.txt
```

 `config.example.yaml` and add your discord bot key (and optionally your CSE keys) to it.
```
$ mv config.example.yaml config.yaml
$ nano config.yaml
```

```
BOT_KEY="YOUR BOT KEY"
```
Finally, start the bot:
```
$ python3 GB_Bot.py
```

## Adding new extensions

Simply create a new python module inside the `cogs` folder, the bot will automatically attempt to load it on startup. For an example, check out the dice rolling extension `cogs/dice.py` and the [discord.py documention](https://discordpy.readthedocs.io/en/latest/).

Please be aware that this project is using the `rewrite` branch of discord.py, keep that in mind when browsing the documentation.