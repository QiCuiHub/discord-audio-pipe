#!/usr/bin/env python3
import os
import gui
import cli
import asyncio
import discord
import logging
import argparse
import platform
from tkinter import messagebox

# set display if not set
if os.environ.get('DISPLAY', '') == '' and platform.system() == 'Linux':
    os.environ.__setitem__('DISPLAY', ':0.0')

# error logging
root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)

fh = logging.FileHandler('DAP_errors.log', delay=True)
fh.setLevel(logging.ERROR)

root_logger.addHandler(fh)

# commandline args
parser = argparse.ArgumentParser(description='Discord Audio Pipe')
connect = parser.add_argument_group('Connect')
query = parser.add_argument_group('Query')

parser.add_argument('-g', '--gui', dest='gui', action='store_true',
                   help='Start a graphical interface (default when no args)')

connect.add_argument('-s', '--server', dest='server', action='store_true',
                   help='The server to connect to as an id')

connect.add_argument('-c', '--channel', dest='channel', action='store_true',
                   help='The channel to connect to as an id')

connect.add_argument('-d', '--device', dest='device', action='store_true',
                   help='The device to listen from as an index')

parser.add_argument('-t', '--token', dest='token', action='store', default=None
                   help='The token for the bot')

query.add_argument('-q', '--query', dest='query', action='store_true',
                   help='Query useable devices')

query.add_argument('-o', '--online', dest='online', action='store_true',
                   help='Query accessible servers and channels, requires token')

args = parser.parse_args()
is_gui = args.gui or not any([args.server, args.channel, args.device])

# run program
try:
    token = args.token

    if token is None:
        token = open('token.txt', 'r').read()
    
    bot = discord.Client()

    if is_gui:
        bot_ui = gui.GUI(bot)
        asyncio.ensure_future(bot_ui.run_tk())
        asyncio.ensure_future(bot_ui.ready())

    bot.run(token)

except FileNotFoundError:
    if is_gui: messagebox.showerror('Token Error', "No token detected")
    else: print('No token detected')

except:
    logging.exception('Error on main')
