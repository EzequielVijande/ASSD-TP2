import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import SampleSynthesizer as sam
import midi


pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
synthesizer = sam.SampleSynthesizer(pattern.resolution)
# for trk in pattern:
#   synth.synthesize(trk)
synthesizer.synthesize(pattern[1],'guitar','Track0_voc2.wav')
#note = synthesizer.MakeNote(pitch=57,intensity=68,duration=9923)
#note = note.astype('int16')
#wavfile.write('nota.wav',44100,note)