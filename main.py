import ui
import asyncio
import discord

async def ready(bot_ui):
    await bot.wait_until_ready()
    
    bot_ui.set_cred(bot.user.name)
    bot_ui.set_servers([guild for guild in bot.guilds])

loop = asyncio.get_event_loop()
bot = discord.Client(loop=loop)
bot_ui = ui.UI(bot)

asyncio.ensure_future(bot_ui.run_tk())
asyncio.ensure_future(ready(bot_ui))
bot.run(open('token.txt', 'r').read())
