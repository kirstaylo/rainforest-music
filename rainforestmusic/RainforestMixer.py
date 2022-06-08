"""
MusicMixer
"""

import pygame
from tkinter import *
 
def play():
    pygame.mixer.music.load('woods_spirit.wav')
    pygame.mixer.music.play()
 
def pause():
    pygame.mixer.music.pause()
 
def unpause():
    pygame.mixer.music.unpause()
 
def sound():
    pygame.mixer.Sound.play(sound_effect)
    
def song():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.load('rainforest_sounds/woods_spirit.mp3')
        pygame.mixer.music.play()

def wind():
    # pygame.mixer.music.load('rainforest_sounds/forest_wind.wav')
    # pygame.mixer.music.play()
    insects = pygame.mixer.Sound('rainforest_sounds/forest_wind.wav') 
    pygame.mixer.Sound.play(insects)
    
def rain():
    # pygame.mixer.music.load('rainforest_sounds/forest_rain.wav')
    # pygame.mixer.music.play()
    insects = pygame.mixer.Sound('rainforest_sounds/forest_rain.wav') 
    pygame.mixer.Sound.play(insects)
    
def birds():
    # pygame.mixer.music.load('rainforest_sounds/bird_tweet.wav')
    # pygame.mixer.music.play()
    insects = pygame.mixer.Sound('rainforest_sounds/bird_tweet.wav') 
    pygame.mixer.Sound.play(insects)
    
def insects():
    insects = pygame.mixer.Sound('rainforest_sounds/river_insects.wav') 
    pygame.mixer.Sound.play(insects)
        
                  
pygame.init()
# sound_effect = pygame.mixer.Sound('river_insects.wav') 
 
root = Tk()
root.geometry('1280x800')
root.configure(bg='green')

myframe = Frame(root, bg="green")
myframe.pack()

mylabel = Label(myframe, text = "Rainforest Sounds Mixer", font='Helvetica', bg="green")
mylabel.pack()
 
button1 = Button(myframe, text = "Song", command = song, width = 15, font='Helvetica', bg="#BADA55")
button1.pack(pady = 5)
button2 = Button(myframe, text = "Wind", command = wind, width = 15, font='Helvetica', bg="#BADA55")
button2.pack(pady = 5)
button3 = Button(myframe, text = "Rain", command = rain, width = 15, font='Helvetica', bg="#BADA55")
button3.pack(pady = 5)
button4 = Button(myframe, text = "Birds", command = birds, width = 15, font='Helvetica', bg="#BADA55")
button4.pack(pady = 5)
button4 = Button(myframe, text = "Insects", command = insects, width = 15, font='Helvetica', bg="#BADA55")
button4.pack(pady = 5)
 
root.mainloop()

