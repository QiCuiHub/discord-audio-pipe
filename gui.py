import os
import sys
import sound
import asyncio
import logging
import discord
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import (
    QFontDatabase,
    QFontMetrics,
    QIcon
)
from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
    QEventLoop,
    QDir
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QFrame,
    QGridLayout,
    QComboBox,
    QLabel,
    QHBoxLayout,
    QStyledItemDelegate
)

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


class TitleBar(QFrame):
    def __init__(self, parent):
        # title bar
        super(TitleBar, self).__init__()
        self.setObjectName('titlebar')

        # discord
        self.parent = parent
        self.bot = parent.bot

        # layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # window title
        title = QLabel("Discord Audio Pipe")

        # minimize
        minimize_button = QPushButton('—')
        minimize_button.setObjectName('minimize')
        layout.addWidget(minimize_button)

        # close
        close_button = QPushButton('✕')
        close_button.setObjectName('close')
        layout.addWidget(close_button)

        # add widgets
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(minimize_button)
        layout.addWidget(close_button)

        # events
        minimize_button.clicked.connect(self.minimize)
        close_button.clicked.connect(
            lambda: asyncio.ensure_future(self.close())
        )

    async def close(self):
        # workaround for logout bug
        for voice in self.bot.voice_clients:
            try:
                await voice.disconnect()
            except Exception:
                pass

        self.bot._closed = True
        await self.bot.ws.close()
        self.parent.close()

    def minimize(self):
        self.parent.showMinimized()


class GUI(QMainWindow):

    def __init__(self, app, bot, stream):
        # app
        super(GUI, self).__init__()
        QDir.setCurrent(bundle_dir)
        self.app = app

        # window info
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        window_icon = QIcon('./assets/favicon.ico')
        self.setWindowTitle('Discord Audio Pipe')
        self.app.setWindowIcon(window_icon)
        self.position = None

        # discord
        self.bot = bot
        self.voice = None
        self.stream = stream

        # layout
        central = QWidget()
        layout = QGridLayout()
        central.setLayout(layout)

        # loading
        self.info = QLabel('Connecting...')
        self.loading = QSvgWidget('./assets/loading.svg')

        # devices
        self.devices = QComboBox(self)
        self.devices.setItemDelegate(QStyledItemDelegate())
        self.devices.setPlaceholderText('None')
        device_lb = QLabel('Devices')
        device_lb.setObjectName('label')

        for device, idx in sound.query_devices().items():
            self.devices.addItem(device + '   ', idx)

        # servers
        self.servers = QComboBox(self)
        self.servers.setItemDelegate(QStyledItemDelegate())
        self.servers.addItem('None', None)
        server_lb = QLabel('Servers     ')
        server_lb.setObjectName('label')

        # channels
        self.channels = QComboBox(self)
        self.channels.setItemDelegate(QStyledItemDelegate())
        self.channels.addItem('None', None)
        channel_lb = QLabel('Channels  ')
        channel_lb.setObjectName('label')

        # mute
        self.mute = QPushButton('Mute', self)
        self.mute.setObjectName('mute')

        # add widgets
        layout.addWidget(self.info,     0, 0, 1, 3)
        layout.addWidget(self.loading,  0, 3, alignment=Qt.AlignHCenter)
        layout.addWidget(device_lb,     1, 0)
        layout.addWidget(self.devices,  2, 0)
        layout.addWidget(server_lb,     1, 1)
        layout.addWidget(self.servers,  2, 1)
        layout.addWidget(channel_lb,    1, 2)
        layout.addWidget(self.channels, 2, 2)
        layout.addWidget(self.mute,     2, 3)

        # events
        self.devices.currentTextChanged.connect(self.change_device)
        self.servers.currentTextChanged.connect(
            lambda: asyncio.ensure_future(self.change_server())
        )
        self.channels.currentTextChanged.connect(
            lambda: asyncio.ensure_future(self.change_channel())
        )
        self.mute.clicked.connect(self.toggle_mute)

        # build window
        titlebar = TitleBar(self)
        self.setMenuWidget(titlebar)
        self.setCentralWidget(central)
        self.disable_ui()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.position = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.position is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.position = None
        event.accept()

    def disable_ui(self):
        self.loading.setVisible(True)
        self.devices.setEnabled(False)
        self.servers.setEnabled(False)
        self.channels.setEnabled(False)
        self.mute.setEnabled(False)

    def enable_ui(self):
        self.loading.setVisible(False)
        self.devices.setEnabled(True)
        self.servers.setEnabled(True)
        self.channels.setEnabled(True)
        self.mute.setEnabled(True)

    async def run_Qt(self, interval=0.01):
        while True:
            QCoreApplication.processEvents(
                QEventLoop.AllEvents,
                interval * 1000
            )
            await asyncio.sleep(interval)

    def resize_combobox(self, combobox):
        font = combobox.property('font')
        metrics = QFontMetrics(font)
        min_width = 0

        for i in range(combobox.count()):
            size = metrics.horizontalAdvance(combobox.itemText(i))
            if size > min_width:
                min_width = size

        combobox.setMinimumWidth(min_width + 30)

    async def ready(self):
        await self.bot.wait_until_ready()
        self.info.setText(f'Logged in as: {self.bot.user.name}')

        for guild in self.bot.guilds:
            self.servers.addItem(guild.name, guild)

        self.resize_combobox(self.servers)
        self.enable_ui()

    def load_style(self):
        QFontDatabase.addApplicationFont('./assets/Roboto-Black.ttf')

        with open('./assets/style.qss', 'r') as qss:
            self.app.setStyleSheet(qss.read())

        self.show()

    def change_device(self):
        try:
            selection = self.devices.currentData()
            self.mute.setText('Mute')

            if selection is not None:
                if self.voice is not None:
                    self.voice.stop()
                    self.stream.change_device(selection)
                    self.voice.play(discord.PCMAudio(self.stream))
                else:
                    self.stream.change_device(selection)

        except Exception:
            logging.exception('Error on change_device')

    async def change_server(self):
        try:
            selection = self.servers.currentData()
            self.channels.clear()
            self.channels.addItem('None', None)
            self.mute.setText('Mute')

            if selection is not None:
                self.channels.clear()
                self.channels.addItem('None', None)

                for channel in selection.channels:
                    if isinstance(channel, discord.VoiceChannel):
                        self.channels.addItem(channel.name, channel)

            self.resize_combobox(self.channels)

            if self.voice is not None:
                self.voice.stop()
                await self.voice.disconnect()
                self.voice = None

        except Exception:
            logging.exception('Error on change_server')

    async def change_channel(self):
        try:
            selection = self.channels.currentData()
            self.mute.setText('Mute')

            if selection is not None:
                self.disable_ui()

                not_connected = (
                    self.voice is None or
                    self.voice is not None and
                    not self.voice.is_connected()
                )

                if not_connected:
                    self.voice = await selection.connect(timeout=10)
                else:
                    await self.voice.move_to(selection)

                not_playing = (
                    self.devices.currentData() is not None and
                    not self.voice.is_playing()
                )

                if not_playing:
                    self.voice.play(discord.PCMAudio(self.stream))

            else:
                if self.voice is not None:
                    self.voice.stop()
                    await self.voice.disconnect()
                    self.voice = None

        except Exception:
            logging.exception('Error on change_channel')

        finally:
            self.enable_ui()

    def toggle_mute(self):
        try:
            if self.voice is not None:
                if self.voice.is_playing():
                    self.voice.pause()
                    self.mute.setText('Resume')
                else:
                    self.voice.resume()
                    self.mute.setText('Mute')

        except Exception:
            logging.exception('Error on toggle_mute')
