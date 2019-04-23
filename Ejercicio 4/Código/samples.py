import numpy as np
from scipy.io.wavfile import read
from pydub import AudioSegment
from pydub.playback import play
import wave, struct, math


#Create 44KHz signal and save to 'sound.wav'
sampleRate = 44100.0 # hertz
duration = 1.0       # seconds
frequency = 440.0    # hertz

wavef = wave.open('sound.wav','w')
wavef.setnchannels(1) # mono
wavef.setsampwidth(2)
wavef.setframerate(sampleRate)

for i in range(int(duration * sampleRate)):
    value = int(32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate)))
    data = struct.pack('<h', value)
    wavef.writeframesraw( data )

wavef.writeframes('')
wavef.close()

#Read wave file and save signal to text file
rate, signal = read("sound.wav")

np.savetxt('test.txt', signal, delimiter=',')   # X is an array


#load wav data from text file
wavedata1 = np.loadtxt("test.txt", comments="#", delimiter=",", unpack=False, dtype=np.int16)

#Create variation of signal
wavedata2 = np.loadtxt("test.txt", comments="#", delimiter=",", unpack=False, dtype=np.int32)

#Create variation of signal
wavedata3 = np.loadtxt("test.txt", comments="#", delimiter=",", unpack=False, dtype=np.float16)

#create first audio segment
audio_segment1 = AudioSegment(
    wavedata1.tobytes(),
    frame_rate=rate,
    sample_width=2,
    channels=1
)

#create second audio segment
audio_segment2 = AudioSegment(
    wavedata2.tobytes(),
    frame_rate=rate,
    sample_width=2,
    channels=1
)

#create third audio segment
audio_segment3 = AudioSegment(
    wavedata3.tobytes(),
    frame_rate=rate,
    sample_width=2,
    channels=1
)

# Play audio (requires ffplay, or pyaudio):
play(audio_segment1)
play(audio_segment2)
play(audio_segment3)

#Mix three audio segments
mixed1 = audio_segment1.overlay(audio_segment2)          #combine , superimpose audio files
mixed2  = mixed1.overlay(audio_segment3)          #Further combine , superimpose audio files
#If you need to save mixed file
mixed2.export("mixed.wav", format='wav') #export mixed  audio file
play(mixed2)                             #play mixed audio file
