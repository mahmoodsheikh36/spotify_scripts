#!/usr/bin/env python3
import json
import requests
import sys
import os

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

def play_track(access_token, track_id):
    r = requests.put('https://api.spotify.com/v1/me/player/play',
                     headers={'Authorization': 'Bearer ' + access_token},
                     data=json.dumps({'uris': ['spotify:track:{}'.format(track_id)]}))
    print('spotify:track:{}'.format(track_id))
    print(r.text)

if __name__ == '__main__':
    secrets = load_secrets()
    access_token = fetch_access_token(secrets['client_id'], secrets['client_secret'], secrets['refresh_token'])
    play_track(access_token, sys.argv[1])
