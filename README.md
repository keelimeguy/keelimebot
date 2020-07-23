# Keelimebot

My custom bot for Twitch.

## Commands
|Command|Parameters|Description|Permissions
|----------|-----------|-----------|-----------|
|**!addcommand**|\<new_cmd> \<action>|*Add a command in the channel*|Moderator|
|**!delcommand**|\<cmd>|*Remove a command from the channel*|Moderator|
|**!bottest**|n/a|*Check that the bot is connected*|Moderator|
|**!commandlist**|n/a|*Provides the list of commands created with !addcommand*|Any|
|**!help**|n/a|*Provides link to this repository*|Any|

## Usage
For developers wishing to build their own bots, read on.

Python virtual environment is always recommended.

### Tokens
Get an IRC OAuth token [here](https://twitchapps.com/tmi/).

Get a Client ID [here](https://dev.twitch.tv/console/apps/create).

### Requirements
`pip install -r requirements.txt`

### Testing
`python -m unittest`

### Command line
`python -m keelimebot.main -h`
