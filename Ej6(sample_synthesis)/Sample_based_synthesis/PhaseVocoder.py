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
    #Construyo el vector que mappea las instancias de sintesis en el input
    tau=0
    j=0
    interp_spectrums = np.zeros( (synth_vector.size,int(len(window)/2)) )
    for i in range(0,synth_vector.size):
        while tau < synth_vector[i]:
            tau = t_func[j] #Busco cuando me paso del tiempo ya que la funcion es monotona creciente.
            j = j+1
        lower_instance_index = math.floor( (j-1)/hop_size )
        interp_spectrums[i] = InterpolateSpectrum(spectrums,j-1,lower_instance_index,hop_size)

def CalculateSpectrums(input,window,instances):
    window_size= window.size
    result = np.zeros( (instances.size,int(window_size/2)) )
    for i in range(0,instances.size):
        k=0
        start_index = math.floor( instances[i] - (window_size/2.0) )
        points_left = window_size
        windowed_input = np.zeros( window_size)
        if(start_index<0): #Parte de la ventana cae donde el input es nulo
            points_left= window_size + start_index
            start_index=0
            while (k<points_left)and(start_index+k <len(input)):
                windowed_input[window_size-points_left+k] = input[start_index+k]*window[window_size-points_left+k]
                k=k+1
        else:
            while (k<points_left)and(start_index+k <len(input)):
                windowed_input[k] = input[start_index+k]*window[k]
                k=k+1
        #Le aplico la fft al segmento con la ventana aplicada
        aux = 2*( fft.rfft(windowed_input)/window_size )
        result[i] = np.array( aux[range(int(window_size/2))] )

    return result
def InterpolateSpectrum(spectrums,time,lower_instance_index,hop_size):
    #Determina el espectro correspondiente al tiempo que
    #recibe mediante una interpolacion lineal del espectro de
    #la instancia inmediatamente superior y la inferior.
   first_coef= (time-lower_instance_index*hop_size)/( hop_size )
   second_coef= ( (lower_instance_index+1)*hop_size-time )/( hop_size )
   return ( first_coef*spectrums[lower_instance_index+1]+second_coef*spectrums[lower_instance_index])
