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
            'airport': None,
            'comercial': None,
            'carga': None,
            'militar': None,
        }
        
        analyzer['airport'] = mp.newMap(numelements=1000,
                                        maptype='PROBING',
                                        loadfactor=0.5,
                                        cmpfunction=None)
        
        analyzer['comercial'] = gr.newGraph(datastructure='ADJ_LIST', 
                                            directed=True,
                                            size=3022,
                                            cmpfunction=None)
        
        analyzer['carga'] = gr.newGraph(datastructure='ADJ_LIST', 
                                            directed=True,
                                            size=3022,
                                            cmpfunction=None)
        
        analyzer['militar'] = gr.newGraph(datastructure='ADJ_LIST', 
                                            directed=True,
                                            size=3022,
                                            cmpfunction=None)
    
        return analyzer
        
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

#Funciones para cargar vertices.

def addAirportNode(analyzer, data):
    '''
    Vuelve cada aeropuerto una tabla de hash con llave el codigo ICAO.
    '''
    if not mp.contains(analyzer['airport'], data['ICAO']):
        newlst = lt.newList()
        lt.addLast(newlst, data)
        mp.put(analyzer['airport'], data['ICAO'], newlst)
    else:
        lst = me.getValue(mp.get(analyzer['airport'], data['ICAO']))
        lt.addLast(lst, data)
    

def addAirportCharge(analyzer, airportid):
    """
    Adiciona un aeropuerto como un vértice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['carga'], airportid):
            gr.insertVertex(analyzer['carga'], airportid)
        
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportCharge')

def addAirportComercial(analyzer, airportid):
    """
    Adiciona un aeropuerto como un vértice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['comercial'], airportid):
            gr.insertVertex(analyzer['comercial'], airportid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportComercial')


def addAirportMilitar(analyzer, airportid):
    """
    Adiciona un aeropuerto como un vértice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['militar'], airportid):
            gr.insertVertex(analyzer['militar'], airportid)
            
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportMilitar')
        
#Funciones para cargar vuelos.

def addFlightCharge(analyzer, vertexa, vertexb, weight):
    '''
    Adiciona un vuelo de carga a los aeropuertos.
    '''
    try:
        gr.addEdge(analyzer['carga'], vertexa, vertexb, weight)
        
    except Exception as exp:
        error.reraise(exp, 'model:addFlightCharge')

def addFlightComercial(analyzer, vertexa, vertexb, weight):
    '''
    Adiciona un vuelo comercial a los aeropuertos.
    '''
    try:
        gr.addEdge(analyzer['comercial'], vertexa, vertexb, weight)
        
    except Exception as exp:
        error.reraise(exp, 'model:addFlightComercial')

def addFlightMilitar(analyzer, vertexa, vertexb, weight):
    '''
    Adiciona un vuelo militar a los aeropuertos.
    '''
    try:
        gr.addEdge(analyzer['militar'], vertexa, vertexb, weight)
        
    except Exception as exp:
        error.reraise(exp, 'model:addFlightMilitar')
    
#Funciones de comparacion.
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


def data_size_vertex(data_structs):
    """
    Retorna el numero de vertices en un grafo.
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return gr.numVertices(data_structs)

def data_size_edges(data_structs):
    '''
    Retorna el numero de arcos en un grafo.
    '''
    return gr.numEdges(data_structs)

def data_size_map(data_structs):
    '''
    Retorna el tamanio de un mapa.
    '''
    return mp.size(data_structs)

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
