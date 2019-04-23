import wave
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import SampleSynthesizer as sam
import midi


synthesizer = sam.SampleSynthesizer()
synthesizer.SetInstrument('guitar')

pattern = midi.read_midifile(".\ArchivosMIDI\Aguado_12valses_Op1_No1.mid")
synthesizer.set_resolution(pattern.resolution)
# for trk in pattern:
#   synth.synthesize(trk)
synthesizer.synthesize(pattern[0])

