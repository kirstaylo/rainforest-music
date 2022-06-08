"""
ImageSongSurvey
"""
import json
import time
import csv
from dotenv import dotenv_values
from SpotifyTools import SpotifyTools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load in secret environmental variables from .env file
config = dotenv_values(".env")

# extract the environmental variables to instantiate the class with
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
USERNAME = config['USERNAME']
DEVICE_ID = config['DEVICE_ID']

REDIRECT = "http://localhost:3000/callback/"
PHASE_LEN = 15
MIN_SONG_DURATION_MS = 6000
RICK_ROLL_THRESHOLD = 100


# extract the genre information from the genres json
with open('spotify_genres.json', 'r') as genre_file:
    GENRE_LIST = json.load(genre_file)

# create the instance of spotify control class
SpotifySurvey = SpotifyTools(USERNAME, CLIENT_ID, CLIENT_SECRET, REDIRECT, DEVICE_ID, GENRE_LIST)
SpotifySurvey.gen_use_tokens()

def create_csv():
    with open('midi_features.csv', 'w', newline='') as f:
        # create the csv writer
        writer = csv.DictWriter(f, fieldnames=["track", "artist", "uri", 'danceability', 'energy', 'key', 
                                               'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 
                                               'liveness', 'valence', 'tempo', 'time_signature'])
        writer.writeheader()

def append_to_csv(row_dict):
    # open the file in the write mode
    with open('midi_features.csv', 'a', newline='') as f:
        # create the csv writer
        writer = csv.DictWriter(f, fieldnames=["track", "artist", "uri", 'danceability', 'energy', 'key', 
                                               'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 
                                               'liveness', 'valence', 'tempo', 'time_signature'])
        writer.writerow(row_dict)

midi_uris = pd.read_csv('midi_uris.csv')

num_songs = midi_uris.shape[0]

uri_array = np.array(midi_uris['uri'])
track_array = np.array(midi_uris['track'])
artist_array = np.array(midi_uris['artist'])

input("HAVE YOU CHECKED YOU ARE NOT OVERWRITING THE CSV?")
print('creating csv')
create_csv()

batch_no = 1
broken = False
while len(uri_array) > 100:
    print('processing batch {} / {}'.format(batch_no, (num_songs//100)+1))
    # batch 100 uri ids from df
    uri_batch = uri_array[:100]
    track_batch = track_array[:100]
    artist_batch = artist_array[:100]
    
    # find the audio features for the batch
    audio_features = SpotifySurvey.get_many_audio_features(uri_batch, track_batch, artist_batch)
    print('appending found features')
    for feature in audio_features:
        try: 
            append_to_csv(feature)
        except UnicodeError:
            continue
    
    # delete first 100 indexes of array to move batch window
    uri_array = np.delete(uri_array, range(100))
    track_array = np.delete(track_array, range(100))
    artist_array = np.delete(artist_array, range(100))
    batch_no +=1
    
# final loop
if not broken:
    print('processing batch {} / {}'.format(batch_no, (num_songs%100)+1))
    uri_batch = uri_array
    track_batch = track_array
    artist_batch = artist_array
    audio_features = SpotifySurvey.get_many_audio_features(uri_batch, track_batch, artist_batch)
    for feature in audio_features:
        print('appending found features')
        append_to_csv(feature)
