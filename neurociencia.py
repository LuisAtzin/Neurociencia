# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
        
#Calcular la tasa de disparo de un archivo dado
def calcular_td(archivo, longitud, paso):
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

