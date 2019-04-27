import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import SampleSynthesizer as sam
import midi


pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
synthesizer = sam.SampleSynthesizer(pattern.resolution)
synthesizer.synthesize(pattern[2],'corn anglais','prueba.wav')