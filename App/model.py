﻿"""
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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#========================
# Construccion de modelos
#========================
def newAnalyzer():
    analyzer = {'routes': None,
                'airports': None,
                'noDirigido': None
                }

    analyzer['routes'] = gr.newGraph(datastructure = 'ADJ_LIST', 
                                     directed = True,
                                     size = 4000,
                                     comparefunction = cmpRouteIds)

    analyzer['noDirigido'] = gr.newGraph(datastructure = 'ADJ_LIST', 
                                         directed = False,
                                         size = 4000,
                                         comparefunction = cmpRouteIds)

    analyzer['airports'] = mp.newMap(maptype = 'PROBING',
                                     loadfactor = 0.5,
                                     comparefunction = cmpMapAirport)

    return analyzer

#===============================================
# Funciones para agregar informacion al catalogo
#===============================================
def addRoute(analyzer, route):
    if not gr.containsVertex(analyzer['routes'], route['Departure']):
        gr.insertVertex(analyzer['routes'], route['Departure'])

    if not gr.containsVertex(analyzer['routes'], route['Destination']):
        gr.insertVertex(analyzer['routes'], route['Destination'])
    
    return analyzer

def addConnection(analyzer, route):
    edge = gr.getEdge(analyzer['routes'], route['Departure'], route['Destination'])
    if edge is None:
        gr.addEdge(analyzer['routes'], route['Departure'], route['Destination'], route['distance_km'])
    
    return analyzer

def addRouteConnectionND(analyzer, route):
    aero1 = route['Departure']
    aero2 = route['Destination']

    arco1 = gr.getEdge(analyzer['routes'], aero1, aero2)
    arco2 = gr.getEdge(analyzer['routes'], aero2, aero1)

    if (arco1 != None) and (arco2 != None):
        if not gr.containsVertex(analyzer['noDirigido'], aero1):
            gr.insertVertex(analyzer['noDirigido'], aero1)

        if not gr.containsVertex(analyzer['noDirigido'], aero2):
            gr.insertVertex(analyzer['noDirigido'], aero2)
        
        gr.addEdge(analyzer['noDirigido'], aero1, aero2, 0)

    return analyzer

def generateGraph(analyzer):
    vertices = gr.vertices(analyzer['routes'])
    i = 0

    while i < lt.size(vertices):
        aero1 = lt.getElement(vertices, i)
        j = i + 1

        while j <= lt.size(vertices):
            aero2 = lt.getElement(vertices, j)
            
            arco1 = gr.getEdge(analyzer['routes'], aero1, aero2)
            arco2 = gr.getEdge(analyzer['routes'], aero2, aero1)

            if arco1 != None and arco2 != None:
                if not gr.containsVertex(analyzer['noDirigido'], aero1):
                    gr.insertVertex(analyzer['noDirigido'], aero1)

                if not gr.containsVertex(analyzer['noDirigido'], aero2):
                    gr.insertVertex(analyzer['noDirigido'], aero2)

                gr.addEdge(analyzer['noDirigido'], aero1, aero2, 0)

            j += 1
        i += 1
    
    return analyzer

#=================================
# Funciones para creacion de datos
#=================================

#======================
# Funciones de consulta
#======================
def totalAirports(analyzer):

    return gr.numVertices(analyzer['routes'])

def totalConnections(analyzer):

    return gr.numEdges(analyzer['routes'])

def totalAirports2(analyzer):

    return gr.numVertices(analyzer['noDirigido'])

def totalConnections2(analyzer):

    return gr.numEdges(analyzer['noDirigido'])

#=================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
#=================================================================
def cmpRouteIds(route, keyvalueroute):
    routecode = keyvalueroute['key']
    if (route == routecode):
        return 0
    elif (route > routecode):
        return 1
    else:
        return -1

def cmpMapAirport(keyname, airport):
    airport_entry = me.getKey(airport)
    if (keyname == airport_entry):
        return 0
    elif (keyname > airport_entry):
        return 1
    else:
        return -1

#==========================
# Funciones de ordenamiento
#==========================
