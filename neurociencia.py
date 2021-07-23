# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def homogenizar(archivo):
    numero_columnas = 0
    
    with open(archivo, 'r') as texto:
        # Leer las líneas
        lineas = texto.readlines()
    
        for linea in lineas:
            #Contar número de columnas en linea
            contador = len(linea.split(',')) + 1
    
            if numero_columnas < contador:
                numero_columnas = contador
    
    # Cerrar el archivo
    texto.close()   
    
    # Generar el índice de columnas
    nombre_columnas = [i for i in range(0, numero_columnas)]
    
    datos_neurona = pd.read_csv(archivo, header=None, delimiter=',',
                                skip_blank_lines=False, names=nombre_columnas)    

    data = datos_neurona.to_numpy()
    return data
    
#Calcular la tasa de disparo de un archivo dado
def calcular_td(data, longitud, paso, tiempo_minimo, tiempo_maximo,
                numero_clases):
    
    
    indices = [0 for x in range(numero_clases + 1)]
    
    numero_ensayos, numero_columnas = data.shape
    
    #Obtener los indices para los cambios de clase
    indices[0] = -1
    indices[numero_clases] = numero_ensayos
    j = 1
    for i in range(numero_ensayos):
        if  np.isnan(data[i,1]):
            indices[j] = i
            j += 1 
    
    #Dividir entre el paso para obtener última ventana
    data = np.floor_divide(data, paso)
    ultima = np.nanmin(data)
    
    ventanas = int(longitud//paso)
    
    #Calcular tiempos
    tiempos_paso = []
    tiempos_grafica = []
        
    tiempo = tiempo_minimo + (longitud / 2)
    while tiempo <= tiempo_maximo - (longitud / 2):
        tiempos_paso.append(tiempo)
        tiempos_grafica.append(tiempo + (longitud / 2))
        tiempo += paso

    tasas_disparo = np.zeros((numero_clases, len(tiempos_grafica)))
    
    for i in range(numero_clases):
        ensayos_clase = data[indices[i] + 1 : indices[i + 1], :]
        k = ultima
        for j in range(len(tiempos_paso)):
            suma = 0
            for m in range(ventanas + 1):
                sumandos = np.where(ensayos_clase == (k - m), 1, 0)
                suma += np.sum(sumandos)
            promedio = (suma) / (len(ensayos_clase))
            tasa_disparo = promedio / longitud
            tasas_disparo[i,j] = tasa_disparo
            k+=1
    return tasas_disparo, tiempos_grafica
