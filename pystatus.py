#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

if sys.version_info[0] == 2:
    sys.stderr.write('please use python3\n')
    sys.exit(1)

dir_path=os.path.dirname(os.path.realpath(__file__))

# Spotify Song Status
# EDIT ME IF YOU USE A DIFFERENT SPOTIFY CLIENT
spotify_client = 'spotifyd'
player = 'org.mpris.MediaPlayer2.Player'

def connect_dbus():
    global interface
    bus = dbus.SessionBus()
    try:
        proxy = bus.get_object(f'org.mpris.MediaPlayer2.{spotify_client}','/org/mpris/MediaPlayer2')
    except dbus.exceptions.DBusException:
        print(f"[ERROR] Player {spotify_client} doesn't exist or isn't playing")
        return False
    interface = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')
    return True


def get_status():
    status = interface.GetAll(player)
    playback = str(status['PlaybackStatus'])
    return playback


def get_playing():
    status = interface.GetAll(player)
    meta = status['Metadata']
    artist = str(meta['xesam:artist'][0])
    song = str(meta['xesam:title'])
    return artist, song


##### Network speed
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def update_rate(interface=None):
    global last_time, last_rx, last_tx
    current_time = time.time()
    rx = 0
    tx = 0
    if interface:
        ifaces = [interface]
    else:
        # parse interfaces
        valid_iface = re.compile(r'^(eno|enp|ens|enx|eth|wlan|wlp)')
        ifaces = [iface.name for iface in Path('/sys/class/net').glob('*') if valid_iface.match(iface.name)]

    for iface in ifaces:
        tmp_rx = int(open(f'/sys/class/net/{iface}/statistics/rx_bytes','r').read())
        tmp_tx = int(open(f'/sys/class/net/{iface}/statistics/tx_bytes','r').read())
        rx+=tmp_rx
        tx+=tmp_tx
        
    try:
        interval = current_time - last_time
    except NameError:
        interval = 0
        
    if interval > 0:
        rate_rx = (rx - last_rx) / interval
        rate_tx = (tx - last_tx) / interval
        rate = f' {sizeof_fmt(rate_rx)}↓ {sizeof_fmt(rate_tx)}↑'
    else:
        rate = ''
        
    last_time = current_time
    last_rx = rx
    last_tx = tx
    
    return rate


def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()


def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()


if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','
        j = json.loads(line)
        
        # always insert the rate into the network
        for status in j:
            if status['name'] == 'ethernet':
                # pick the interface configured in i3status
                iface = status['instance']
                status['full_text'] = f'{j[0]["full_text"]}{update_rate(iface)}'
        
        # check if dbus object is available
        if not connect_dbus():
            print_line(prefix+json.dumps(j))
        if get_status() in ['Playing']:
            # insert information into the start of the json, but could be anywhere
            # CHANGE THIS LINE TO INSERT SOMETHING ELSE
            artist, song = get_playing()
            j.insert(0, {'color' : '#9ec600', 'full_text' : f' {artist} - {song}', 'name' : 'spotify', 'markup': 'none'})
            # and echo back new encoded json
            print_line(prefix+json.dumps(j))
        else:
            j.insert(0, {'color' : '#9ec600', 'full_text' : f' {get_status()}', 'name' : 'spotify', 'markup': 'none'})
            print_line(prefix+json.dumps(j))
