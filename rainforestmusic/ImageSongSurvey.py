"""
ImageSongSurvey
"""
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
PHASE_LEN = 15
MIN_SONG_DURATION_MS = 6000
RICK_ROLL_THRESHOLD = 100


# extract the genre information from the genres json
with open('spotify_genres.json', 'r') as genre_file:
    GENRE_LIST = json.load(genre_file)

# create the instance of spotify control class
SpotifySurvey = SpotifyTools(USERNAME, CLIENT_ID, CLIENT_SECRET, REDIRECT, DEVICE_ID, GENRE_LIST)

SpotifySurvey.gen_use_tokens()
feature_dict = 0

audio_dict = {'uri' : [], 
              'name': [],
              'artist':[],
              'genre': [],
              'danceability' : [],
              'energy' : [],
              'speechiness' : [],
              'acousticness' : [],
              'instrumentalness' : [],
              'liveness' : [],
              'valence' : []}

# display photo that the songs are being chosen for
# print('Displaying Photo {}'.format(photo))
# search random songs with appropriate filters
for round in range(0,20):
    print('Finding songs for round {}...'.format(round+1))
    name_1, artist_1, uri_1, genre_1, duration_1 = SpotifySurvey.find_random_song(30000, 1000)
    name_2, artist_2, uri_2, genre_2, duration_2 = SpotifySurvey.find_random_song(30000, 1000)
    name_3, artist_3, uri_3, genre_3, duration_3 = SpotifySurvey.find_random_song(30000, 1000)
    name_4, artist_4, uri_4, genre_4, duration_4 = SpotifySurvey.find_random_song(30000, 1000)
    name_5, artist_5, uri_5, genre_5, duration_5 = SpotifySurvey.find_random_song(30000, 1000)
    name_6, artist_6, uri_6, genre_6, duration_6 = SpotifySurvey.find_random_song(30000, 1000)
    name_7, artist_7, uri_7, genre_7, duration_7 = SpotifySurvey.find_random_song(30000, 1000)
    name_8, artist_8, uri_8, genre_8, duration_8 = SpotifySurvey.find_random_song(30000, 1000)
    
    print('Songs found!')

    print("playing song 1:")
    SpotifySurvey.play_song_segment(uri_1, name_1, artist_1, duration_1)
    print("playing song 2:")
    SpotifySurvey.play_song_segment(uri_2, name_2, artist_2, duration_2)
    print("playing song 3:")
    SpotifySurvey.play_song_segment(uri_3, name_3, artist_3, duration_3)
    print("playing song 4:")
    SpotifySurvey.play_song_segment(uri_4, name_4, artist_4, duration_4)
    print("playing song 5:")
    SpotifySurvey.play_song_segment(uri_5, name_5, artist_5, duration_5)
    print("playing song 6:")
    SpotifySurvey.play_song_segment(uri_6, name_6, artist_6, duration_6)
    print("playing song 7:")
    SpotifySurvey.play_song_segment(uri_7, name_7, artist_7, duration_7)
    print("playing song 8:")
    SpotifySurvey.play_song_segment(uri_8, name_8, artist_8, duration_8)

    songs = [uri_1, uri_2, uri_3, uri_4, uri_5, uri_6, uri_7, uri_8]
    names = [name_1, name_2, name_3, name_4, name_5, name_6, name_7, name_8]
    artists = [artist_1, artist_2, artist_3, artist_4, artist_5, artist_6, artist_7, artist_8]
    genres = [genre_1, genre_2, genre_3, genre_4, genre_5, genre_6, genre_7, genre_8]

    # get the user to choose which song matches the image
    chosen_song = input("which song matches the photo best? (1,2,3,4,5,6,7,8)")
    chosen_song = int(chosen_song)

    # extract the audio features from the chosen song
    feature_dict = SpotifySurvey.get_audio_features(songs[chosen_song-1])
    
    # add the information to the dictionary
    audio_dict['uri'].append(songs[chosen_song-1])
    audio_dict['name'].append(names[chosen_song-1])
    audio_dict['artist'].append(artists[chosen_song-1])
    audio_dict['genre'].append(genres[chosen_song-1])
    audio_dict['danceability'].append(feature_dict['danceability'])
    audio_dict['energy'].append(feature_dict['energy'])
    audio_dict['speechiness'].append(feature_dict['speechiness'])
    audio_dict['acousticness'].append(feature_dict['acousticness'])
    audio_dict['instrumentalness'].append(feature_dict['instrumentalness'])
    audio_dict['liveness'].append(feature_dict['liveness'])
    audio_dict['valence'].append(feature_dict['valence'])
    
# export the data to an object 
audio_df = pd.DataFrame(data=audio_dict)
audio_df.to_csv('photo_3_songs.csv')

# if it's the last loop, save to the dictionary/write to csv
# if not the last loop, use audio features to filter the next search

