#!/usr/bin/env python3
'''simdatos.py
Programa para simular el flujo de datos desde sensores de Arduino
'''
import argparse
import time

def stream_data(datos, d_t):
    '''Función que imprime cada elemento de la lista datos esperando d_t entre
    instrucciones de escritura.'''
    for linea in datos:
        print(linea[:-1], flush=True)
        time.sleep(d_t)

def main():
    ''' Programa principal. Lee el nombre del archivo con los datos a
    "streamear" y el intervalo de tiempo entre escrituras.'''

    parser = argparse.ArgumentParser(description='''Programa para simular un
    stream de datos de sensores en tiempo real.''')
    parser.add_argument('-f', '--file', help='Archivo con datos reales',
                        required=True, action='store')
    parser.add_argument('-i', '--intervalo', help='''Intervalo de tiempo entre
    escrituras (en s)''', required=True, action='store')
    args = parser.parse_args()
    file_name = args.file
    delta_t = float(args.intervalo)

    fin = open(file_name, 'r')
    data = fin.readlines()
    fin.close()
    stream_data(data, delta_t)

if __name__ == '__main__':
    main()
