"""
MidiProcessing
"""

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from music21 import converter,instrument
from midi2audio import FluidSynth
import os

class MidiProcessing():
    def __init__(self, filename):
        self.filename = filename
        plt.style.use('seaborn-dark')
        # assign global variables
        self.s = converter.parse('./gen_music/{}.mid'.format(filename))
        
    def change_instrument(self, instrument):
        for el in self.s.recurse():
            if 'Instrument' in el.classes:
                el.activeSite.replace(el, instrument)
                
        self.s.write('midi', './gen_music/{}_Harp.mid'.format(self.filename))
        
    def write_wav(self):
        fs = FluidSynth()
        fs.midi_to_audio('good.mid', 'good.wav')

midi = MidiProcessing('good')
midi.change_instrument(instrument.Harp())
midi.write_wav()