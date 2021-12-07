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
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
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
    analyzer = {'digrafo': None,
                'nodirigido': None,
                'airports': None,
                'ciudades': None,
                'lt_airports': None,
                'lt_ciudades': None,
                }

    analyzer['digrafo'] = gr.newGraph(datastructure = 'ADJ_LIST', 
                                     directed = True,
                                     size = 4000,
                                     comparefunction = cmpRouteIds)

    analyzer['nodirigido'] = gr.newGraph(datastructure = 'ADJ_LIST', 
                                         directed = False,
                                         size = 4000,
                                         comparefunction = cmpRouteIds)

    analyzer['airports'] = mp.newMap(maptype = 'PROBING',
                                     loadfactor = 0.5,
                                     comparefunction = cmpMapAirport)
    
    analyzer['ciudades'] = mp.newMap(maptype = 'PROBING',
                                   loadfactor = 0.5,
                                   comparefunction = cmpMapCiudades)

    analyzer['lt_airports'] = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmpListIATA)
    
    analyzer['lt_ciudades'] = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmpListCity)

    analyzer['lt_routes'] = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmpListRoute)

    return analyzer

#=================================================
# Funciones para agregar informacion al analizador
#=================================================
def addAirportGraphs(analyzer, airport):
    if not gr.containsVertex(analyzer['digrafo'], airport['IATA']):
        gr.insertVertex(analyzer['digrafo'], airport['IATA'])

    if not gr.containsVertex(analyzer['nodirigido'], airport['IATA']):
        gr.insertVertex(analyzer['nodirigido'], airport['IATA'])
    
    return analyzer

def addRouteDiGraph(analyzer, route):
    edge = gr.getEdge(analyzer['digrafo'], route['Departure'], route['Destination'])
    if edge == None:
        distance = float(route['distance_km'])
        gr.addEdge(analyzer['digrafo'], route['Departure'], route['Destination'], distance)
    
    return analyzer

def addAirportRouteND(analyzer, route):
    digraph = analyzer['digrafo']
    nd = analyzer['nodirigido']
    aero1 = route['Departure']
    aero2 = route['Destination']
    distancia = float(route['distance_km'])

    edge1 = gr.getEdge(digraph, aero1, aero2)
    edge2 = gr.getEdge(digraph, aero2, aero1)

    if edge1 is not None and edge2 is not None:
        gr.addEdge(nd, aero1, aero2, distancia)

    return analyzer

def addAirportList(analyzer, airport):
    lt.addLast(analyzer['lt_airports'], airport)

def addCityList(analyzer, city):
    lt.addLast(analyzer['lt_ciudades'], city)

def addRouteList(analyzer, route):
    lt.addLast(analyzer['lt_routes'], route)

def addCityMap(analyzer, ciudad, ciudadUnica):
    ciudades = analyzer['ciudades']
    existe = mp.contains(ciudades, ciudad)
    if existe:
        dupla = mp.get(ciudades, ciudad)
        ciudad_actual = me.getValue(dupla)
    else:
        ciudad_actual = lt.newList("ARRAY_LIST")
        mp.put(ciudades, ciudad, ciudad_actual)
    lt.addLast(ciudad_actual, ciudadUnica)

    return ciudades

#=================================
# Funciones para creacion de datos
#=================================
def Requerimiento4(analyzer, ciudad, millas):
    digraph = analyzer['nodirigido']
    estruc_prim = prim.PrimMST(digraph)
    total_distancia = round(prim.weightMST(digraph, estruc_prim), 2)
    total_millas_km = round(millas*1.6, 2)

    return total_distancia, total_millas_km

#======================
# Funciones de consulta
#======================
def getVerticesDiGraph(analyzer):
    digraph = analyzer['digrafo']
    vertices = gr.vertices(digraph)
    tam_vertices = lt.size(vertices)
    prim_ult = lt.newList(datastructure = 'ARRAY_LIST')
    prim = lt.getElement(vertices, 0)
    lt.addLast(prim_ult, prim)
    ult = lt.getElement(vertices, tam_vertices)
    lt.addLast(prim_ult, ult)

    lt_airports = analyzer['lt_airports']
    tam_lt_airports = lt.size(lt_airports)
    lt_rta = lt.newList(datastructure = 'ARRAY_LIST')
    for iata in lt.iterator(prim_ult):
        i = 0
        encontrar = False
        while i < tam_lt_airports and encontrar == False:
            airport = lt.getElement(lt_airports, i)
            iata2 = airport['IATA']
            if str(iata) == str(iata2):
                lt.addLast(lt_rta, airport)
                encontrar = True
            
            i += 1

    return lt_rta

def getVerticesGraph(analyzer):
    graph = analyzer['nodirigido']
    vertices = gr.vertices(graph)
    tam_vertices = lt.size(vertices)
    prim_ult = lt.newList(datastructure = 'ARRAY_LIST')
    prim = lt.getElement(vertices, 0)
    lt.addLast(prim_ult, prim)
    ult = lt.getElement(vertices, tam_vertices)
    lt.addLast(prim_ult, ult)

    lt_airports = analyzer['lt_airports']
    tam_lt_airports = lt.size(lt_airports)
    lt_rta = lt.newList(datastructure = 'ARRAY_LIST')
    for iata in lt.iterator(prim_ult):
        i = 0
        encontrar = False
        while i < tam_lt_airports and encontrar == False:
            airport = lt.getElement(lt_airports, i)
            iata2 = airport['IATA']
            if str(iata) == str(iata2):
                lt.addLast(lt_rta, airport)
                encontrar = True
            
            i += 1

    return lt_rta

def getDataIATA(analyzer, iata):
    i = 0
    encontrar = False
    lt_airports = analyzer['lt_airports']
    tam_lt_airports = lt.size(lt_airports)

    while i < tam_lt_airports and encontrar == False:
        airport = lt.getElement(lt_airports, i)
        iata2 = airport['IATA']
        if str(iata) == str(iata2):
            rta = airport
            encontrar = True
        
        i += 1

    return rta

def getCity(analyzer, city):
    
    return me.getValue(mp.get(analyzer['ciudades'],city))

def TotalVerticesDiGraph(analyzer):

    return gr.numVertices(analyzer['digrafo'])

def TotalEdgesDiGraph(analyzer):

    return gr.numEdges(analyzer['digrafo'])

def TotalVerticesGraph(analyzer):

    return gr.numVertices(analyzer['nodirigido'])

def TotalEdgesGraph(analyzer):

    return gr.numEdges(analyzer['nodirigido'])

def TotalCiudades(analyzer):
    lt_ciudades = analyzer['lt_ciudades']
    total_ciudades = lt.size(lt_ciudades)
    primera_ciudad = lt.getElement(lt_ciudades, 1)
    ultima_ciudad = lt.getElement(lt_ciudades, total_ciudades)
    lt_rta = lt.newList(datastructure = 'ARRAY_LIST')
    lt.addLast(lt_rta, primera_ciudad)
    lt.addLast(lt_rta, ultima_ciudad)

    return total_ciudades, lt_rta

def TotalRoutesDiGraph(analyzer):
    lt_routes = analyzer['lt_routes']
    total_routes = lt.size(lt_routes)

    return total_routes

def TotalRoutesGraph(analyzer):
    lt_routes = analyzer['lt_routes']

    return

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

def cmpMapCiudades(keyname, airport):
    airport_entry = me.getKey(airport)
    if (keyname == airport_entry):
        return 0
    elif (keyname > airport_entry):
        return 1
    else:
        return -1

def cmpListIATA(iata1, iata2):
    if (iata1 == iata2):
        return 0
    elif (iata1 > iata2):
        return 1
    else:
        return -1

def cmpListCity(city1, city2):
    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1

def cmpListRoute(route1, route2):
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


