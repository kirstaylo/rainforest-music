"""
BuildPlaylistFromImage
"""

# use the average values for audio characteristics from the existing data

# search but include target audio features in the search query

# user_playlist_create to create a new playlist

# set the playlist photo to be the photo it was chosen for

import json
import time
from dotenv import dotenv_values
import pandas as pd
from SpotifyTools import SpotifyTools

# load in secret environmental variables from .env file
config = dotenv_values(".env")

# extract the environmental variables to instantiate the class with
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
USERNAME = config['USERNAME']
DEVICE_ID = config['DEVICE_ID']

REDIRECT = "http://localhost:3000/callback/"


# extract the genre information from the genres json
with open('spotify_genres.json', 'r') as genre_file:
    GENRE_LIST = json.load(genre_file)

# create the instance of spotify control class
SpotifySurvey = SpotifyTools(USERNAME, CLIENT_ID, CLIENT_SECRET, REDIRECT, DEVICE_ID, GENRE_LIST)

SpotifySurvey.gen_use_tokens()

import requests

endpoint_url = "https://api.spotify.com/v1/recommendations?"

# OUR FILTERS
limit=100
market="US"
seed_genres="acoustic"
target_danceability=0.2
target_energy=0.13
target_speechiness=0.01
target_acousticness=0.91
target_instrumentalness=0.9
target_liveness=0.1
target_valence=0.06
target_popularity=1

query = f'{endpoint_url}limit={limit}&target_danceability={target_danceability}'
query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}&target_energy={target_energy}&target_speechiness={target_speechiness}&target_acousticness={target_acousticness}&target_instrumentalness={target_instrumentalness}&target_liveness={target_liveness}&target_valence={target_valence}&target_popularity={target_popularity}'


response=requests.get(query, 
               headers={"Content-Type":"application/json", 
                        "Authorization":"Bearer BQBwfOTpudBUbSRHxR-Uyz5tnxr-CDBLeBMgffY_mx5bXZf4UlyhPSyQDmnqc8yXkCwq10FMnA2AWHdlj-iDhBOsfEGQ39Zkx1kAefcDn7TeWxzsF9DbPt7TlDibU-Rn64cbhpkJuHXk"})

json_response = response.json()
print(response)

uris = []
for i in json_response['tracks']:
            uris.append(i['uri'])
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
           
# playlist = SpotifySurvey.pmp.user_playlist_create('ktay1234', 'Rainforest Tunes', public=True, collaborative=False, description='')

# SpotifySurvey.pmp.user_playlist_add_tracks('ktay1234', playlist["id"], uris, position=None)

