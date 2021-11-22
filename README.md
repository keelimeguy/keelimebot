# Keelimebot
![build-status-master](https://github.com/keelimeguy/keelimebot/actions/workflows/python-app.yml/badge.svg?branch=master)
[![GitHub license](https://img.shields.io/github/license/keelimeguy/keelimebot)](https://github.com/keelimeguy/keelimebot/blob/master/LICENSE)

My custom bot for Twitch/Discord.

## Commands
|Command|Parameters|Description|Permissions
|----------|-----------|-----------|-----------|
|**!addcommand**|\<new_cmd> \<action>|*Add a command in the channel*|Moderator|
|**!delcommand**|\<cmd>|*Remove a command from the channel*|Moderator|
|**!bottest**||*Check that the bot is connected*|Moderator|
|**!commandlist**||*Provides the list of commands created with !addcommand*|Any|
|**!help**||*Provides link to this repository*|Any|

## Usage
**For developers wishing to build their own bots, read on.**

Python virtual environment is always recommended.

### Tokens

#### Twitch

Get a Client ID / Client Secret [here](https://dev.twitch.tv/console/apps/create/).

Get a Twitch access token (for development, not recommended for production) [here](https://twitchtokengenerator.com/).

#### Discord
Create your bot application and find a token [here](https://discord.com/developers/applications).

### Environment
The following environment variables are used by the program (the `./run.sh` script can help set them automatically):

- TWITCH_TOKEN= Twitch Access Token (for twitch bots)
- DISCORD_OWNER_ID= User ID of bot owner (for discord bots)
- BOT_EMOJI_GUILD= Guild ID of main bot discord channel (for grabbing emojis)
- DISCORD_TOKEN= Bot token (for discord bots)

### Requirements
- Using script: `./run.sh venv`
- Without script: `python3 -m pip install -r requirements.txt`

### Testing
- Using script: `./run.sh test`
- Without script: `python3 -m unittest`

### Command line
- Using script: `./run.sh -h`
- Without script: `python3 -m keelimebot.main -h`

## TODO
- Check updates in requirement submodules..
