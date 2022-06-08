"""
SpotifyTools
"""

import os
import csv
import time
import random as r
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyTools():
    def __init__(self, username, client_id, client_secret, redirect, device_id, genre_list):
        # assign global variables from init parameters
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect = redirect
        self.device_id = device_id
        self.genre_list = genre_list
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        
    ''' factory method to generate tokens for specific scopes '''
    def create_token(self, scope):
        token = util.prompt_for_user_token(self.username, scope, self.client_id, self.client_secret, self.redirect)
        sp = spotipy.Spotify(auth=token)
        return sp
    
    
    ''' method to generate specific tokens for the main scopes being used '''
    def gen_use_tokens(self):
        # create user read currently playing token
        self.urcp = self.create_token('user-read-currently-playing')
        # create user read playback state token
        self.urps = self.create_token('user-read-playback-state')
        # create user modify playback state token
        self.urms = self.create_token('user-modify-playback-state')
        # create user modify playback state token
        self.pmp = self.create_token('playlist-modify-public')


    ''' method to check that music is being played on the correct device at same volume '''
    def check_device(self):
        device_info = self.urps.devices()
        print(device_info)
        # iterate through devices to find the active one
        for device in device_info['devices']:
            if device['is_active']:
                # check that the music is playing from the correct device
                if device['id'] != self.device_id:
                    print('incorrect device connected')
                # check that the music is at full volume (or change it to full volume)
                if device['volume_percent'] != 100:
                    print('correcting volume')
                    self.urms.volume(100, device_id=self.device_id)
                    
    ''' function to play a song '''
    def play_song(self, uri):
        self.urms.start_playback(uris=[uri])
        
    
    ''' get audio features of a song '''
    def get_audio_features(self, uri):
        # extract the song's audio features
        audio_features = self.urcp.audio_features(uri)
        feature_dict = {}
        
        # add the audio feature info to the song dictionary
        feature_dict['danceability'] = audio_features[0]['danceability']
        feature_dict['energy'] = audio_features[0]['energy']
        feature_dict['key'] = audio_features[0]['key']
        feature_dict['loudness'] = audio_features[0]['loudness']
        feature_dict['mode'] = audio_features[0]['mode']
        feature_dict['speechiness'] = audio_features[0]['speechiness']
        feature_dict['acousticness'] = audio_features[0]['acousticness']
        feature_dict['instrumentalness'] = audio_features[0]['instrumentalness']
        feature_dict['liveness'] = audio_features[0]['liveness']
        feature_dict['valence'] = audio_features[0]['valence']
        feature_dict['tempo'] = audio_features[0]['tempo']
        feature_dict['time_signature'] = audio_features[0]['time_signature']
        return feature_dict
    
    ''' get audio features of a song '''
    def get_many_audio_features(self, uri_batch, track_batch, artist_batch):
        # extract the song's audio features
        audio_features = self.urcp.audio_features(uri_batch)
        feature_dict_list = []
        
        for i in range(len(audio_features)):
            try: 
                feature_dict = {}
                # add the audio feature info to the song dictionary
                feature_dict['track'] = track_batch[i]
                feature_dict['artist'] = artist_batch[i]
                feature_dict['uri'] = uri_batch[i]
                feature_dict['danceability'] = audio_features[i]['danceability']
                feature_dict['energy'] = audio_features[i]['energy']
                feature_dict['key'] = audio_features[i]['key']
                feature_dict['loudness'] = audio_features[i]['loudness']
                feature_dict['mode'] = audio_features[i]['mode']
                feature_dict['speechiness'] = audio_features[i]['speechiness']
                feature_dict['acousticness'] = audio_features[i]['acousticness']
                feature_dict['instrumentalness'] = audio_features[i]['instrumentalness']
                feature_dict['liveness'] = audio_features[i]['liveness']
                feature_dict['valence'] = audio_features[i]['valence']
                feature_dict['tempo'] = audio_features[i]['tempo']
                feature_dict['time_signature'] = audio_features[i]['time_signature']
                feature_dict_list.append(feature_dict)
            except: continue
        return feature_dict_list
                    
                              
    ''' method to check the session id and instantiate csv for data collection '''
    def init_collection_session(self):
        # find which listening session this is
        self.session_id = len(os.listdir('./spotify_data')) + 1

        # open the file in the write mode
        with open('./spotify_data/song_data_session_{}.csv'.format(self.session_id), 'w', newline='') as f:
            # create the csv writer
            writer = csv.DictWriter(f, fieldnames=list(self.song_dict.keys()))
            writer.writeheader()

    ''' method to apply a filter to the audio features being searched for '''
    def apply_search_filter(self, loop_no, features, features_found):
        range_size = [0.25, 0.125, 0.0625] # for loops 2,3,4
        loop_no = loop_no-2
        
        # build the max min ranges for each feature
        danceability = features['danceability']
        danceability_range = [danceability+range_size[loop_no], danceability-range_size[loop_no]]
        
        energy = features['energy']
        energy_range = [energy+range_size[loop_no], energy-range_size[loop_no]]
        
        speechiness = features['speechiness']
        speechiness_range = [speechiness+range_size[loop_no], speechiness-range_size[loop_no]]
        
        acousticness = features['acousticness']
        acousticness_range = [acousticness+range_size[loop_no], acousticness-range_size[loop_no]]
        
        instrumentalness = features['instrumentalness']
        instrumentalness_range = [instrumentalness+range_size[loop_no], instrumentalness-range_size[loop_no]]
        
        liveness = features['liveness']
        liveness_range = [liveness+range_size[loop_no], liveness-range_size[loop_no]]
        
        valence = features['valence']
        valence_range = [valence+range_size[loop_no], valence-range_size[loop_no]]
        
        # compare to the found_features, only return true if it fits in criteria
        if features_found['danceability'] > danceability_range[0] or features_found['danceability'] < danceability_range[1]:
            return False
        
        elif features_found['energy'] > energy_range[0] or features_found['energy'] < energy_range[1]:
            return False
        
        elif features_found['speechiness'] > speechiness_range[0] or features_found['speechiness'] < speechiness_range[1]:
            return False
        
        elif features_found['acousticness'] > acousticness_range[0] or features_found['acousticness'] < acousticness_range[1]:
            return False
        
        elif features_found['instrumentalness'] > instrumentalness_range[0] or features_found['instrumentalness'] < instrumentalness_range[1]:
            return False
        
        elif features_found['liveness'] > liveness_range[0] or features_found['liveness'] < liveness_range[1]:
            return False
        
        elif features_found['valence'] > valence_range[0] or features_found['valence'] < valence_range[1]:
            return False
        
        elif features_found['danceability'] > danceability_range[0] or features_found['danceability'] < danceability_range[1]:
            return False
        
        else:
            return True
        

    ''' method to choose random song from spotify'''
    def find_random_song(self, min_song_duration, rick_roll_threshold):
        found_song = False
        search_count = 0
        
        # repeat loop until a valid song is found
        while not found_song:
            # create list of vowels
            vowels = ['a', 'e', 'i', 'o', 'u']
            # choose random vowel, genre and offset for search query
            vowel = r.choice(vowels)
            genre = r.choice(self.genre_list)
            o = r.randint(0,5)
            
            # search spotify with the randomised query
            results = self.urcp.search(q='track:{} genre:{}'.format(vowel, genre), type='track', limit=1, offset=o)
            try: 
                # extract the song data
                # this will throw an error if nothing is found
                rand_name = results['tracks']['items'][0]['name']
                rand_artist = results['tracks']['items'][0]['artists'][0]['name']
                rand_uri = results['tracks']['items'][0]['uri']
                
                # find the song duration
                duration = results['tracks']['items'][0]['duration_ms']
                # if the song is too short, throw an error
                if duration < min_song_duration:
                    raise IndexError
                
                # break out of the search loop
                found_song = True
               
            # if no song is found
            except:
                # try again with new search query
                search_count +=1
                # if it is taking more than the rick roll threshold to find a random song, get Rick Rolled
                if search_count > rick_roll_threshold:
                    print('playing Never Gonna Give You Up by Rick Astley')
                    self.urms.start_playback(uris=['spotify:track:4cOdK2wGLETKBW3PvgPWqT'])
                    
        return rand_name, rand_artist, rand_uri, genre, duration
        
    ''' method to play a segment from a song '''
    def play_song_segment(self, uri, name, artist, duration):
        # print the name of the song being played and the song number
        print('playing {} by {}'.format(name, artist))
        # start playing the song from the middle
        self.urms.start_playback(uris=[uri], position_ms=duration/2)
        time.sleep(7)
        # self.urms.pause_playback()
      
        
