"""
app.py
Hexcodes:
Light grey: #eeeeee
Light cream: #bcb5b1
Mid green: #75736b
Dark green: #353531
"""

import pygame
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# ROOT WINDOW
window = tk.Tk()
window.title("The Amazone")
window.configure(bg="#506b52")
window.geometry('1280x800')

# TITLE SECTION
# font choices: sylfaen, palatino linotype, Gabriola, Ebrima, Candara, Candara light
title_frame = tk.Frame(master=window, bg="#506b52")
title_frame.pack(fill=tk.X)
title = tk.Label(master=title_frame, text="Welcome to the Amazone", width=800, font=('Candara',25), bg='#506b52', fg='#eeeeee')
title.pack(pady=2)

# TODO ADD THE BUTTON CONTROLS
def play():
    pygame.mixer.music.load('sounds/woods_spirit.mp3')
    pygame.mixer.music.play(-1)
    
def pause():
    pygame.mixer.music.pause()
    
def unpause():
    pygame.mixer.music.unpause()
    
def restart():
    pygame.mixer.music.stop()

# VIDEO SECTION
video_frame = tk.Frame(master=window, width=200, height=450, bg="orange")
video_frame.pack()

# add photo placeholder to video section
img = (Image.open("3.jpg"))
img = img.resize((800,600), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
video_label = tk.Label(video_frame, image = img)
video_label.pack()

# CONTROLS SECTION
create_frame = tk.Frame(master=window, width=200, height=350, bg="purple")
# create_frame.pack(fill=tk.X, side=tk.TOP)
create_frame.place(relx=0, rely=0.7)

# add the sample label
sample_label_frame = tk.Frame(master=create_frame, relief=tk.FLAT,borderwidth=1)
sample_label_frame.grid(row=0, column=0)
sample_label_frame = tk.Label(master=sample_label_frame, text="Sample", width=20, font=('Candara',10))
sample_label_frame.pack(pady=2)

# add the timeline
timeline_frame = tk.Frame(master=create_frame, relief=tk.FLAT,borderwidth=1)
timeline_frame.grid(row=0, column=1)
timeline_label = tk.Label(master=timeline_frame, text="Timeline Label", width=120)
timeline_label.pack(pady=2)

# add the controls section
controls_frame = tk.Frame(master=create_frame, relief=tk.FLAT, borderwidth=1)
controls_frame.grid(row=0, column=2)

# add the control buttons
play_photo = (Image.open("play_green.png")).resize((20,20), Image.ANTIALIAS)
play_photo = ImageTk.PhotoImage(play_photo)
pause_photo = (Image.open("pause_green.png")).resize((20,20), Image.ANTIALIAS)
pause_photo = ImageTk.PhotoImage(pause_photo)
restart_photo = (Image.open("restart_green.png")).resize((20,20), Image.ANTIALIAS)
restart_photo = ImageTk.PhotoImage(restart_photo)

play_button = tk.Button(master=controls_frame, command=play, image=play_photo, width=50, bg="#eeeeee", activebackground="#BADA55")
pause_button = tk.Button(master=controls_frame, command=pause, image=pause_photo, width=50, bg="#eeeeee", activebackground="#BADA55")
restart_button = tk.Button(master=controls_frame, command=restart, image=restart_photo, width=50, bg="#eeeeee", activebackground="#BADA55")

play_button.pack(side=tk.LEFT)
pause_button.pack(side=tk.LEFT)
restart_button.pack(side=tk.LEFT)

# add the sample name label
sample_frame = tk.Frame(master=create_frame, relief=tk.FLAT, borderwidth=1)
sample_frame.grid(row=1, column=0)
sample_label = tk.Label(master=sample_frame, text="Generated Sample", width=20)
sample_label.pack(pady=7)

# add the sound image section
sound_frame = tk.Frame(master=create_frame, relief=tk.FLAT, borderwidth=1)
sound_frame.grid(row=1, column=1)
sound_photo = (Image.open("soundscape.png")).resize((800,50), Image.ANTIALIAS)
sound_photo = ImageTk.PhotoImage(sound_photo)
sound_label = tk.Label(master=sound_frame, image=sound_photo, width=800)
sound_label.pack(pady=7)

# add the volume controls section
volume_frame = tk.Frame(master=create_frame, relief=tk.FLAT,borderwidth=1)
volume_frame.grid(row=1, column=2)

# within the volume control section, add a volume label, a volume slider and a bin button
bin_photo = (Image.open("bin_green.png")).resize((20,20), Image.ANTIALIAS)
bin_photo = ImageTk.PhotoImage(bin_photo)

vol_label = tk.Label(master=volume_frame, text="Vol", width=5, font=('Candara',10))
vol_slider = ttk.Scale(master=volume_frame, from_=0, to=100, orient='horizontal')
bin_button = tk.Button(master=volume_frame, image = bin_photo, width=50, bg="#eeeeee", activebackground="#BADA55")

vol_label.pack(side=tk.LEFT)
vol_slider.pack(side=tk.LEFT)
bin_button.pack(side=tk.LEFT)

pygame.init()
window.mainloop()
