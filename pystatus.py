#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import os

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

dir_path=os.path.dirname(os.path.realpath(__file__))


def get_status():
    spotify_read = subprocess.check_output("%s/getInfo.sh status" % dir_path, shell=True)
    spotify_status=spotify_read.decode('utf-8')
    return spotify_status
    #sys.stdout.write(spotify_status)

def get_artist():
    spotify_read = subprocess.check_output("%s/getInfo.sh artist" % dir_path, shell=True)
    spotify_artist=spotify_read.decode('utf-8')
    return spotify_artist[:-1]
    #sys.stdout.write(spotify_artist)

def get_song():
    spotify_read = subprocess.check_output("%s/getInfo.sh song" % dir_path, shell=True)
    spotify_song=spotify_read.decode('utf-8')
    return spotify_song[:-1]
    #sys.stdout.write(spotify_song)


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

def get_governor():
    with open('/sys/devices/platform/i5k_amb.0/temp4_input') as fp:
        return fp.readlines()[0].strip()



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
        if get_status() in ['Playing\n']:
            j = json.loads(line)
            # insert information into the start of the json, but could be anywhere
            # CHANGE THIS LINE TO INSERT SOMETHING ELSE
            j.insert(0, {'color' : '#9ec600', 'full_text' : ' %s - %s' % (get_artist(), get_song()) , 'name' : 'spotify'})
            # and echo back new encoded json
            print_line(prefix+json.dumps(j))
        else:
            j = json.loads(line)
            print_line(prefix+json.dumps(j))
            #print_line(json.dumps(j))
