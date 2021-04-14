#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
import json
import os
import subprocess
import sys

if sys.version_info[0] == 2:
    sys.stderr.write('please use python3\n')
    sys.exit(1)

dir_path=os.path.dirname(os.path.realpath(__file__))

#Get from the bus
bus = dbus.SessionBus()
# EDIT ME IF YOU USE A DIFFERENT SPOTIFY CLIENT
spotify_client = 'spotifyd'
player = 'org.mpris.MediaPlayer2.Player'
proxy = bus.get_object(f'org.mpris.MediaPlayer2.{spotify_client}','/org/mpris/MediaPlayer2')
interface = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')

def get_status():
    status = interface.GetAll(player)
    playback = str(status['PlaybackStatus'])
    return playback
    #sys.stdout.write(playback)

def get_playing():
    status = interface.GetAll(player)
    meta = status['Metadata']
    artist = str(meta['xesam:artist'][0])
    song = str(meta['xesam:title'])
    return artist, song
    #sys.stdout.write(artist, song)

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
        if get_status() in ['Playing']:
            j = json.loads(line)
            # insert information into the start of the json, but could be anywhere
            # CHANGE THIS LINE TO INSERT SOMETHING ELSE
            artist, song = get_playing()
            j.insert(0, {'color' : '#9ec600', 'full_text' : f' {artist} - {song}', 'name' : 'spotify'})
            # and echo back new encoded json
            print_line(prefix+json.dumps(j))
        else:
            j = json.loads(line)
            print_line(prefix+json.dumps(j))
            #print_line(json.dumps(j))
