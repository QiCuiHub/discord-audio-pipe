# discord-audio-bot
Barebones program to send computer audio (microphone, stereo mix, virtual audio cable, etc) into a discord bot.

## Dependencies
Python 3.5+
```
    $ pip3 install discord.py[voice]
    $ pip3 install sounddevice
    $ pip3 install numpy
```

## Use
1. Create a discord application [here](https://discordapp.com/developers/applications/me) and make a bot user
3. Get client id from the application and invite the bot using
   - ``https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID>&scope=bot``
4. Provide the voice channel id, bot token, and sound device to the code and run
