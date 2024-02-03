#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import platform
import sys
import time
from datetime import datetime

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

os_name = platform.system()
if os_name == 'Linux':
    print(f"{os_name} OS detected")
    from gpiozero import CPUTemperature
elif os_name == 'Windows':
    print(f"{os_name} OS detected")
else:
    print(f"{os_name} OS detected. I'm not sure if my script run on it")


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    if chat_id == chat_id_key:
        if command in command_linux:
            if os_name == 'Linux':
                # Useful commands for Raspberry
                if command in ['/temperature', 'Temp. 🌡️']:
                    bot.sendMessage(chat_id_key, f'{str(temperature)} °C')

                if command in ['/quick_update', 'Update ⚙️']:
                    bot.sendMessage(chat_id_key, 'Starting update...')
                    os.system('sudo apt-get update -y')
                    bot.sendMessage(chat_id_key, 'Update done.\nStarting upgrade...')
                    os.system('sudo apt-get upgrade -y')
                    bot.sendMessage(chat_id_key, 'Upgrade done')

                if command == '/update':
                    bot.sendMessage(chat_id_key, 'Starting update...')
                    os.system('sudo apt-get update -y')
                    bot.sendMessage(chat_id_key, 'Update done.\nStarting upgrade...')
                    os.system('sudo apt-get upgrade -y')
                    bot.sendMessage(chat_id_key, 'Upgrade done.\nStarting autoremove...')
                    os.system('sudo apt-get autoremove -y')
                    bot.sendMessage(chat_id_key, 'Autoremove done.\nStarting reboot...\nSee U soon')

                if command in ['/reboot', 'Reboot 🔄️']:
                    bot.sendMessage(chat_id_key, 'See U soon')
                    os.system('sudo reboot now')

                if command in ['/shutdown', 'Shutdown 🛑']:
                    bot.sendMessage(chat_id_key, 'Seen U soon')
                    os.system('sudo shutdown now')

        elif command in command_hyperion:
            # Commands for Hyperion
            if command in ['/hyperion_on', 'Start 🌞']:
                os.system('hyperion-remote --on')
                os.system('hyperion-remote --clearall')
                os.system('hyperion-remote -E V4L')
                bot.sendMessage(chat_id_key, "Ambilight ON")

            if command in ['/hyperion_off', 'Stop 🌚']:
                os.system('hyperion-remote --off')
                bot.sendMessage(chat_id_key, "Ambilight OFF")

            if command in ['/video_on', 'Video ▶️']:
                os.system('hyperion-remote --clearall')
                os.system('hyperion-remote -E V4L')
                bot.sendMessage(chat_id_key, "Video ON")

            if command in ['/video_off', 'Video ⏹️']:
                os.system('hyperion-remote --clearall')
                os.system('hyperion-remote -D V4L')
                bot.sendMessage(chat_id_key, "Video OFF")

            if command in ['/brightness', 'Bright. 🔅']:
                bot.sendMessage(chat_id_key, 'Choose brightness:', reply_markup=brightness_keyboard)

            if command in ['/effect', 'Effect 🎆']:
                bot.sendMessage(chat_id_key, 'Choose color/effect:', reply_markup=color_effect_keyboard)

        elif command in command_telegram_bot:
            # Commands for Telegram bot
            if command == '/test':
                bot.sendMessage(chat_id_key, "I'm running :)")

            if command in ['/help', 'Help ❔']:
                if os_name == 'Linux':
                    bot.sendMessage(chat_id_key,
                                    "/temperature - Get CPU temperature\n"
                                    "/quick_update - To update and upgrade without autoremove and reboot\n"
                                    "/update - To update, upgrade, autoremove AND REBOOT\n"
                                    "/reboot - Sometimes it's good\n"
                                    "/shutdown - As excepted\n"
                                    "/hyperion_on - Turn on Hyperion\n"
                                    "/hyperion_off - Turn off Hyperion\n"
                                    "/video_on - Hyperion based on video input\n"
                                    "/video_off - Hyperion background effect/color\n"
                                    "/brightness - Manage brightness\n"
                                    "/effect - Select effect\n"
                                    "/test - Is my Telegram bot still works ?\n"
                                    "/help - A little reminder")
                else:
                    bot.sendMessage(chat_id_key,
                                    "/hyperion_on - Turn on Hyperion\n"
                                    "/hyperion_off - Turn off Hyperion\n"
                                    "/video_on - Hyperion based on video input\n"
                                    "/video_off - Hyperion background effect/color\n"
                                    "/brightness - Manage brightness\n"
                                    "/effect - Select effect\n"
                                    "/test - Is my Telegram bot still works ?\n"
                                    "/help - A little reminder")

        else:
            if os_name != 'Linux':
                bot.sendMessage(chat_id_key, f"Command not allowed for {os_name}... Try /help")
            else:
                bot.sendMessage(chat_id_key, "I don't understand... Try /help")

    # For unknown ID connection
    else:
        # Send to unknown ID (not allowed to talk with your bot)
        message_to_unknown_id = f'You are not allowed, your ID is {chat_id}'
        bot.sendMessage(chat_id, message_to_unknown_id)

        # Send to you to warn you about unknown ID wants to talk with your Telegram Bot
        warning_unknown_id = f'Someone trying to do something strange...\nID: {chat_id}\nMessage: {str(command)}'
        bot.sendMessage(chat_id_key, warning_unknown_id)


def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    if query_data.isdigit():
        os.system(f'hyperion-remote -L {int(query_data)}')
        bot.answerCallbackQuery(query_id, text=f"Brightness {int(query_data)}%")
    else:
        os.system('hyperion-remote --clearall')
        if query_data in ['FF0000', 'FFA500', 'FFFF00', '00FF00', '0000FF', '4B0082', '8A2BE2', 'FFC0CB', 'FFFFFF']:
            os.system(f'hyperion-remote -c {query_data}')
        else:
            os.system(f'hyperion-remote -e "{query_data}"')
        bot.answerCallbackQuery(query_id, text=f"Color/effect {query_data} applied ")


command_linux = ['/temperature', 'Temp. 🌡️',
                 '/quick_update', 'Update ⚙️',
                 '/update',
                 '/reboot', 'Reboot 🔄️',
                 '/shutdown', 'Shutdown 🛑']

command_hyperion = ['/hyperion_on', 'Start 🌞',
                    '/hyperion_off', 'Stop 🌚',
                    '/brightness', 'Bright. 🔅',
                    '/effect', 'Effect 🎆',
                    '/b100',
                    '/b75',
                    '/b50',
                    '/b25',
                    '/video_on', 'Video ▶️',
                    '/video_off', 'Video ⏹️']

command_telegram_bot = ['/test',
                        '/help', 'Help ❔']

main_buttons = [
    [KeyboardButton(text='Start 🌞'), KeyboardButton(text='Stop 🌚')],
    [KeyboardButton(text='Video ▶️'), KeyboardButton(text='Video ⏹️')],
    [KeyboardButton(text='Effect 🎆'), KeyboardButton(text='Bright. 🔅')],
    [KeyboardButton(text='Temp. 🌡️'), KeyboardButton(text='Update ⚙️')],
    [KeyboardButton(text='Reboot 🔄️'), KeyboardButton(text='Shutdown 🛑')],
    [KeyboardButton(text='Help ❔')]
]
main_keyboard = ReplyKeyboardMarkup(keyboard=main_buttons, resize_keyboard=True)

brightness_button = [
    [InlineKeyboardButton(text='25', callback_data='25')],
    [InlineKeyboardButton(text='50', callback_data='50')],
    [InlineKeyboardButton(text='75', callback_data='75')],
    [InlineKeyboardButton(text='100', callback_data='100')]
]
brightness_keyboard = InlineKeyboardMarkup(inline_keyboard=brightness_button)

color_effect_button = [
    [InlineKeyboardButton(text='Red 🔴', callback_data='FF0000'),
     InlineKeyboardButton(text='Orange 🟠', callback_data='FFA500'),
     InlineKeyboardButton(text='Yellow 🟡', callback_data='FFFF00')],
    [InlineKeyboardButton(text='Green 🟢', callback_data='00FF00'),
     InlineKeyboardButton(text='Blue 🩵', callback_data='0000FF'),
     InlineKeyboardButton(text='Indigo 🔵', callback_data='4B0082')],
    [InlineKeyboardButton(text='Purple 🟣', callback_data='8A2BE2'),
     InlineKeyboardButton(text='Pink 🩷', callback_data='FFC0CB'),
     InlineKeyboardButton(text='White ⚪', callback_data='FFFFFF')],
    [InlineKeyboardButton(text='Atomic swirl', callback_data='Atomic swirl'),
     InlineKeyboardButton(text='Blue mood blobs', callback_data='Blue mood blobs'),
     InlineKeyboardButton(text='Breath', callback_data='Breath')],
    [InlineKeyboardButton(text='Candle', callback_data='Candle'),
     InlineKeyboardButton(text='Cinema brighten lights', callback_data='Cinema brighten lights'),
     InlineKeyboardButton(text='Cinema dim lights', callback_data='Cinema dim lights')],
    [InlineKeyboardButton(text='Cold mood blobs', callback_data='Cold mood blobs'),
     InlineKeyboardButton(text='Collision', callback_data='Collision'),
     InlineKeyboardButton(text='Color traces', callback_data='Color traces')],
    [InlineKeyboardButton(text='Double swirl', callback_data='Double swirl'),
     InlineKeyboardButton(text='Fire', callback_data='Fire'),
     InlineKeyboardButton(text='Flags Germany/Sweden', callback_data='Flags Germany/Sweden')],
    [InlineKeyboardButton(text='Full color mood blobs', callback_data='Full color mood blobs'),
     InlineKeyboardButton(text='Green mood blobs', callback_data='Green mood blobs'),
     InlineKeyboardButton(text='Knight rider', callback_data='Knight rider')],
    [InlineKeyboardButton(text='Led Test', callback_data='Led Test'),
     InlineKeyboardButton(text='Led Test - Sequence', callback_data='Led Test - Sequence'),
     InlineKeyboardButton(text='Light clock', callback_data='Light clock')],
    [InlineKeyboardButton(text='Lights', callback_data='Lights'),
     InlineKeyboardButton(text='Matrix', callback_data='Matrix'),
     InlineKeyboardButton(text='Notify blue', callback_data='Notify blue')],
    [InlineKeyboardButton(text='Pac-Man', callback_data='Pac-Man'),
     InlineKeyboardButton(text='Plasma', callback_data='Plasma'),
     InlineKeyboardButton(text='Police Lights Single', callback_data='Police Lights Single')],
    [InlineKeyboardButton(text='Police Lights Solid', callback_data='Police Lights Solid'),
     InlineKeyboardButton(text='Rainbow mood', callback_data='Rainbow mood'),
     InlineKeyboardButton(text='Rainbow swirl', callback_data='Rainbow swirl')],
    [InlineKeyboardButton(text='Rainbow swirl fast', callback_data='Rainbow swirl fast'),
     InlineKeyboardButton(text='Random', callback_data='Random'),
     InlineKeyboardButton(text='Red mood blobs', callback_data='Red mood blobs')],
    [InlineKeyboardButton(text='Sea waves', callback_data='Sea waves'),
     InlineKeyboardButton(text='Snake', callback_data='Snake'),
     InlineKeyboardButton(text='Sparks', callback_data='Sparks')],
    [InlineKeyboardButton(text='Strobe red', callback_data='Strobe red'),
     InlineKeyboardButton(text='Strobe white', callback_data='Strobe white'),
     InlineKeyboardButton(text='System Shutdown', callback_data='System Shutdown')],
    [InlineKeyboardButton(text='Trails', callback_data='Trails'),
     InlineKeyboardButton(text='Trails color', callback_data='Trails color'),
     InlineKeyboardButton(text='Warm mood blobs', callback_data='Warm mood blobs')],
    [InlineKeyboardButton(text='Waves with Color', callback_data='Waves with Color'),
     InlineKeyboardButton(text='X-Mas', callback_data='X-Mas')]
]

color_effect_keyboard = InlineKeyboardMarkup(inline_keyboard=color_effect_button)

# Start Telegram bot
script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)

chat_id_key = secrets['id']

bot = telepot.Bot(secrets['token'])
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('Im listening...')
bot.sendMessage(chat_id_key, 'Hello World 👋🏽', reply_markup=main_keyboard)

while 1:
    # For Linux (Raspberry)
    if os_name == 'Linux':
        # Temperature control
        cpu = CPUTemperature()
        temperature = cpu.temperature
        if temperature >= 85:
            bot.sendMessage(chat_id_key, f'WARNING ! CPU temperature too hot{temperature}')
        if temperature >= 90:
            bot.sendMessage(chat_id_key,
                            f'WARNING ! CPU temperature too hot{temperature}.\nShutdown in progress... See U soon')
            os.system('sudo shutdown now')

        # Auto update
        now = datetime.now()
        hour = now.strftime("%H:%M")
        date = now.strftime("%d")
        day = now.weekday()

        # Quick update every monday @ 2:30
        if day == 0 and hour == '02:30':
            bot.sendMessage(chat_id_key, 'Starting weekly update...')
            os.system('sudo apt-get update -y')
            bot.sendMessage(chat_id_key, 'Weekly update done.\nStarting weekly upgrade...')
            os.system('sudo apt-get upgrade -y')
            bot.sendMessage(chat_id_key, 'Weekly upgrade done')

        # Update every 1st of month @ 2:00
        if date == '1' and hour == '02:00':
            bot.sendMessage(chat_id_key, 'Starting monthly update...')
            os.system('sudo apt-get update -y')
            bot.sendMessage(chat_id_key, 'Monthly update done.\nStarting monthly upgrade...')
            os.system('sudo apt-get upgrade -y')
            bot.sendMessage(chat_id_key, 'Monthly upgrade done.\nStarting monthly autoremove...')
            os.system('sudo apt-get autoremove -y')
            bot.sendMessage(chat_id_key, 'Monthly autoremove done.\nStarting reboot...\nSee U soon')

    time.sleep(10)
