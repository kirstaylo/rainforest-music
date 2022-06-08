# -*- coding: utf-8 -*-
"""
download_midi_songs
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time

def check_element_exists(func, text):
    try:
        if func == 'plt':
            driver.find_element_by_partial_link_text(text)
        if func =='id':
            driver.find_element_by_id(text)
    except:
        return False
    return True

driver = webdriver.Chrome('/Users/kirst/chromedriver_win32/chromedriver')

manual_download = {
        'track': [],
        'artist' : []
    }


def download_routine(song_box):
    # find and click the download page link 
    title_div = song_box.find_elements_by_class_name("search-song-title")[0]
    title_href = title_div.find_element_by_tag_name('a')
    title_href.click()
    # wait for page to load
    time.sleep(2.5)
    midi_download = driver.find_element_by_id("downloadmidi")
    midi_download.click()
    
def add_to_manual_download(track, artist):
    manual_download['track'].append(track)
    manual_download['artist'].append(artist)
    
def compare_names(song_boxes, track, artist):
    # compare the names of each found song to the chosen one
    for song_box in song_boxes: 
        title_div = song_box.find_elements_by_class_name("search-song-title")[0]
        title_href = title_div.find_element_by_tag_name('a')
        artist_div = song_box.find_elements_by_class_name("search-song-cat")[0]
        artist_href = artist_div.find_element_by_tag_name('a')
        if title_href.text == track and artist_href.text == artist:
            return song_box
        else:
            continue
    # if nothing is found, add it to the manual download dict
    add_to_manual_download(track, artist)
    return False

# import chosen songs
chosen_songs = pd.read_csv('chosen_midi_songs.csv')

# iterate through songs
for row in range(1002, chosen_songs.shape[0]):
    track = chosen_songs["track"].iloc[row]
    artist = chosen_songs["artist"].iloc[row]
    print('finding download {}/{}, {} by {}'.format(row, chosen_songs.shape[0], track, artist))
    
    try:
        # build search query
        q = track.replace(' ', '+')
        print(q)
        # go to the search page
        driver.get('https://freemidi.org/search?q={}'.format(q))
        # wait for page to load
        time.sleep(2.5)
        # how many results?
        song_boxes = driver.find_elements_by_class_name("search-song-container")
        num_res = len(song_boxes)
        
        # if no results
        if num_res == 0:
            print('no results found')
            add_to_manual_download(track, artist)
            
        # if 1 result
        elif num_res == 1:
            print('one result found')
            song_box = song_boxes[0]
            download_routine(song_box)
            
        # if multiple results
        else:
            print('multiple results found')
            song_box = compare_names(song_boxes, track, artist)
            if song_box:
                download_routine(song_box)
    except Exception as e:
        print(e)
        add_to_manual_download(track, artist)
    
print('creating manual download csv')
manual_download_df = pd.DataFrame(manual_download)
manual_download_df.to_csv('manual_download3.csv')
