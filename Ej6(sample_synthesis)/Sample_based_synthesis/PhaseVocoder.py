import numpy as np
import math
import scipy.fftpack as fft
#Funcion que implementa el algoritmo de Timecale Modification
#conocido como Phase vocoder.Recibe el vector al que se le desea
#cambiar su escala de tiempo, la funcion de escalamiento a utilizar,
#la ventana y el espacio entre ventanas que se desea
def PhVocoder(input,window,stretch_func,hop_size):
    output= np.zeros( int(stretch_func[-1]) )
    analysis_vector = np.zeros(  math.floor( len(input)/hop_size) )
    synth_vector= np.zeros( math.floor( len(output)/hop_size) ) #Creo el vector con las instancias de sintesis
    #Inicializo las instancias de analisis y de sintesis
    for i in range(0,analysis_vector.size):
        analysis_vector[i]= i*hop_size
    for i in range(0,synth_vector.size):
        synth_vector[i]=i*hop_size

    spectrums = CalculateSpectrums(input,window,analysis_vector)
    y=1

def CalculateSpectrums(input,window,instances):
    window_size= window.size
    result = np.zeros( (instances.size,window_size) )
    for i in range(0,instances.size):
        start_index = math.floor( instances[i] - (window_size/2.0) )
        points_left = window_size
        if(start_index<0):
            points_left= window_size + start_index
            start_index=0
        windowed_input = np.zeros( points_left)
        k=0
        while (k<points_left)and(start_index+k <len(input)):
            windowed_input[k] = input[start_index+k]*window[k]
            k=k+1
        #Le aplico la fft al segmento con la ventana aplicada
        aux = 2*( fft.rfft(windowed_input)/points_left )
        result[i] = np.array( aux[range(int(points_left/2))] )

    return result