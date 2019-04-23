import numpy as np
import math
#Funcion que implementa el algoritmo de Timecale Modification
#conocido como Phase vocoder.Recibe el vector al que se le desea
#cambiar su escala de tiempo, la funcion de escalamiento a utilizar,
#la ventana y el espacio entre ventanas que se desea
def PhVocoder(input,window,stretch_func,hop_size):
    window_size= int(window.size)
    output= np.zeros( math.ceil(stretch_func[-1]) )
    analysis_vector = np.zeros(  math.floor( len(input)/hop_size) )
    synth_vector= np.zeros( math.floor( len(output)/hop_size) ) #Creo el vector con las instancias de sintesis
    #Inicializo las instancias de analisis y de sintesis
    for i in range(0,analysis_vector.size):
        analysis_vector[i]= i*hop_size
    for i in range(0,synth_vector.size):
        synth_vector[i]=i*hop_size

    spectrums = CalculateSpectrums(input,window,analysis_vector)
    number_of_freqs = (spectrums.shape)[1]
    #Construyo el vector que mappea las instancias de sintesis en el input
    tau=0
    j=0
    interp_spectrums = np.zeros( (synth_vector.size,number_of_freqs),dtype=complex )
    gm= np.zeros(synth_vector.size, dtype='int16')
    interp_spectrums[0] = spectrums[0]

    for i in range(1,synth_vector.size):
        while tau < synth_vector[i]:
            tau = stretch_func[j] #Busco cuando me paso del tiempo ya que la funcion es monotona creciente.
            j = j+1
        time_index = math.floor( (j-1)/hop_size )
        interp_spectrums[i] = InterpolateSpectrum(spectrums,j-1,int(time_index),hop_size)
        gm[i] = int(time_index)
    #Queda corregir la fase de los espectros
    corrected_phases = np.zeros( interp_spectrums.shape )
    CorrectPhase(corrected_phases,spectrums,gm)
    OutputSpectrum = np.zeros( interp_spectrums.shape,dtype=complex) #armo el vector con los espectros finales
    OutputSpectrum[0] = spectrums[0]
    output_intervals = np.zeros( (synth_vector.size,window_size) )
    output_intervals[0] = np.fft.irfft( OutputSpectrum[0],window_size ) 
    for i in range(1,synth_vector.size):
        for j in range(0,int(len(window)/2)):
            OutputSpectrum[i][j]= np.abs( interp_spectrums[i][j])*complex(math.cos(corrected_phases[i][j]),math.sin(corrected_phases[i][j]))
        output_intervals[i] =np.fft.irfft(OutputSpectrum[i] ) 
    #sumo las secuencias con la ventana aplicada a cada una
    for i in range(0,synth_vector.size):
        k=0
        interval = output_intervals[i]
        start_index = math.floor( synth_vector[i] - (window_size/2.0) )
        points_left = window_size
        windowed_seq = np.zeros( window_size)
        if(start_index<0): #Parte de la ventana cae donde la secuencia es nula
            points_left= window_size + start_index
            start_index=0
            while (k<points_left)and(start_index+k <len(output)):
                windowed_seq[window_size-points_left+k] = interval[k]*window[window_size-points_left+k]
                output[start_index+k]=output[start_index+k]+windowed_seq[window_size-points_left+k]
                k=k+1
        else:
            while (k<points_left)and(start_index+k <len(output)):
                windowed_seq[k] = interval[k]*window[k]
                output[start_index+k]=output[start_index+k]+windowed_seq[k]
                k=k+1
    #normalizo amplitudes
    amp=0
    for i in range(0,window_size):
        amp= amp + ( (window[i])*(window[i]) )
    amp = amp/(2*hop_size)
    return output/amp
    

def CalculateSpectrums(input,window,instances):
    window_size= int(window.size)
    samples= 0
    if( window_size % 2):
        samples =int( (window_size+1)/2 )
    else:
        samples= int( (window_size/2)+1)
    result = np.zeros( (instances.size,samples),dtype=complex )
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
        aux = ( np.fft.rfft(windowed_input) )
        result[i] =  aux 

    return result
def InterpolateSpectrum(spectrums,time,lower_instance_index,hop_size):
    #Determina el espectro correspondiente al tiempo que
    #recibe mediante una interpolacion lineal del espectro de
    #la instancia inmediatamente superior y la inferior.
   first_coef= (time-lower_instance_index*hop_size)/( hop_size )
   second_coef= ( (lower_instance_index+1)*hop_size-time )/( hop_size )
   if (lower_instance_index < (spectrums.shape[0]-1) ):
        return ( first_coef*spectrums[lower_instance_index+1]+second_coef*spectrums[lower_instance_index])
   else:
       return spectrums[-1]
def CorrectPhase(result,spectrums,times):
    time_interval, freq_interval= result.shape
    for i in range(0,freq_interval):
        for j in range(1,time_interval-1):
            if(times[j]+1 >=( (spectrums.shape)[0])):
                delta_phase=0
            else:
                delta_phase= np.angle( spectrums[times[j]+1][i]) - np.angle( spectrums[times[j]][i])
            result[j][i] = result[j-1][i] + delta_phase
            result[j][i] = result[j][i] - math.floor( result[j][i]/(2.0*math.pi) )*2.0*math.pi #argumento principal