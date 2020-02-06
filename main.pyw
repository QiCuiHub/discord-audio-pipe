import ui
import asyncio
import discord
import logging
from tkinter import messagebox

root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)

fh = logging.FileHandler('DAP_errors.log', delay=True)
fh.setLevel(logging.ERROR)

root_logger.addHandler(fh)

async def ready(bot_ui):
    await bot.wait_until_ready()
    
    bot_ui.set_cred(bot.user.name)
    bot_ui.set_servers([guild for guild in bot.guilds])

try:
    token = open('token.txt', 'r').read()

    loop = asyncio.get_event_loop()
    bot = discord.Client(loop=loop)
    bot_ui = ui.UI(bot)

    asyncio.ensure_future(bot_ui.run_tk())
    asyncio.ensure_future(ready(bot_ui))
    bot.run(token)

except FileNotFoundError:
    messagebox.showerror('Token Error', "token.txt was not found")

except:
    logging.exception('Error on main')
