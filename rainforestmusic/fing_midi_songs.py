# -*- coding: utf-8 -*-
"""
find_midi_songs
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
pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
pages = ['w', 'x', 'y', 'z']

song_list = []
artist_list = []

try: 
    for i in pages:
        for j in range(1000):
            website = 'https://freemidi.org/songtitle-{}-{}'.format(i,j)
            print('searching the website: {}'.format(website))
            driver.get(website)
            time.sleep(1)
            song_boxes = driver.find_elements_by_class_name("song-list-container")
    
            for song_box in song_boxes:
                title_div = song_box.find_elements_by_class_name("row-title")[0]
                title_href = title_div.find_element_by_tag_name('a')
                title = title_href.text
                artist_div = song_box.find_elements_by_class_name("row-directory")[0]
                artist_href = artist_div.find_element_by_tag_name('a')
                artist = artist_href.text
                print(j, title, artist)
                if title!='':
                    print('appending')
                    song_list.append(title)
                    artist_list.append(artist)
            if title == '':
                    break
except:            
    midi_dict = {'Songs': song_list, 'Artists': artist_list}
    midi_df = pd.DataFrame(midi_dict)
    midi_df.to_csv('midi_songs2.csv')
    
midi_dict = {'Songs': song_list, 'Artists': artist_list}
midi_df = pd.DataFrame(midi_dict)
midi_df.to_csv('midi_songs2.csv')
