import numpy as np
import math
#Funcion que implementa el algoritmo OverLap and Add
#recibe un vector con los valores de la senal, la funcion ventana
#a utilizar, el overlap entre ventanas(factor que indica cuanto se
# superponen, ej: 0.5 =50%). Devuelve el vector con los valores de la
#senal en su nueva escala de tiempo.

def OLA(input,window,t_func,overlap=0.5):

    grain_size= len(window)
    window_spacing = (1.0-overlap)*len(window)
    max_output_time= int(t_func[-1])
    output_size = max_output_time
    output = np.zeros( output_size )
    number_of_slots = math.ceil(max_output_time/window_spacing)
    output_slots= np.zeros( number_of_slots ) #Vector con las coordenadas centrales de los intervalos(grains) del output
    output_slots[0] = 0
    for i in range(1,number_of_slots):
        output_slots[i] = i*window_spacing

    input_slots= np.zeros( number_of_slots ) #Vector con las coordenadas centrales de los intervalos(grains) del input
    aux=0
    tau=0
    for i in range(1,number_of_slots):
        j=0
        while tau < output_slots[i]:
            tau = t_func[aux+j] #Busco cuando me paso del tiempo ya que la funcion es monotona creciente.
            j = j+1
        input_slots[i] = aux+j-1
        aux = j

    #Copio los slots del input a su lugar correspondiente en el output
    center_of_window = math.floor(len(window)/2.0)
    grain= np.multiply( input[0:center_of_window], window[center_of_window:])
    output[0:center_of_window]= grain
    grain= np.zeros(grain_size)
    for j in range(1,number_of_slots):
        start_index_inp = math.floor(input_slots[j] - (grain_size/2.0))
        if(start_index_inp< 0):
            start_index_inp=0
        start_index_out= math.floor(output_slots[j] - (grain_size/2.0))
        k=0
        end_of_grain = math.floor(input_slots[j] + (grain_size/2.0))
        while (k<grain_size)and(start_index_out+k<output_size)and( start_index_inp+k<len(input))and(start_index_inp+k<end_of_grain):
            #obtengo el intervalo a copiar
            grain[k] = input[start_index_inp+k]
            grain[k] = grain[k]*window[k]
            #Actualizo el vector de output
            output[start_index_out+k] = grain[k]
            k= k+1
    #Normalizo el vector
    return np.array(output)
