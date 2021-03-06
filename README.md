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
Get an IRC OAuth token [here](https://twitchapps.com/tmi/).

Get a Client ID [here](https://dev.twitch.tv/console/apps/create).

#### Discord
Create your bot application and find a token [here](https://discord.com/developers/applications).

### Environment
The following environment variables are used by the program:

- BOTNAME=the name for your bot
- TWITCH_CHANNEL=channel to connect to (for twitch bots)
- TWITCH_TOKEN=IRC OAuth token (for twitch bots)
- TWITCH_ID=Client ID (for twitch bots)
- DISCORD_TOKEN= Bot token (for discord bots)
- DISCORD_OWNER_ID= User ID of bot owner (for discord bots)

### Requirements
`pip install -r requirements.txt`

### Testing
`python -m unittest`

### Command line
`python -m keelimebot.main -h`

## TODO
- Check updates in requirement submodules..
