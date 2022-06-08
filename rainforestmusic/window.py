"""
Window
"""
import pygame
import tkinter as tk
from tkinter import ttk
from tkvideo import tkvideo
from PIL import ImageTk, Image

class Window():
    def __init__(self, window_name, geometry, background_colour):
        # general gui settings
        self.background_colour = background_colour
        self.window = tk.Tk()
        self.window.title(window_name)
        self.window.configure(bg=background_colour)
        self.window.geometry(geometry)
        # locations to store which sounds are in the control area
        self.sounds = []
        self.volumes = []
        self.widget_store = []
        self.hover_store = []
        self.soundwaves = {}
        # location to store the button instances so doesn't get lost
        self.button_icons = {}
        self.info_pics = {}
        # flag to decide whether play button should play or unpause
        self.at_start = 1
        self.convert = {"insects":"AI Music", "flowing_river":"Flowing River", "forest_rain": "Forest Rain"}
        
    def woods_spirit(self):
        print('adding woods_spirit')
        self.add_sound("woods_spirit", 'Candara', 10, 2)
        
    def flowing_river(self):
        print('adding flowing_river')
        self.add_sound("flowing_river", 'Candara', 10, 2)
        
    def birds(self):
        print('adding birds')
        self.add_sound("birds", 'Candara', 10, 2)
        
    def insects(self):
        print('adding insects')
        self.add_sound("insects", 'Candara', 10, 2)
        
    def wind(self):
        print('adding wind')
        self.add_sound("wind", 'Candara', 10, 2)
        
    def forest_rain(self):
        print('adding forest_rain')
        self.add_sound("forest_rain", 'Candara', 10, 2)
        
    def build_title(self, title_text, font, font_size, font_colour, pady):
        self.title_frame = tk.Frame(master=self.window, bg=self.background_colour)
        self.title_frame.pack(fill=tk.X)
        title = tk.Label(master=self.title_frame, text=title_text, font=(font, font_size), bg=self.background_colour, fg=font_colour)
        title.pack(pady=pady)
        
    def build_video(self, video_loc, size):
        self.video_frame = tk.Frame(master=self.window, width=200, height=450)
        self.video_frame.pack()
        video_label = tk.Label(master=self.video_frame)
        video_label.pack()
        # read video to display on label
        player = tkvideo("scenes/canoe.MOV", video_label, loop = 20, size = (700, 500))
        player.play()
    
    def make_button(self, master, icon_loc, size, command, key=0):
        if key==0:
            key = command
        self.button_icons[key] = (Image.open(icon_loc)).resize(size, Image.ANTIALIAS)
        self.button_icons[key] = ImageTk.PhotoImage(self.button_icons[key])
        button = tk.Button(master=master, command=command, image=self.button_icons[key], width=50, bg="#eeeeee", activebackground="#BADA55")
        return button
        
    def build_controls(self, yloc, sample_title, font, font_size, pady):
        # self.controls_frame = tk.Frame(master=self.window, bg=self.background_colour)
        # self.controls_frame.place(rely=yloc)
        self.control = VerticalScrolledFrame(self.window)
        self.control.place(rely=yloc)
        self.controls_frame = self.control.interior
        # make the sample label
        sample_label_frame = tk.Frame(master=self.controls_frame, borderwidth=1, width=25, bg="#bada55")
        sample_label_frame.grid(row=0, column=0)
        sample_label = tk.Label(master=sample_label_frame, text=sample_title, font=(font,font_size), width=26, bg="#bada55")
        sample_label.pack(pady=pady)
        # add the timeline
        timeline_frame = tk.Frame(master=self.controls_frame, borderwidth=1, bg="#BADA55", width=800)
        timeline_frame.grid(row=0, column=1)
        self.timeline_icon = (Image.open("button_icons/timeline_2.png")).resize((870,20), Image.ANTIALIAS)
        self.timeline_icon = ImageTk.PhotoImage(self.timeline_icon)
        timeline_label = tk.Label(master=timeline_frame, image=self.timeline_icon, width=870, bg="#bada55")
        timeline_label.pack()
        cbuttons_frame = tk.Frame(master=self.controls_frame, relief=tk.FLAT, borderwidth=1, bg='#bada55')
        cbuttons_frame.grid(row=0, column=2)
        play_button = self.make_button(cbuttons_frame, "button_icons/play_green.png", (20,20), self.play)
        play_button.pack(side=tk.LEFT)
        pause_button = self.make_button(cbuttons_frame, "button_icons/pause_green.png", (20,20), self.pause)
        pause_button.pack(side=tk.LEFT)
        restart_button = self.make_button(cbuttons_frame, "button_icons/restart_green.png", (20,20), self.restart)
        restart_button.pack(side=tk.LEFT)
        
        # wood spirit
        spirit = tk.Button(master=self.window, command=self.woods_spirit, text="Cicada", width=10, bg="#eeeeee", activebackground="#BADA55")
        spirit.place(rely=0.5, relx=0.90)
        spirit.bind("<Enter>", self.button_hover_maker(spirit, 0.67, 0.5))
        spirit.bind("<Leave>", self.button_leave_maker(spirit))
        # fowing river
        river = tk.Button(master=self.window, command=self.flowing_river, text="Flowing River", width=10, bg="#eeeeee", activebackground="#BADA55")
        river.place(rely=0.5, relx=0.05)
        river.bind("<Enter>", self.button_hover_maker(river, 0.11, 0.5))
        river.bind("<Leave>", self.button_leave_maker(river))
        # birds
        birds = tk.Button(master=self.window, command=self.birds, text="Forest Rain", width=10, bg="#eeeeee", activebackground="#BADA55")
        birds.place(rely=0.3, relx=0.05)
        birds.bind("<Enter>", self.button_hover_maker(birds, 0.11, 0.3))
        birds.bind("<Leave>", self.button_leave_maker(birds))
        # insects
        insects = tk.Button(master=self.window, command=self.insects, text="AI Music", width=10, bg="#eeeeee", activebackground="#BADA55")
        insects.place(rely=0.4, relx=0.05)
        insects.bind("<Enter>", self.button_hover_maker(insects, 0.11, 0.4))
        insects.bind("<Leave>", self.button_leave_maker(insects))
        # wind
        wind = tk.Button(master=self.window, command=self.wind, text="Toucan", width=10, bg="#eeeeee", activebackground="#BADA55")
        wind.place(rely=0.3, relx=0.90)
        wind.bind("<Enter>", self.button_hover_maker(wind, 0.627, 0.3))
        wind.bind("<Leave>", self.button_leave_maker(wind))
        # rain
        rain = tk.Button(master=self.window, command=self.forest_rain, text="Tree Frog", width=10, bg="#eeeeee", activebackground="#BADA55")
        rain.place(rely=0.4, relx=0.90)
        rain.bind("<Enter>", self.button_hover_maker(rain, 0.67, 0.4))
        rain.bind("<Leave>", self.button_leave_maker(rain))
        
    def create_sound_controls(self, master, font, font_size, i):
        # within the volume control section, add a volume label, a volume slider and a bin button
        bin_button = self.make_button(master, "button_icons/bin_green.png", (20,20), self.binn_maker(i), key="{}".format(i))
        vol_label = tk.Label(master=master, text="Vol", width=5, font=(font,font_size))
        vol_slider = ttk.Scale(master=master, from_=0, to=100, orient='horizontal', command=self.vol_slider_change_maker(i-1), variable=self.volumes[i-1])
        vol_label.pack(side=tk.LEFT)
        vol_slider.pack(side=tk.LEFT)
        bin_button.pack(side=tk.LEFT)
        
    def add_sound(self, sound_name, font, font_size, pady, index=100):
        if index==100:
            index = len(self.sounds)+1
            # add the sound to the list
            self.sounds.append(sound_name)
            self.volumes.append(tk.DoubleVar())
        # add the name to the index row of the controls frame
        sound_label_frame = tk.Frame(master=self.controls_frame, borderwidth=1, bg='#eeeeee')
        sound_label_frame.grid(row=index, column=0, sticky='nsew')
        sound_label = tk.Label(master=sound_label_frame, text=self.convert[sound_name], font=(font,font_size), bg="#eeeeee")
        sound_label.pack(pady=pady)
        # add the soundscape image to the middle column
        soundwave_frame = tk.Frame(master=self.controls_frame, relief=tk.FLAT, borderwidth=1, bg='#eeeeee')
        soundwave_frame.grid(row=index, column=1, sticky='nsew')
        self.soundwaves[sound_name] = (Image.open("soundwaves/{}.png".format(sound_name))).resize((800,50), Image.ANTIALIAS)
        self.soundwaves[sound_name] = ImageTk.PhotoImage(self.soundwaves[sound_name])
        sound_label = tk.Label(master=soundwave_frame, image=self.soundwaves[sound_name], width=800)
        sound_label.pack(pady=7)
        # add the volume and bin controls to the last column
        volume_frame = tk.Frame(master=self.controls_frame, relief=tk.FLAT,borderwidth=1, bg='#eeeeee')
        volume_frame.grid(row=index, column=2, sticky='nsew')
        self.create_sound_controls(volume_frame, font, font_size, index)
        
        # use the index to assign the sound to a channel/row in the GUI
        print(self.sounds)
        # store the widgets 
        self.widget_store.extend([sound_label_frame, volume_frame, soundwave_frame])
    
    # BUTTON FUNCTIONS
    
    def rebuild_control(self):
        # destroy last layer
        layers = len(self.sounds)
        # reassign the layers
        for layer in range(layers):
            self.add_sound(self.sounds[layer], 'Candara', 10, 2, index=layer+1)
        
    def play(self):
        print('play')
        if self.at_start:
            for i, sound in enumerate(self.sounds):
                try:
                    pygame.mixer.Channel(i).play(pygame.mixer.Sound('sounds/{}.mp3'.format(sound)), loops=-1)
                except:
                    pygame.mixer.Channel(i).play(pygame.mixer.Sound('sounds/{}.wav'.format(sound)), loops=-1)
        else:
            for i, sound in enumerate(self.sounds):
                pygame.mixer.Channel(i).unpause()
                self.at_start = 0
        
    def pause(self):
        print('pause')
        pygame.mixer.music.pause()
        for i, sound in enumerate(self.sounds):
            pygame.mixer.Channel(i).pause()
        
    def restart(self):
        print('restart')
        pygame.mixer.music.stop()
        self.at_start = 1
        
    def binn_maker(self, index):
        def binn():
            for widget in self.widget_store:
                widget.destroy()
            print(index-1)
            print(self.sounds[index-1])
            self.sounds.pop(index-1)
            self.volumes.pop(index-1)
            self.rebuild_control()
        return binn
        
    def volume(self, index):
        print('something something volume index {}'.format(index))
    
    def run(self):
        pygame.init()
        self.window.mainloop()
    
    def vol_get_val_maker(self, index):
        def vol_get_current_value():
            return '{: .2f}'.format(self.columes[index].get())
        return vol_get_current_value
    
    def vol_slider_change_maker(self, index):
        def vol_slider_changed(event):
            print("slider {} changed to {}".format(index, self.volumes[index].get()))
            pygame.mixer.Channel(index).set_volume(self.volumes[index].get()/100)
        return vol_slider_changed
    
    def button_hover_maker(self, button, xloc, yloc):
        def button_hover(event):
            button['bg'] = '#ffffff'
            frame = tk.Frame(master=self.window, bg="#eeeeee", width=300, height=150)
            frame.place(relx=xloc, rely=yloc)
            self.hover_store.append(frame)
            # add title to the frame
            title = tk.Label(master=frame, text='Toucan', font=('Candara', 12))
            title.pack(pady=10)
            info_frame = tk.Frame(master=frame, bg="#eeeeee")
            info_frame.pack()
            # add smaller text
            fact = tk.Label(master=info_frame, text='Despite its size, the \n toucan\'s bill is very light \n as it is made of keratin', font=('Candara', 10))
            fact.pack(pady=10, side=tk.LEFT)
            # add photo
            self.info_pics['toucan'] = (Image.open('./info_pics/toucan.jpg')).resize((200,200), Image.ANTIALIAS)
            self.info_pics['toucan'] = ImageTk.PhotoImage(self.info_pics['toucan'])
            # add photo frame
            # photo_frame = tk.Frame(master=info_frame, bg="#eeeeee")
            photo_label = tk.Label(master=info_frame, image=self.info_pics['toucan'])
            photo_label.pack(side=tk.LEFT)
            # photo_frame.pack(side=tk.LEFT)
        return button_hover
    
    def button_leave_maker(self, button):
        def button_leave(event):
            button['bg'] = '#eeeeee'
            self.hover_store[0].destroy()
            self.hover_store.pop()
        return button_leave
    
    
class VerticalScrolledFrame(ttk.Frame):
    """* Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set, width=1200, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        