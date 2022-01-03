#!/usr/bin/env python3
import json
import os.path
import requests
import base64
import time

def load_secrets():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'secrets.json')) as secrets_file:
        return json.loads(secrets_file.read())

def fetch_access_token(client_id, client_secret, refresh_token):
    r = requests.post('https://accounts.spotify.com/api/token',
                      data = {
                          'grant_type': 'refresh_token',
                          'refresh_token': refresh_token,
                          'client_id': client_id,
                          'client_secret': client_secret,
                      })
    return r.json()['access_token']

def fetch_library(access_token, tracks, url="https://api.spotify.com/v1/me/tracks?limit=50"):
    r = requests.get(url, headers={'Authorization': 'Bearer ' + access_token})
    if r.status_code != 200:
        time.sleep(1)
        fetch_library(access_token, tracks, url)
        return
    r_data = r.json()
    for item in r_data['items']:
        track = item['track']
        data = {
            'id': track['id'],
            'name': track['name'],
            'images': track['album']['images'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name']
        }
        tracks.append(data)
        print(data['name'])
    if 'next' in r_data and r_data['next']:
        fetch_library(access_token, tracks, url=r_data['next'])

if __name__ == '__main__':
    secrets = load_secrets()
    access_token = fetch_access_token(secrets['client_id'], secrets['client_secret'], secrets['refresh_token'])

    track_list = []
    fetch_library(access_token, track_list)
    with open('tracks.json', 'w+') as tracks_file:
        tracks_file.write(json.dumps(track_list, indent=2))
