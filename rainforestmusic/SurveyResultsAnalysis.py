"""
SurveyResultsAnalysis
"""
import pandas as pd


# load in the song data for the different images
photo_1 = pd.read_csv('photo_1_songs.csv')
photo_2 = pd.read_csv('photo_2_songs.csv')
# photo_3 = pd.read_csv('photo_3_songs.csv')
# photo_4 = pd.read_csv('photo_4_songs.csv')
# photo_5 = pd.read_csv('photo_5_songs.csv')

print(photo_1.head())

# extract the different mean results and standard deviations
# means_1 = photo_1.mean()
# stds_1 = photo_1.std()

# means_2 = photo_2.mean()
# stds_2 = photo_2.std()

# means_3 = photo_3.mean()
# stds_3 = photo_3.std()

# means_4 = photo_4.mean()
# stds_4 = photo_4.std()

# means_5 = photo_5.mean()
# stds_5 = photo_5.std()