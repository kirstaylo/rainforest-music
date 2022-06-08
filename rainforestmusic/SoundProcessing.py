"""
SoundProcessing
"""

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

class SoundProcessing():
    def __init__(self, sound_name):
        plt.style.use('seaborn-dark')
        # assign global variables
        self.sample_rate, self.wave = wavfile.read('{}.wav'.format(sound_name))
        
    def plot_wave(self, interval=(500, 2500)):
        # add error message that catches if there is no wave produces
        
        # visualise the wave
        plt.plot(self.wave[interval[0]:interval[1]])
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Wave Shape')
        plt.grid()
        plt.show()
            
    def find_fft_overtones(self, note_freq, plot=True):
        #FFT
        t = np.arange(self.wave.shape[0])
        freq = np.fft.fftfreq(t.shape[-1])*self.sample_rate
        sp = np.fft.fft(self.wave) 
        
        if plot:
            # Plot spectrum
            plt.plot(freq, abs(sp.real))
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')
            plt.title('FFT Spectrum of Sound Sample')
            plt.xlim((0, 2000))
            plt.grid()
            plt.show()
            
        # Get positive frequency
        idx = np.where(freq > 0)[0]
        freq = freq[idx]
        sp = sp[idx]
        
        # Get dominant frequencies
        sort = np.argsort(-abs(sp.real))[:100]
        dom_freq = freq[sort]
        
        # Round and calculate amplitude ratio
        freq_ratio = np.round(dom_freq/note_freq)
        unique_freq_ratio = np.unique(freq_ratio)
        amp_ratio = abs(sp.real[sort]/np.sum(sp.real[sort]))
        factor = np.zeros((int(unique_freq_ratio[-1]), ))
        for i in range(factor.shape[0]):
            # find the frequency ratios for the particular unique frequency component
            idx = np.where(freq_ratio==i+1)[0]
            # sum the amplitude ratios together for the amplitude ratios
            factor[i] = np.sum(amp_ratio[idx])
        # make all the factors add to one
        self.factor = factor/np.sum(factor)
        
        