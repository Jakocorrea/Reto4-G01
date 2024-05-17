"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc
import os
from DISClib.ADT import graph as gr

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {'model':None}
    control['model'] = model.newAnalyzer()
    return control
    
# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de aeropuertos que
    pertenecen al mismo tipo de vuelo y van en el mismo sentido.

    addRouteConnections crea conexiones entre diferentes vuelos
    servidos en un mismo aeropuerto.
    """
    data_structs = control['model']
    airportCharge = loadDataAirportCharge(data_structs)
    airportComercial = loadDataAirportComercial(data_structs)
    airportMilitar = loadDataAirportMilitar(data_structs)
    flightCharge = loadDataFlightCharge(data_structs)
    flightComercial = loadDataFlightComercial(data_structs)
    flightMilitar = loadDataFlightMilitar(data_structs)
    
    return airportCharge, airportComercial, airportMilitar, flightCharge, flightComercial, flightMilitar
    
#Funciones para cargar los aeropuertos.
    
def loadDataAirportCharge(data_structs):
    '''
    Lee el csv de los aeropuertos y aniade al grafo determinado los aeropuertos como vertices con el ICAO.
    '''
    filename = os.path.join(cf.data_dir + 'airports-2022.csv')
    input_file = csv.DictReader(open(filename, encoding= 'utf-8'), delimiter=';', restval='Unknown')
    for data in input_file:
        airportid = data['ICAO']
        model.addAirportCharge(data_structs, airportid)
    return model.data_size_vertex(data_structs['carga'])
    
def loadDataAirportComercial(data_structs):
    '''
    Lee el csv de los aeropuertos y aniade al grafo determinado los aeropuertos como vertices con el ICAO.
    '''
    filename = os.path.join(cf.data_dir + 'airports-2022.csv')
    input_file = csv.DictReader(open(filename, encoding= 'utf-8'), delimiter=';', restval='Unknown')
    for data in input_file:
        airportid = data['ICAO']
        model.addAirportComercial(data_structs, airportid)
    return model.data_size_vertex(data_structs['comercial'])

def loadDataAirportMilitar(data_structs):
    '''
    Lee el csv de los aeropuertos y aniade al grafo determinado los aeropuertos como vertices con el ICAO.
    '''
    filename = os.path.join(cf.data_dir + 'airports-2022.csv')
    input_file = csv.DictReader(open(filename, encoding= 'utf-8'), delimiter=';', restval='Unknown')
    for data in input_file:
        airportid = data['ICAO']
        model.addAirportMilitar(data_structs, airportid) 
    return model.data_size_vertex(data_structs['militar'])
        
#Funciones para cargar los vuelos.

def loadDataFlightCharge(data_structs):
    '''
    Lee el csv de los vuelos y aniade al grafo determinado los vuelos como arcos con el peso en tiempo.
    '''
    filename = os.path.join(cf.data_dir + 'fligths-2022.csv')
    input_file = csv.DictReader(open(filename, encoding='UTF-8'), delimiter=';', restkey='Unknown')
    for data in input_file:
        if data['TIPO_VUELO'] == 'AVIACION_CARGA':
            vertexa = data['ORIGEN']
            vertexb = data['DESTINO']
            weight = data['TIEMPO_VUELO']
            model.addFlightCharge(data_structs, vertexa, vertexb, weight)
    return model.data_size_edges(data_structs['carga'])
     
def loadDataFlightComercial(data_structs):
    '''
    Lee el csv de los vuelos y aniade al grafo determinado los vuelos como arcos con el peso en tiempo.
    '''
    filename = os.path.join(cf.data_dir + 'fligths-2022.csv')
    input_file = csv.DictReader(open(filename, encoding='UTF-8'), delimiter=';', restkey='Unknown')
    for data in input_file:
        if data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
            vertexa = data['ORIGEN']
            vertexb = data['DESTINO']
            weight = data['TIEMPO_VUELO']
            model.addFlightComercial(data_structs, vertexa, vertexb, weight)
    return model.data_size_edges(data_structs['comercial'])
     
def loadDataFlightMilitar(data_structs):
    '''
    Lee el csv de los vuelos y aniade al grafo determinado los vuelos como arcos con el peso en tiempo.
    '''
    filename = os.path.join(cf.data_dir + 'fligths-2022.csv')
    input_file = csv.DictReader(open(filename, encoding='UTF-8'), delimiter=';', restkey='Unknown')
    for data in input_file:
        if data['TIPO_VUELO'] == 'MILITAR':
            vertexa = data['ORIGEN']
            vertexb = data['DESTINO']
            weight = data['TIEMPO_VUELO']
            model.addFlightMilitar(data_structs, vertexa, vertexb, weight)
    return model.data_size_edges(data_structs['militar'])

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
