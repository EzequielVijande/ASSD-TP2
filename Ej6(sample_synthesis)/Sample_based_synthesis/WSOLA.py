import numpy as np
import math
#Funcion que implementa el algoritmo OverLap and Add
#recibe un vector con los valores de la senal, la funcion ventana
#a utilizar, el overlap entre ventanas(factor que indica cuanto se
# superponen, ej: 0.5 =50%). Devuelve el vector con los valores de la
#senal en su nueva escala de tiempo.

def WSOLA(input,window,t_func,max_tolerance=50,overlap=0.5):

    grain_size= len(window)
    window_spacing = (1.0-overlap)*len(window)
    max_output_time= math.ceil(t_func[-1])
    output_size = max_output_time
    output = np.zeros( output_size )
    number_of_slots = math.ceil(max_output_time/window_spacing)
    output_slots= np.zeros( number_of_slots ) #Vector con las coordenadas centrales de los intervalos(grains) del output
    output_slots[0] = 0
    for i in range(1,number_of_slots):
        output_slots[i] = i*window_spacing

    input_slots= np.zeros( number_of_slots ) #Vector con las coordenadas centrales de los intervalos(grains) del input
    input_offsets = np.zeros( number_of_slots) #Vector con el offset de cada ventana
    j=0
    tau=0
    for i in range(1,number_of_slots):
        while tau < output_slots[i]:
            tau = t_func[j] #Busco cuando me paso del tiempo ya que la funcion es monotona creciente.
            j = j+1
        input_slots[i] = j-1

    #Copio los slots del input a su lugar correspondiente en el output
    center_of_window = math.floor(len(window)/2.0)
    grain= np.multiply( input[0:center_of_window], window[center_of_window:])
    output[0:center_of_window]= grain[0:center_of_window]
    for j in range(1,number_of_slots):
        k=0
        grain= np.zeros(grain_size)
        start_index_inp = math.floor(input_slots[j] + input_offsets[j-1] - (grain_size/2.0))
        points_left = grain_size
        start_index_out= math.floor(output_slots[j] - (grain_size/2.0))
        end_of_grain = math.floor(input_slots[j] + (grain_size/2.0))
        if(start_index_inp< 0):
            points_left = grain_size + start_index_inp
            start_index_inp=0
            while (k<points_left)and(start_index_out+k<output_size)and( start_index_inp+k<len(input)):
                #obtengo el intervalo a copiar
                grain[grain_size-points_left+k] = input[start_index_inp+k] * window[grain_size-points_left+k]
                #Actualizo el vector de output
                output[start_index_out+k] = grain[grain_size-points_left+k]
                k= k+1
        else:
            while (k<grain_size)and(start_index_out+k<output_size)and( start_index_inp+k<len(input))and(start_index_inp+k<end_of_grain):
                #obtengo el intervalo a copiar
                grain[k] = input[start_index_inp+k]
                grain[k] = grain[k]*window[k]
                #Actualizo el vector de output
                output[start_index_out+k] = grain[k]
                k= k+1
        #Calculo el proximo offset
        natural_prog_frame_center = input_slots[j-1]+input_offsets[j-1]+window_spacing
        ideal_frame = GetWindowedFrame(input,window,natural_prog_frame_center)
        lower_end = math.floor(input_slots[j]-(grain_size/2.0)-max_tolerance)
        upper_end = math.ceil(input_slots[j]+(grain_size/2.0)+max_tolerance)
        if(lower_end < 0):
            lower_end=0
        if(upper_end >= input.size):
            upper_end = (input.size)-1
        next_frame = input[lower_end:upper_end]
        correlation = np.convolve(next_frame,ideal_frame)
        relevant = correlation[0:2*max_tolerance] #Falta ver que hacer cuando el intevalo se me vaaaaa!!!!!!
        max_correlation = np.max(relevant)
        if(max_correlation < max_tolerance):
            input_offsets[i] = -max_correlation
        else:
            input_offsets[i] = max_correlation
    #Normalizo el vector
    sum_of_input_windows= np.zeros(len(output))
    for i in range(0,number_of_slots):
        k=0
        start_index = math.floor( output_slots[i] - (grain_size/2.0) )
        points_left = grain_size
        if(start_index<0): #Parte de la ventana cae donde el input es nulo
            points_left= grain_size + start_index
            start_index=0
            while (k<points_left)and(start_index+k <len(output)):
                sum_of_input_windows[start_index+k] = sum_of_input_windows[start_index+k]+window[grain_size-points_left+k]
                k=k+1
        else:
            while (k<points_left)and(start_index+k <len(output)):
                sum_of_input_windows[start_index+k] = sum_of_input_windows[start_index+k]+window[k]
                k=k+1
    epsilon = 1e-10 * np.ones(sum_of_input_windows.size)
    sum_of_input_windows =sum_of_input_windows+epsilon #Sumo un epsilon para evitar posible division por cero
    return np.divide(np.array(output),sum_of_input_windows)


def GetWindowedFrame(input,window,center_index):
    window_size = window.size
    k=0
    start_index = math.floor( center_index - (window_size/2.0) )
    points_left = window_size
    result = np.zeros( window_size)
    if(start_index<0): #Parte de la ventana cae donde la secuencia es nula
        points_left= window_size + start_index
        start_index=0
        while (k<points_left):
            result[window_size-points_left+k] = input[start_index+k]*window[window_size-points_left+k]
            k=k+1
    else:
        while (k<points_left)and(start_index+k <len(output)):
            result[k] = input[start_index+k]*window[k]
            k=k+1
