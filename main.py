import ui
import asyncio
import discord

async def ready(bot, bot_ui):
    await bot.wait_until_ready()
    
    bot_ui.set_cred(bot.user.name)
    bot_ui.set_servers([server for server in bot.servers])

bot = discord.Client()
bot_ui = ui.UI(bot)
loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(bot_ui.run_tk())
    asyncio.ensure_future(ready(bot, bot_ui))
    
    loop.run_until_complete(bot.start(open('token.txt', 'r').read()))
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
finally:
    loop.close()
