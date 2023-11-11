#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import time
from datetime import datetime

import telepot
from gpiozero import CPUTemperature
from telepot.loop import MessageLoop


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    if chat_id == chat_id_key:
        
        # Useful commands for Raspberry
        if command == '/temperature':
            bot.sendMessage(chat_id_key, f'{str(temperature)} °C')
            
        if command == '/empty_trash':
            os.system('sudo trash-empty')
            os.system('trash-empty')
            bot.sendMessage(chat_id_key, 'Done')

        if command == '/quick_update':
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

        if command == '/reboot':
            bot.sendMessage(chat_id_key, 'See U soon')
            os.system('sudo reboot now')
        
        if command == '/shutdown':
            bot.sendMessage(chat_id_key, 'Seen U soon')
            os.system('sudo shutdown now')

        # Commands for Hyperion
        if command == '/hyperion_on':
            os.system('hyperion-remote --on')
            os.system('hyperion-remote --clearall')
            os.system('hyperion-remote -E V4L')
            bot.sendMessage(chat_id_key, "Ambilight ON")

        if command == '/hyperion_off':
            os.system('hyperion-remote --off')
            bot.sendMessage(chat_id_key, "Ambilight OFF")
            
        if command == '/video_on':
            os.system('hyperion-remote --clearall')
            os.system('hyperion-remote -E V4L')
            bot.sendMessage(chat_id_key, "Video ON")

        if command == '/video_off':
            os.system('hyperion-remote --clearall')
            os.system('hyperion-remote -D V4L')
            bot.sendMessage(chat_id_key, "Video OFF")

        if command == '/b100':
            os.system('hyperion-remote -L 100')
            bot.sendMessage(chat_id_key, "Brightness 100%")

        if command == '/b75':
            os.system('hyperion-remote -L 75')
            bot.sendMessage(chat_id_key, "Brightness 75%")

        if command == '/b50':
            os.system('hyperion-remote -L 50')
            bot.sendMessage(chat_id_key, "Brightness 50%")

        if command == '/b25':
            os.system('hyperion-remote -L 25')
            bot.sendMessage(chat_id_key, "Brightness 25%")
            
        # Commands for Telegram bot
        if command == '/test':
            bot.sendMessage(chat_id_key, "I'm running :)")

        if command == '/restart_telegram_bot':
            bot.sendMessage(chat_id_key, "Restarting script...")
            sys.stdout.flush()
            time.sleep(2.5)
            os.execv(sys.argv[0], sys.argv)
            
        if command == '/help':
            bot.sendMessage(chat_id_key,
                            "/temperature - Get CPU temperature\n"
                            "/empty_trash - As expected\n"
                            "/quick_update - To update and upgrade without autoremove and reboot\n"
                            "/update - To update, upgrade, autoremove AND REBOOT\n"
                            "/reboot - Sometimes it's good\n"
                            "/shutdown - As excepted\n"
                            "/hyperion_on - Turn on Hyperion\n"
                            "/hyperion_off - Turn off Hyperion\n"
                            "/video_on - Hyperion based on video input\n"
                            "/video_off - Hyperion background effect/color\n"
                            "/b100 - Brightness 100%\n"
                            "/b75 - Brightness 75%\n"
                            "/b50 - Brightness 50%\n"
                            "/b25 - Brightness 25%\n"
                            "/test - Is my Telegram bot still works ?"
                            "/restart_telegram_bot - As excepted\n"
                            "/help - A little reminder")

        elif command not in command_list:
            bot.sendMessage(chat_id_key, "I don't understand... Try /help")
    
    # For unknown ID connection
    else:
        # Send to unknown ID (not allowed to talk with your bot)
        message_to_unknown_id = f'You are not allowed, your ID is {chat_id}'
        bot.sendMessage(chat_id, message_to_unknown_id)
        
        # Send to you to warn you about unknown ID wants to talk with your Telegram Bot
        warning_unknown_id = f'Someone trying to do something strange...\nID: {chat_id}\nMessage: {str(command)}'
        bot.sendMessage(chat_id_key, warning_unknown_id)


command_list = ['/temperature',
                '/quick_update',
                '/update',
                '/empty_trash',
                '/reboot',
                '/test',
                '/restart_telegram_bot',
                '/help',
                '/shutdown',
                '/hyperion_on',
                '/hyperion_off',
                '/b100',
                '/b75',
                '/b50',
                '/b25',
                '/video_on',
                'video_off']

# Start Telegram bot
with open('SECRETS.json', 'r') as secrets_file:
    secrets = json.load(secrets_file)
chat_id_key = secrets['id']
bot = telepot.Bot(secrets['token'])
MessageLoop(bot, handle).run_as_thread()
print('Im listening...')
bot.sendMessage(chat_id_key, 'Hello World 👋🏽')

while 1:
    # Temperature control
    cpu = CPUTemperature()
    temperature = cpu.temperature
    if temperature >= 65:
        bot.sendMessage(chat_id_key, f'WARNING ! CPU temperature too hot{temperature}')
    if temperature >= 85:
        bot.sendMessage(chat_id_key, f'WARNING ! CPU temperature too hot{temperature}.\nShutdown in progress... See U soon')
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
