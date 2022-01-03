#!/usr/bin/env sh

selection="$(jq -r '.[] | "\(.name) - \(.artist) - \(.id)"' ~/workspace/spotify_scripts/tracks.json | rofi -dmenu -p track -i -multi-select)"
[ -z "$selection" ] && exit
echo "$selection" | rev | cut -d ' ' -f1 | rev | tr '\n' ' ' | xargs ~/workspace/spotify_scripts/play_tracks.py
