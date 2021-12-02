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

    return analyzer

#===============================================
# Funciones para agregar informacion al catalogo
#===============================================
def addAirport(analyzer, airport):
    if not gr.containsVertex(analyzer['digrafo'], airport['IATA']):
        gr.insertVertex(analyzer['digrafo'], airport['IATA'])

    if not gr.containsVertex(analyzer['nodirigido'], airport['IATA']):
        gr.insertVertex(analyzer['nodirigido'], airport['IATA'])
    
    return analyzer

def addRoute(analyzer, route):
    gr.addEdge(analyzer['digrafo'], route['Departure'], route['Destination'], route['distance_km'])
    
    return analyzer

def addAirportRouteND(analyzer, route):
    aero1 = route['Departure']
    aero2 = route['Destination']

    arco1 = gr.getEdge(analyzer['digrafo'], aero1, aero2)
    arco2 = gr.getEdge(analyzer['digrafo'], aero2, aero1)

    if (arco1 != None) and (arco2 != None):     
        gr.addEdge(analyzer['nodirigido'], aero1, aero2, 0)

    return analyzer

def addAirportList(analyzer, airport):
    lt.addLast(analyzer['lt_airports'], airport)

def addCity2(analyzer, city):
    lt.addLast(analyzer['lt_ciudades'], city)

def addCity(analyzer, ciudad, ciudadUnica):
    ciudades = analyzer['ciudades']
    existe = mp.contains(ciudades, ciudad)
    if existe:
        dupla = mp.get(ciudades, ciudad)
        ciudad_actual = me.getValue(dupla)
    else:
        ciudad_actual = lt.newList("ARRAY_LIST")
        mp.put(ciudades, ciudad, ciudad_actual)
    lt.addLast(ciudad_actual, ciudadUnica)

    return 

#=================================
# Funciones para creacion de datos
#=================================

#======================
# Funciones de consulta
#======================
def totalAirports(analyzer):

    return gr.numVertices(analyzer['digrafo'])

def totalConnections(analyzer):

    return gr.numEdges(analyzer['digrafo'])

def totalAirports2(analyzer):

    return gr.numVertices(analyzer['nodirigido'])

def totalConnections2(analyzer):

    return gr.numEdges(analyzer['nodirigido'])

def getCity(analyzer, city):
    
    return me.getValue(mp.get(analyzer['ciudades'],city))

def TotalAirports(analyzer):
    lt_airports = analyzer['lt_airports']
    total_airports = lt.size(lt_airports)
    primer_airport = lt.getElement(lt_airports, 1)

    return total_airports, primer_airport

def TotalCiudades(analyzer):
    lt_ciudades = analyzer['lt_ciudades']
    total_ciudades = lt.size(lt_ciudades)
    ultima_ciudad = lt.getElement(lt_ciudades, total_ciudades)

    return total_ciudades, ultima_ciudad

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


