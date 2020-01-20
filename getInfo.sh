#!/bin/bash
dir=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
if [ "$1" = status ]; then
  dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'PlaybackStatus' | tail -n1 | cut -d'"' -f2
elif [ "$1" = artist ]; then
  dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata' | awk -f ${dir}/spotify_artist.awk | cut -d':' -f2
elif [ "$1" = song ]; then
  dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata' | awk -f ${dir}/spotify_song.awk | cut -d':' -f2
elif [ "$1" = album ]; then
  dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata' | awk -f ${dir}/spotify_album.awk | cut -d':' -f2
else
  echo "No argument specified to the script who gets info from Spotify. Try using 'status', 'artist' or 'song'."
fi
