"""
ImageSongSurvey
"""
import json
import time
import csv
from dotenv import dotenv_values
from SpotifyTools import SpotifyTools
import pandas as pd
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

midi_songs = pd.read_csv('midi_songs.csv')

audio_dict = {'uri' : [], 
              'track' : [],
              'artist' : [],
              'danceability' : [],
              'energy' : [],
              'key' : [],
              'loudness' : [],
              'mode' : [],
              'speechiness' : [],
              'acousticness' : [],
              'instrumentalness' : [],
              'liveness' : [],
              'valence' : [],
              'tempo' : [], 
              'time_signature' : []}

num_songs = midi_songs.shape[0]

def create_csv():
    with open('midi_uris.csv', 'w', newline='') as f:
        # create the csv writer
        writer = csv.DictWriter(f, fieldnames=["track", "artist", "uri"])
        writer.writeheader()

def append_to_csv(track, artist, uri):
    # open the file in the write mode
    with open('midi_uris.csv', 'a', newline='') as f:
        # create the csv writer
        writer = csv.DictWriter(f, fieldnames=["track", "artist", "uri"])
        writer.writerow({"track":track, "artist":artist, "uri": uri})

input("HAVE YOU CHECKED YOU ARE NOT OVERWRITING THE CSV?")
# print('creating csv')
# create_csv()
for i in range(23303, num_songs):
    time.sleep(0.1)
    track = midi_songs['Songs'].iloc[i]
    artist = midi_songs['Artists'].iloc[i]
    print('processing song {}/{}, {} by {}'.format(i, num_songs, track, artist))
    try: 
        result = SpotifySurvey.urcp.search(q='track:{} artist:{}'.format(track, artist), type='track', limit=1)
        uri = result['tracks']['items'][0]['uri']
        append_to_csv(track, artist, uri)
        # audio_dict["uri"].append(uri)
        # audio_dict["track"].append(track)
        # audio_dict["artist"].append(artist)
        '''audio_features = SpotifySurvey.get_audio_features(uri)
        for key, val in audio_features.items():
            audio_dict[key].append(val)'''
    except IndexError:
        print("spotify cannot find this file")
        continue
    except UnicodeEncodeError:
        print("unicode cannot write filename into csv")
        continue
    except Exception as e:
        print(e)
        break
        
# audio_df = pd.DataFrame(data=audio_dict)
# audio_df.to_csv('midi_song_audio_features.csv')
# print('exported csv')

print('Non-index error broke at {}, continue csv from where it was left'.format(i))
print('exported csv')