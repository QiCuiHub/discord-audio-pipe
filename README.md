# discord-audio-pipe
Barebones program to send computer audio (microphone, stereo mix, virtual audio cable, etc) into a discord bot.  

You can download the latest release [**here**](https://github.com/QiCuiHub/discord-audio-pipe/releases)
- If you are using the executable, run ``dap.exe``  
- If you are using the source code, install the dependencies and start the program using ``main.pyw``

## Setting up a Bot account
1. Follow the steps [**here**](https://discordpy.readthedocs.io/en/latest/discord.html) to setup and invite a discord bot
2. To link the program to your bot, create a file ``token.txt`` in the same directory as ``main.pyw`` / ``dap.exe`` and save the bot token inside

## Dependencies
Python 3.5+
```
    $ pip3 install discord.py[voice]
    $ pip3 install sounddevice
    $ pip3 install numpy
```
