import tkinter as tk

import os.path

settings =  {
                'main_window_geometry': '1280x720+100+100',
                'view_window_geometry': '1000x600+0+0'
            }

def load():
    if os.path.isfile('settings.conf'):
        with open('settings.conf', 'r') as conf:
            for line in conf.read().splitlines():
                parts = line.strip().split('=', 1)
                if parts[0] in settings:
                    settings[parts[0]] = parts[1]

def save():
    with open('settings.conf', 'w') as conf:
        for key, value in settings.items():
            conf.write('{}={}\n'.format(key, value))

def get(name):
    return settings.get(name)

def set(name, value):
    settings[name] = value
