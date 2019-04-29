import synth
from pathlib import Path
import spectralAnalysis as sa

# envelope files
GUITAR_ENVELOPE = ".wav"
VIOLIN_ENVELOPE = ".wav"
SAXO_ENVELOPE = ".wav"
TRUMPET_ENVELOPE = ".wav"

# envelope index
GUITAR = 0
VIOLIN = 1
SAXO = 2
TRUMPET = 3

def initEnvelopes(files,number): # ver que devuelva number env y determinar npg
    originalEnvelopes = []
    for i in range(0,len(files)):
        data_folder = Path("all-samples/")
        file_to_open = data_folder / files[i]
        fs, signalTime, signalData, fftF, fftData, stftF, stftT, stftData, nMax = sa.wavSpectralAnalysis(file_to_open)
        fHarmonic , amplitude = sa.findHarmonic(fftData,fftF, nMax)
        auxEnvelopes = sa.findEnvelopes(fHarmonic,signalData,fs,nMax,npg)
        originalEnvelopes.append(auxEnvelopes)
    return originalEnvelopes


class additiveSynthesis(synth.Synthesizer):
    def __init__(self, resolution):
        self.set_create_notes_callback(self.create_note_array)
        super(additiveSynthesis, self).__init__(resolution)
        files = []
        files.append(GUITAR_ENVELOPE)
        files.append(VIOLIN_ENVELOPE)
        files.append(SAXO_ENVELOPE)
        files.append(TRUMPET_ENVELOPE)
        self.originalEnvelopes = initEnvelopes(files,40)

    # Asume duracion total igual al largo de la envolvente
    # Suma armonicos con su envolvente correspondiente
    # Recibe dos arrays, con las frecuencias y su envolvente correspondiente en el mismo indice del arreglo.
    # Recibe la frecuencia de sampleo. Recibe si se quiere desnormalizar la funcion.
    # Devuelve una arreglo con la funcion final sintetisada
    def additiveSynthesis(frequencies,envelope, fs, desnorm = True):
        signals = [] # arreglo con arreglos de cada senoidal de frecuencia armonica
        synthFunction = [] # arreglo final
        maxLength = 0
        normalizer = 0
        for i in range(0,len(envelope)): # busco envolvente mas larga
            if maxLength < len(envelope[i]):
                maxLength = len(envelope[i])
        for i in range(0,len(envelope)):
            if maxLength > len(envelope[i]):
                zeroArray = np.zeros(maxLength - len(envelope[i])) #
                envelope[i] = np.concatenate([envelope[i], zeroArray])
        t = len(envelope[0])/fs # duracion de la nota
        samples = np.arange(len(envelope[0])) / fs
        for i in range(0,len(frequencies)):
            auxSignal = np.sin(2*np.pi*frequencies[i]*samples) # creo señal
            auxSignal = np.multiply(auxSignal,envelope[i]) # aplico la envolvente
            normalizer = normalizer + np.amax(envelope[i]) # agrego amplitud maxima al coef de normalizacion
            signals.append(auxSignal)
        for i in range(0,len(signals[0])):
            auxValue = 0
            for j in range(0,len(signals)):
                auxValue = auxValue + signals[j][i]
            synthFunction.append(auxValue)
        synthFunction = [i*(1/normalizer) for i in synthFunction] # normalizo en (-1,1)
        if desnorm:
            synthFunction = [i*32767 for i in synthFunction] # desnormalizo a formato wav int16
            synthFunction = np.int16(synthFunction)
        return synthFunction

    def scaleEnvelope(envelope,k):
        scaledEnvelope = []
        scaledEnvelope = np.multiply(k,envelope)
        return scaledEnvelope

    def defineFrequencies(fundamentalFreq,instrument):
        frequencies = []
        harmonics = 30
        frequencies = np.arange(fundamentalFreq,fundamentalFreq*harmonics+1,fo)
        for i in range(0,len(frequencies)):
            desv = random.randint(0,93)/10000.0
            sign = random.randint(0,1)
            desv = desv*((-1)**sign)
            frequencies[i] = frequencies[i]*(1+desv)
        return frequencies

    def getEnvelopes(self,amount_of_ns,instrument):
        envelopes = self.originalEnvelopes[instNumber]
        #hacer que dure lo necesario
        return envelopes

    def create_note_array(self, pitch, amount_of_ns: int, velocity, instrument):
        fundamentalFreq =  2**((pitch - 69) / 12)*440
        intensity = velocity/127
        fs = self.frame_rate
        frequencies = defineFrequencies(fundamentalFreq,instrument)
        envelopes = getEnvelopes(amount_of_ns,instrument)
        note = additiveSynthesis(frequencies,envelopes, fs)
        note = scaleEnvelope(note,intensity)
        return notes


