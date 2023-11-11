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
    chat_id_input = msg['chat']['id']
    command = msg['text']
    if chat_id_input == chat_id_key:
        if command == '/temp':
            bot.sendMessage(chat_id_key, f'{str(temperature)} °C')
        if command == '/quick_update':
            weekly_update.on()
            bot.sendMessage(chat_id_key, 'Starting update...')
            os.system('sudo apt-get update -y')
            bot.sendMessage(chat_id_key, 'Update done.\nStarting upgrade...')
            os.system('sudo apt-get upgrade -y')
            bot.sendMessage(chat_id_key, 'Upgrade done')
        if command == '/update':
            weekly_update.on()
            bot.sendMessage(chat_id_key, 'Starting update...')
            os.system('sudo apt-get update -y')
            bot.sendMessage(chat_id_key, 'Update done.\nStarting upgrade...')
            os.system('sudo apt-get upgrade -y')
            bot.sendMessage(chat_id_key, 'Upgrade done.\nStarting autoremove...')
            os.system('sudo apt-get autoremove -y')
            bot.sendMessage(chat_id_key, 'Autoremove done.\nStarting reboot...\nSee U soon')
        if command == '/empty_trash':
            os.system('sudo trash-empty')
            os.system('trash-empty')
            bot.sendMessage(chat_id_key, 'Done')
        if command == '/reboot':
            bot.sendMessage(chat_id_key, 'See U soon')
            os.system('sudo reboot now')
        if command == '/help':
            bot.sendMessage(chat_id_key,
                            "/temp - Get temperature\n/quick_update - To update and upgrade without autoremove and reboot\n/update - To update, upgrade and autoremove AND REBOOT\n/trash_empty - As expected\n/reboot - Sometimes it's good\n/shutdown - As excepted\n/restart_script - As excepted\n/help - A little reminder")
        if command == '/test':
            bot.sendMessage(chat_id_key, 'test')
        if command == '/restart_script':
            bot.sendMessage(chat_id_key, "Restarting script...")
            sys.stdout.flush()
            time.sleep(2.5)
            os.execv(sys.argv[0], sys.argv)
        if command == '/shutdown':
            bot.sendMessage(chat_id_key, 'Seen U soon')
            os.system('sudo shutdown now')
        if command == '/ambilight_on':
            os.system('hyperion-remote --on')
            os.system('hyperion-remote --clearall')
            os.system('hyperion-remote -E V4L')
            bot.sendMessage(chat_id_key, "Ambilight ON")
        if command == '/ambilight_off':
            os.system('hyperion-remote --off')
            bot.sendMessage(chat_id_key, "Ambilight OFF")
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
        if command == '/video_on':
            os.system('hyperion-remote --clearall')
            os.system('hyperion-remote -E V4L')
            bot.sendMessage(chat_id_key, "Video ON")
        if command == '/video_off':
            os.system('hyperion-remote --clearall')
            os.system('hyperion-remote -D V4L')
            bot.sendMessage(chat_id_key, "Video OFF")
        elif command not in command_list:
            bot.sendMessage(chat_id_key, "I don't understand... Try /help")
    else:
        chat_id1 = 'You are not allowed, your ID is '
        chat_id2 = str(chat_id_input)
        chat_id3 = chat_id1 + chat_id2
        chat_id4 = 'Someone trying to do something strange...\nID: '
        chat_id6 = '\nMessage: '
        chat_id7 = str(command)
        chat_id5 = chat_id4 + chat_id2 + chat_id6 + chat_id7
        bot.sendMessage(chat_id_input, chat_id3)
        bot.sendMessage(chat_id_key, chat_id5)


with open('SECRETS.json', 'r') as id_file:
    id_data = json.load(id_file)

chat_id_key = id_data['id']
command_list = ['/temp',
                '/quick_update',
                '/update',
                '/empty_trash',
                '/reboot',
                '/test',
                '/restart_script',
                '/help',
                '/shutdown',
                '/ambilight_off',
                '/ambilight_on',
                '/b100',
                '/b75',
                '/b50',
                '/b25',
                '/video_on',
                'video_off']
update_list = ['02:00', '02:30']

bot = telepot.Bot(id_data['token'])
MessageLoop(bot, handle).run_as_thread()
print('Im listening...')
bot.sendMessage(chat_id_key, 'Hello World 👋🏽')

while 1:
    cpu = CPUTemperature()
    temperature = cpu.temperature
    now = datetime.now()
    hour = now.strftime("%H:%M")
    date = now.strftime("%d")
    day = now.weekday()

    if temperature >= 65:
        bot.sendMessage(chat_id_key, f'WARNING ! CPU temperature too hot{temperature}')
    if day == 0 and hour == '02:30':
        bot.sendMessage(chat_id_key, 'Starting weekly update...')
        os.system('sudo apt-get update -y')
        bot.sendMessage(chat_id_key, 'Weekly update done.\nStarting weekly upgrade...')
        os.system('sudo apt-get upgrade -y')
        bot.sendMessage(chat_id_key, 'Weekly upgrade done')
    if date == '1' and hour == '02:00':
        bot.sendMessage(chat_id_key, 'Starting monthly update...')
        os.system('sudo apt-get update -y')
        bot.sendMessage(chat_id_key, 'Monthly update done.\nStarting monthly upgrade...')
        os.system('sudo apt-get upgrade -y')
        bot.sendMessage(chat_id_key, 'Monthly upgrade done.\nStarting monthly autoremove...')
        os.system('sudo apt-get autoremove -y')
        bot.sendMessage(chat_id_key, 'Monthly autoremove done.\nStarting reboot...\nSee U soon')
    time.sleep(10)
