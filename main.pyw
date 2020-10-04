import sys
import gui
import cli
import sound
import asyncio
import discord
import logging
import argparse
from PyQt5.QtWidgets import QApplication

# error logging
root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)

fh = logging.FileHandler('DAP_errors.log', delay=True)
fh.setLevel(logging.ERROR)

root_logger.addHandler(fh)

# commandline args
parser = argparse.ArgumentParser(description='Discord Audio Pipe')
connect = parser.add_argument_group('Command Line Mode')
query = parser.add_argument_group('Queries')

parser.add_argument('-t', '--token', dest='token', action='store',
                    default=None, help='The token for the bot')

connect.add_argument('-c', '--channel', dest='channel', action='store',
                     type=int, help='The channel to connect to as an id')

connect.add_argument('-d', '--device', dest='device', action='store', type=int,
                     help='The device to listen from as an index')

query.add_argument('-q', '--query', dest='query', action='store_true',
                   help='Query compatible audio devices')

query.add_argument('-o', '--online', dest='online', action='store_true',
                   help='Query servers and channels (requires token)')

args = parser.parse_args()
is_gui = not any([args.channel, args.device, args.query, args.online])

# main
async def main(bot, stream):
    try:
        token = args.token
        if token is None:
            token = open('token.txt', 'r').read()

        # query devices
        if args.query:
            for device, index in sound.query_devices().items():
                print(index, device)

            return

        # query servers and channels
        if args.online:
            if token is None:
                print('No Token detected')
            else:
                await cli.query(bot, token)

            return

        # GUI
        if is_gui:
            app = QApplication(sys.argv)
            bot_ui = gui.GUI(app, bot, stream)
            bot_ui.load_style()
            asyncio.ensure_future(bot_ui.ready())
            asyncio.ensure_future(bot_ui.run_Qt())

        # CLI
        else:
            asyncio.ensure_future(cli.connect(
                bot,
                stream,
                args.device,
                args.channel,
                token
            ))

        await bot.start(token)

    except FileNotFoundError:
        logging.exception('No Token Provided')

    except Exception:
        logging.exception('Error on main')

# run program
bot = discord.Client()
stream = sound.PCMStream()
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main(bot, stream))
except KeyboardInterrupt:
    print('Exiting...')
    loop.run_until_complete(bot.logout())
    loop.close()
