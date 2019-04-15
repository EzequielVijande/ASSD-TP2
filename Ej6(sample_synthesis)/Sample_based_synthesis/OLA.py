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
    output_size = len(t_func)
    output = np.zeros( output_size )
    number_of_slots = math.floor(output_size/window_spacing)
    output_slots= np.zeros( number_of_slots ) #Vector con las coordenadas centrales de los intervalos(grains) del output
    output_slots[0] = 0
    for i in range(1,number_of_slots):
        output_slots[i] = i*window_spacing

    input_slots= np.zeros( number_of_slots ) #Vector con las coordenadas centrales de los intervalos(grains) del input
    for i in range(0,number_of_slots):
        input_slots[i] = t_func.index( output_slots[i])

    #Copio los slots del input a su lugar correspondiente en el output
    grain= np.multiply( input[0:grain_size], window)
    output[0:grain_size]= grain
    for j in range(1,number_of_slots):
        start_index_inp = input_slots[j] - (window_spacing/2.0)
        start_index_out = output_slots[j] - (window_spacing/2.0)
        grain= input[start_index:grain_size]
        output[0:grain_size]= grain
