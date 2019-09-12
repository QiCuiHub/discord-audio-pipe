# discord-audio-pipe
Barebones program to send computer audio (microphone, stereo mix, virtual audio cable, etc) into a discord bot.  
You can download the latest release [here](https://github.com/QiCuiHub/discord-audio-pipe/releases).

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
4. Create a file ``token.txt`` in the same directory as ``main.py`` / ``dap.exe`` and put the bot token inside
