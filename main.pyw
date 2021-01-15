import logging

# error logging
error_formatter = logging.Formatter(
    fmt="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

error_handler = logging.FileHandler("DAP_errors.log", delay=True)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(error_formatter)

base_logger = logging.getLogger()
base_logger.addHandler(error_handler)

import sys
import cli
import sound
import asyncio
import discord
import argparse

# commandline args
parser = argparse.ArgumentParser(description="Discord Audio Pipe")
connect = parser.add_argument_group("Command Line Mode")
query = parser.add_argument_group("Queries")

parser.add_argument(
    "-t",
    "--token",
    dest="token",
    action="store",
    default=None,
    help="The token for the bot",
)

parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Enable verbose logging",
)

connect.add_argument(
    "-c",
    "--channel",
    dest="channel",
    action="store",
    type=int,
    help="The channel to connect to as an id",
)

connect.add_argument(
    "-d",
    "--device",
    dest="device",
    action="store",
    type=int,
    help="The device to listen from as an index",
)

query.add_argument(
    "-D",
    "--devices",
    dest="query",
    action="store_true",
    help="Query compatible audio devices",
)

query.add_argument(
    "-C",
    "--channels",
    dest="online",
    action="store_true",
    help="Query servers and channels (requires token)",
)

args = parser.parse_args()
is_gui = not any([args.channel, args.device, args.query, args.online])

# verbose logs
if args.verbose:
    debug_formatter = logging.Formatter(
        fmt="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
    )

    debug_handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w"
    )
    debug_handler.setFormatter(debug_formatter)

    debug_logger = logging.getLogger("discord")
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.addHandler(debug_handler)

# don't import qt stuff if not using gui
if is_gui:
    import gui
    from PyQt5.QtWidgets import QApplication, QMessageBox
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

# main
async def main(bot, stream):
    try:
        # query devices
        if args.query:
            for device, index in sound.query_devices().items():
                print(index, device)

            return

        # check for token
        token = args.token
        if token is None:
            token = open("token.txt", "r").read()

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
            asyncio.ensure_future(cli.connect(bot, stream, args.device, args.channel))

        await bot.start(token)

    except FileNotFoundError:
        if is_gui:
            msg.setWindowTitle("Token Error")
            msg.setText("No Token Provided")
            msg.exec()

        else:
            print("No Token Provided")

    except discord.errors.LoginFailure:
        if is_gui:
            msg.setWindowTitle("Login Failed")
            msg.setText("Please check if the token is correct")
            msg.exec()

        else:
            print("Login Failed: Please check if the token is correct")

    except Exception:
        logging.exception("Error on main")


# run program
bot = discord.Client()
stream = sound.PCMStream()
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main(bot, stream))
except KeyboardInterrupt:
    print("Exiting...")
    loop.run_until_complete(bot.logout())
    loop.close()
