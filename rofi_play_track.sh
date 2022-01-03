#!/usr/bin/env sh

selection="$(jq -r '.[] | "\(.name) - \(.artist) - \(.id)"' tracks.json | rofi -dmenu -p track -i)"
id="$(echo $selection | rev | cut -d ' ' -f1 | rev)"
play_track.py $id
