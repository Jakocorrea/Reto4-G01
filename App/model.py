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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def newAnalyzer():
    """Inicializa el analizador

    airports: Tabla de hash para guardar los vértices del grafo
    connections: Grafo para representar las rutas entre aeropuertos
    components: Almacena la información de los componentes conectados
    paths: Estructura que almacena los caminos de costo mínimo desde un
           vértice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'airports': None,
            'connections': None,
            'components': None,
            'paths': None
        }

        analyzer['airports'] = m.newMap(numelements=14000,
                                        maptype='PROBING',
                                        cmpfunction=compareAirportIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAirportIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


def addAirportConnection(analyzer, lastflight, flight):
    """
    Adiciona los aeropuertos y vuelos al grafo como vértices y arcos entre ellos.

    Los vértices tienen por nombre el identificador del aeropuerto
    seguido del número de vuelo. Por ejemplo:

    JFK-UA123

    Si el aeropuerto sirve otro vuelo, se tiene: JFK-UA456
    """
    try:
        origin = formatAirport(lastflight)
        destination = formatAirport(flight)
        cleanFlightDistance(lastflight, flight)
        distance = float(flight['Distance']) - float(lastflight['Distance'])
        distance = abs(distance)
        addAirport(analyzer, origin)
        addAirport(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        addFlight(analyzer, flight)
        addFlight(analyzer, lastflight)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportConnection')


def addAirport(analyzer, airportid):
    """
    Adiciona un aeropuerto como un vértice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], airportid):
            gr.insertVertex(analyzer['connections'], airportid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')


def addFlight(analyzer, flight):
    """
    Agrega un vuelo a la lista de vuelos servidos en un aeropuerto específico
    """
    try:
        airport_code = flight['ORIGEN']
        entry = m.get(analyzer['airports'], airport_code)
        if entry is None:
            flight_list = lt.newList(cmpfunction=compareflights)
            lt.addLast(flight_list, flight)
            m.put(analyzer['airports'], airport_code, flight_list)
        else:
            flight_list = entry['value']
            lt.addLast(flight_list, flight)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addFlight')


def addRouteConnections(analyzer):
    """
    Por cada vértice (cada aeropuerto) se recorre la lista
    de vuelos servidos en dicho aeropuerto y se crean
    arcos entre ellos para representar la conexión entre vuelos
    """
    try:
        airport_keys = m.keySet(analyzer['airports'])
        for airport_code in lt.iterator(airport_keys):
            flight_list = m.get(analyzer['airports'], airport_code)['value']
            for i in range(lt.size(flight_list) - 1):
                flight1 = lt.getElement(flight_list, i)
                flight2 = lt.getElement(flight_list, i + 1)
                addConnection(analyzer, formatAirport(flight1), formatAirport(flight2), 0)
                addConnection(analyzer, formatAirport(flight2), formatAirport(flight1), 0)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addRouteConnections')


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona una conexión entre dos aeropuertos
    """
    try:
        edge = gr.getEdge(analyzer['connections'], origin, destination)
        if edge is None:
            gr.addEdge(analyzer['connections'], origin, destination, distance)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addConnection')

def formatAirport(flight):
    """
    Formatea el nombre del vértice con el código del aeropuerto
    seguido del número de vuelo.
    """
    name = flight['ORIGEN'] + '-'  # Usamos el código del aeropuerto como parte del nombre del vértice
    name += flight['TIPO_VUELO']  # Usamos el tipo de vuelo como parte del nombre del vértice
    return name

def cleanFlightDistance(lastflight, flight):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if flight['TIEMPO_VUELO'] == '':
        flight['TIEMPO_VUELO'] = 0
    if lastflight['TIEMPO_VUELO'] == '':
        lastflight['TIEMPO_VUELO'] = 0
        
def compareflights(flight1, flight2):
    """
    Compara dos vuelos por sus rutas
    """
    if flight1['TIPO_VUELO'] == flight2['TIPO_VUELO']:
        return 0
    elif flight1['TIPO_VUELO'] > flight2['TIPO_VUELO']:
        return 1
    else:
        return -1
    
def compareAirportIds(airport_id, airport_info):
    """
    Compara dos aeropuertos por sus identificadores
    """
    airport_code = airport_info['NOMBRE']
    if airport_id == airport_code:
        return 0
    elif airport_id > airport_code:
        return 1
    else:
        return -1

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
