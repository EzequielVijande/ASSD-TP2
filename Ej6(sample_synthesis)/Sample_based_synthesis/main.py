import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import SampleSynthesizer as sam
import midi


synthesizer = sam.SampleSynthesizer()
synthesizer.SetInstrument('guitar')

pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
synthesizer.set_resolution(pattern.resolution)
# for trk in pattern:
#   synth.synthesize(trk)
synthesizer.synthesize(pattern[1])

