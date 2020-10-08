import sys
import gui
import cli
import sound
import asyncio
import discord
import logging
import argparse
from PyQt5.QtWidgets import QApplication, QMessageBox

# error logging
formatter = logging.Formatter(
    fmt='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

error_handler = logging.FileHandler('DAP_errors.log', delay=True)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

base_logger = logging.getLogger()
base_logger.addHandler(error_handler)

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
async def main(app, bot, stream, msg):
    try:
        # query devices
        if args.query:
            for device, index in sound.query_devices().items():
                print(index, device)

            return

        # check for token
        token = args.token
        if token is None:
            token = open('token.txt', 'r').read()

        # query servers and channels
        if args.online:
            await cli.query(bot, token)

            return

        # GUI
        if is_gui:
            bot_ui = gui.GUI(app, bot, stream)
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
        if is_gui:
            msg.setWindowTitle('Token Error')
            msg.setText('No Token Provided')
            msg.exec();

        else:
            print('No Token Provided')

    except discord.errors.LoginFailure:
        if is_gui:
            msg.setWindowTitle('Login Error')
            msg.setText('Login Failed')
            msg.exec();        

        else:
            print('Login Failed')

    except Exception:
        logging.exception('Error on main')

# run program
app = QApplication(sys.argv)
bot = discord.Client()
stream = sound.PCMStream()

msg = QMessageBox()
msg.setIcon(QMessageBox.Information)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main(app, bot, stream, msg))
except KeyboardInterrupt:
    print('Exiting...')
    loop.run_until_complete(bot.logout())
    loop.close()
