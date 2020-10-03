
# discord-audio-pipe
Barebones program to send stereo computer audio (microphone, stereo mix, virtual audio cable, etc) into a discord bot.

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
    $ pip3 install PyQt5
```
In some cases PortAudio may be missing, on Ubuntu they can be installed with
```
    $ sudo apt-get install libportaudio2
```

## CLI
Running `main.pyw` / ``dap.exe`` without any arguments will start the graphical interface. Alternatively, discord-audio-pipe can  be run from the command line and contains some tools to query system audio devices and accessible channels.
```
usage: main.pyw [-h] [-c CHANNEL] [-d DEVICE] [-t TOKEN] [-q] [-o]

Discord Audio Pipe

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        The token for the bot

Command Line Mode:
  -c CHANNEL, --channel CHANNEL
                        The channel to connect to as an id
  -d DEVICE, --device DEVICE
                        The device to listen from as an index

Queries:
  -q, --query           Query compatible audio devices
  -o, --online          Query accessible servers and channels, requires token
```