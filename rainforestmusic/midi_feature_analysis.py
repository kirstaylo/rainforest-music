"""
midi feature analysis
"""
import pandas as pd
import numpy as np

midi_audio_features = pd.read_csv('midi_features.csv')

# not speechiness as this is not included in midi files
target_danceability = 0.088260
target_energy = 0.201003
target_acousticness = 0.209396
target_instrumentalness = 0.320842
target_liveness = 0.210592
target_valence = 0.028271

# calculate score based off accumulated squared differences from the target value
scores = []

for row in range(midi_audio_features.shape[0]):
    print('calculating score for row {}/{}'.format(row, midi_audio_features.shape[0]))
    score = 0
    score += (midi_audio_features['danceability'].iloc[row] - target_danceability)**2
    score += (midi_audio_features['energy'].iloc[row] - target_energy)**2
    score += (midi_audio_features['acousticness'].iloc[row] - target_acousticness)**2
    score += (midi_audio_features['instrumentalness'].iloc[row] - target_instrumentalness)**2
    score += (midi_audio_features['liveness'].iloc[row] - target_liveness)**2
    score += (midi_audio_features['valence'].iloc[row] - target_valence)**2
    scores.append(score)
    
# add the scores list to the dataframe
midi_audio_features['scores'] = scores

print('sorting data')
# sort the dataframe by the scores, with the lowest scores at the top
sorted_midi = midi_audio_features.sort_values(by=['scores'], ascending=True)

# grab the first 1200 datapoints
cropped_audio_features = sorted_midi.iloc[:1200]

# export the cropped csv
cropped_audio_features.to_csv('chosen_midi_songs.csv')
print('exported csv')