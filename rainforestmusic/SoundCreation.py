# -*- coding: utf-8 -*-
"""
Sound Creation
built using tutorial https://towardsdatascience.com/music-in-python-2f054deb41f4
"""

import numpy as np
import pandas as pd
import json
from scipy.io import wavfile
import matplotlib.pyplot as plt
from fraction import Fraction

class SoundCreation():
    def __init__(self, duration, sample_rate=44100):
        self.note_freqs = pd.read_csv('./note_frequencies.csv')
        self.sample_rate = sample_rate
        self.duration = duration 
        with open('./note_frequencies.json', 'r') as note_frequencies:
            self.note_freqs = json.load(note_frequencies)


    def gen_sin_wave(self, frequency, amplitude=4096):
        # duration is in seconds
        # amplitude defines loudness
        # sample rate is the frequency
        t = np.linspace(0, self.duration, int(self.sample_rate*self.duration)) # Time axis
        self.wave = amplitude*np.sin(2*np.pi*frequency*t)
        
        
    def plot_wave(self, interval=(500, 2500)):
        # add error message that catches if there is no wave produces
        plt.style.use('seaborn-dark')
        
        # visualise the wave
        plt.plot(self.wave[interval[0]:interval[1]])
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Wave Shape')
        plt.grid()
        plt.show()
        
        
    def export_wave(self, name): 
        # write the wave to a wav file
        wavfile.write('{}.wav'.format(name), rate=44100, data=self.wave.astype(np.int16))
        
        
    def add_overtones(self, overtone_ratio):
        assert abs(1-sum(overtone_ratio)) < 1e-8
        
        # find the minimum frequency using the nyquist frequency
        frequencies = np.minimum(np.array([self.frequency*(x+1) for x in range(len(overtone_ratio))]), self.sample_rate//2)
        amplitudes = np.array([self.amplitude*x for x in overtone_ratio])
        
        for i in range(1, len(overtone_ratio)):
            overtone = self.gen_sin_wave(frequencies[i], amplitudes[i])
            self.wave += overtone
        
        
    def add_asdr(self, note_freq, duration, length, decay, sustain_level):
        assert abs(sum(length)-1) < 1e-8
        assert len(length) == len(decay) == 4
    
        intervals = int(duration*note_freq)
        len_A = np.maximum(int(intervals*length[0]),1)
        len_D = np.maximum(int(intervals*length[1]),1)
        len_S = np.maximum(int(intervals*length[2]),1)
        len_R = np.maximum(int(intervals*length[3]),1)
    
        decay_A = decay[0]
        decay_D = decay[1]
        decay_S = decay[2]
        decay_R = decay[3]
    
        A = 1/np.array([(1-decay_A)**n for n in range(len_A)])
        A = A/np.nanmax(A)
        D = np.array([(1-decay_D)**n for n in range(len_D)])
        D = D*(1-sustain_level)+sustain_level
        S = np.array([(1-decay_S)**n for n in range(len_S)])
        S = S*sustain_level
        R = np.array([(1-decay_R)**n for n in range(len_R)])
        R = R*S[-1]
    
        weights = np.concatenate((A,D,S,R))
        smoothing = np.array([0.1*(1-0.1)**n for n in range(5)])
        smoothing = smoothing/np.nansum(smoothing)
        weights = np.convolve(weights, smoothing, mode='same')
        
        weights = np.repeat(weights, int(self.sample_rate*duration/intervals))
        tail = int(self.sample_rate*duration-weights.shape[0])
        if tail > 0:
            weights = np.concatenate((weights, weights[-1]-weights[-1]/tail*np.arange(tail)))
            
        self.wave = self.wave*weights
        self.wave = self.wave*(4096/np.max(self.wave)) # Adjusting the Amplitude 
        
    def do_it_b_synthenizin(self, note_1, note_2):
        freq_1 = float(self.note_freqs[note_1])
        freq_2 = float(self.note_freqs[note_2])
        
        # divide the higher note by the lower note
        ratio = min(freq_1, freq_2) / max(freq_1, freq_2)
        print('ratio', ratio)
        for i in range(1,6):
            ratio_multiplied = ratio * i
            print('ratio multiplied by {}'.format(i), ratio_multiplied)
            nearest_int = round(ratio_multiplied)
            print('nearest int', nearest_int)
            diff = np.abs(ratio_multiplied - nearest_int)
            print('diff', diff)
            print('')
            if diff <= 0.1:
                return True
        return False
        
        
sound = SoundCreation(2)
print(sound.do_it_b_synthenizin('C4', 'E5'))