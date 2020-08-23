import sound
import discord
import asyncio
import logging
import tkinter as tk

class UI():
    def __init__(self, bot):
        self.root = tk.Tk()
        self.root.title('Bot')
        
        self.bot = bot
        self.voice = None
        self.stream = sound.PCMStream()
        
        self.cred = tk.Label(self.root, text='Connecting...', fg='black')
        self.cred.grid(row=0, column=0, columnspan=2, sticky='W')
        
        tk.Label(self.root, text='Device', fg='black').grid(row=1, column=0)
        tk.Label(self.root, text='Server', fg='black').grid(row=1, column=1)
        tk.Label(self.root, text='Channel', fg='black').grid(row=1, column=2)

        device_options = sound.query_devices()
        self.dv = tk.StringVar(self.root)
        self.dv.trace('w', lambda *args: self.change_device(device_options, self.dv))
        self.dv.set(device_options.get(0))
        device = tk.OptionMenu(self.root, self.dv, *device_options)
        device.grid(row=2, column=0)

        self.sv = tk.StringVar(self.root)
        self.sv.trace('w', lambda *args: asyncio.ensure_future(self.change_server()))
        self.sv.set('None')
        self.server = tk.OptionMenu(self.root, self.sv, 'None')
        self.server.grid(row=2, column=1)
        self.server_map = {}

        self.cv = tk.StringVar(self.root)
        self.cv.trace("w", lambda *args: asyncio.ensure_future(self.change_channel()))
        self.cv.set('None')
        self.channel = tk.OptionMenu(self.root, self.cv, 'None')
        self.channel.grid(row=2, column=2)
        self.channel_map = {}

        self.mv = tk.StringVar(self.root)
        self.mv.set('Mute')
        self.mute = tk.Button(self.root, textvariable=self.mv, command=self.toggle_mute)
        self.mute.grid(row=2, column=3, padx=5)
        
        self.root.protocol('WM_DELETE_WINDOW', lambda: asyncio.ensure_future(self.exit()))

    async def exit(self):
        # workaround for logout bug 
        self.bot._closed = True

        for voice in self.bot.voice_clients:
            try:
                await voice.disconnect()
            except Exception:
                pass

        await self.bot.ws.close()
        self.root.destroy()

    def change_device(self, options, dv):
        try:
            if dv.get() != 'None':
                if self.voice is not None:
                    self.voice.stop()
                    self.stream.change_device(options.get(dv.get()))
                    self.voice.play(discord.PCMAudio(self.stream))
                else:
                    self.stream.change_device(options.get(dv.get()))
                    
        except:
            logging.exception('Error on change_device')

    async def run_tk(self, interval=0.05):
        try:
            while True:
                self.root.update()
                await asyncio.sleep(interval)
        except tk.TclError as e:
            return

    async def change_server(self):
        try:
            s_name = self.sv.get()

            if s_name != 'None':
                guild = discord.utils.find(lambda s: s.id == self.server_map[s_name].id, self.bot.guilds)
                channel_names = [c for c in guild.channels if isinstance(c, discord.VoiceChannel)]
                self.set_channels(channel_names)    
            else:
                self.set_channels([])

            if self.voice is not None:
                await self.voice.disconnect()
                self.voice = None
                
        except:
            logging.exception('Error on change_server')
        
    async def change_channel(self):
        try:
            s_name = self.sv.get()
            c_name = self.cv.get()
        
            if c_name != 'None':
                guild = discord.utils.find(lambda s: s.id == self.server_map[s_name].id, self.bot.guilds)
                channel = discord.utils.find(lambda c: c.id == self.channel_map[c_name].id, guild.channels)
                
                if self.voice is None or (self.voice is not None and not self.voice.is_connected()):
                    self.voice = await channel.connect()
                else:
                    await self.voice.move_to(channel)

                if self.dv.get() != 'None' and not self.voice.is_playing():
                    self.voice.play(discord.PCMAudio(self.stream))

            else:
                if self.voice is not None:
                    await self.voice.disconnect()
                    self.voice = None
                    
        except:
            logging.exception('Error on change_channel')
 
    def deEmojify(self, inputString):
        return ''.join(char for char in inputString if char <= '\uffff')
 
    def set_cred(self, username):
        self.cred.config(text='Logged in as: ' + self.deEmojify(username))

    def set_servers(self, servers):
        menu = self.server['menu']
        
        for idx, server in enumerate(servers):
            escaped = str(idx) + '. ' + self.deEmojify(server.name)
            menu.add_command(label=escaped, command=lambda value=escaped: self.sv.set(value))
            self.server_map[escaped] = server
        
    def set_channels(self, channels):
        menu = self.channel['menu']
        menu.delete(0, 'end')
        menu.add_command(label='None', command=lambda value='None': self.cv.set(value))    
        self.cv.set('None')
        self.channel_map.clear()

        for idx, channel in enumerate(channels):
            escaped = str(idx) + '. ' + self.deEmojify(channel.name)
            menu.add_command(label=escaped, command=lambda value=escaped: self.cv.set(value))
            self.channel_map[escaped] = channel
 
    def toggle_mute(self):
        try:
            if self.voice is not None:
                if self.voice.is_playing():
                    self.voice.pause()
                    self.mv.set('Resume')
                else:
                    self.voice.resume()
                    self.mv.set('Mute')
                    
        except:
            logging.exception('Error on toggle_mute')