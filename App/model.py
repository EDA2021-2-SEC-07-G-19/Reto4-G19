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
import math as mt
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import edge as ed
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import gr, outdegree
import DISClib.ADT.indexminpq as pq
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
                'lt_ciudades': None
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
    analyzer['mp_airports'] = mp.newMap(maptype = 'PROBING',
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
    ndedge = gr.getEdge(nd,aero1,aero2)
    if edge1 is not None and edge2 is not None and ndedge is None:
        gr.addEdge(nd, aero1, aero2, distancia)
        

    return analyzer

def addAirportList(analyzer, airport):
    lt.addLast(analyzer['lt_airports'], airport)

def addAirportMap(analyzer, airport):
    mp.put(analyzer['mp_airports'], airport['IATA'],airport)

def addCityList(analyzer, city):
    lt.addLast(analyzer['lt_ciudades'], city)

def addRouteList(analyzer, route):
    lt.addLast(analyzer['lt_routes'], route)

def getRouteList(analyzer):
    return analyzer['lt_routes']

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
def requerimiento1(analyzer):
    lista=analyzer['lt_airports']
    aeropuertos=lt.size(lista)
    mejores5 = pq.newIndexMinPQ(cmpMinPq)
    grafo=analyzer['digrafo']
   
    aeropuerto=lt.getElement(lista, 1)
    degree=gr.degree(grafo, aeropuerto['IATA'])
    pq.insert(mejores5, aeropuerto['IATA'], degree)
    
    for j in range(1, lt.size(lista)+1):
        aeropuerto=lt.getElement(lista, j)
        degree=gr.degree(grafo, aeropuerto['IATA'])
        degree2=gr.degree(grafo, pq.min(mejores5))
        if pq.size(mejores5) < 5:
            pq.insert(mejores5, aeropuerto['IATA'], degree)
        elif degree>degree2: 
            pq.delMin(mejores5)
            pq.insert(mejores5, aeropuerto['IATA'], degree)

    mapa=analyzer['mp_airports']
    listaFinal=lt.newList('SINGLE_LINKED')
    for k in range(1,6):
        aeropuerto= me.getValue(mp.get(mapa, pq.delMin(mejores5)))
        print(aeropuerto)
        indegree=gr.indegree(grafo, aeropuerto['IATA'])
        outdegree=gr.outdegree(grafo, aeropuerto['IATA'])
        aeropuerto['inbound']=indegree
        aeropuerto['outbound']=outdegree
        aeropuerto['conections']=indegree + outdegree
        lt.addFirst(listaFinal,aeropuerto)
    return listaFinal, aeropuertos

def requerimiento2(analyzer, codigo1, codigo2):
    grafo=analyzer['digrafo']
    clusters = scc.KosarajuSCC(grafo)
    cluster=scc.connectedComponents(clusters)
    connected=scc.stronglyConnected(clusters, codigo1, codigo2)

    return cluster, connected

def requerimiento3(analyzer, ciudadO, ciudadD):
    lat1= float(ciudadO['lat'])
    lon1=float(ciudadO['lng'])
    lat2= float(ciudadD['lat'])
    lon2=float(ciudadD['lng'])
    aeropuerto1=aeropuertoMasCercano(analyzer,lat1,lon1)
    aeropuerto2=aeropuertoMasCercano(analyzer,lat2,lon2)
    grafo=analyzer['digrafo']
    path=djk.Dijkstra(grafo, aeropuerto1['IATA'])
    distanceTo=djk.distTo(path, aeropuerto2['IATA'])

    paradas= djk.pathTo(path, aeropuerto2['IATA'])

    aeropuertos= lt.newList('ARRAY_LIST')
    lt.addLast(aeropuertos, aeropuerto1)
    for i in range(1, lt.size(paradas)+1):
        parada=lt.getElement(paradas, i)
        
        destino=lt.getElement(aeropuertos, i)
        parada2= ed.other(parada, ed.either(parada))
        aeropuerto=me.getValue(mp.get(analyzer['mp_airports'],parada2))
        lt.addLast(aeropuertos, aeropuerto)

    print(aeropuertos)

    return aeropuerto1, aeropuerto2, distanceTo, paradas, aeropuertos


def aeropuertoMasCercano(analyzer,lat1,lon1):
    aeropuertoMinimo=None
    kilometrajeActual=10

    while aeropuertoMinimo is None: 
        lista= analyzer['lt_airports']
        menorKilometraje=100000000000000
        for i in range(1, lt.size(lista)+1):
            aeropuerto=lt.getElement(lista, i)
            lat2=float(aeropuerto['Latitude'])
            lon2=float(aeropuerto['Longitude'])
            distancia=formulaHaversine(lat1, lat2, lon1, lon2)
            if distancia<kilometrajeActual and distancia<menorKilometraje:
                aeropuertoMinimo=aeropuerto
                menorKilometraje=distancia
        kilometrajeActual+=10


    return aeropuertoMinimo

def formulaHaversine(lat1, lat2, lon1, lon2):
    lat1r= (lat1*mt.pi)/180
    lat2r= (lat2*mt.pi)/180
    diflat=(lat2-lat1)/2
    diflon=(lon2-lon1)/2
    diflatr=(diflat*mt.pi)/180
    diflonr=(diflon*mt.pi)/180
    a=mt.asin((((mt.sin(diflatr))**2)+mt.cos(lat2r)*mt.cos(lat1r)*((mt.sin(diflonr))**2))**(1/2))
    distancia=2*a*3958.8

    return distancia


def Requerimiento4(analyzer, ciudad, millas):
    digraph = analyzer['nodirigido']
    estruc_prim = prim.PrimMST(digraph)
    total_distancia = round(prim.weightMST(digraph, estruc_prim), 2)
    total_millas_km = round(millas*1.6, 2)
    rec_dfs = dfs.DepthFirstSearch(digraph, ciudad)
    visitados = rec_dfs['visited']
    keyset_visitados = mp.keySet(visitados)

    mayor = 0
    for iata in lt.iterator(keyset_visitados):
        camino = dfs.pathTo(rec_dfs, iata)
        tam = lt.size(camino)
        if tam > mayor:
            lt_rta = camino
            mayor = tam
    airports_c = lt.size(keyset_visitados)
    lt_rta = getDataIATAList2(analyzer, lt_rta)
    distancia_camino = 0

    for edge in lt.iterator(lt_rta):
        distancia = edge['weight']
        distancia_camino += distancia

    distancia_camino = round(distancia_camino, 2)
    
    millas_f1 = 0
    millas_f2 = 0
    if total_millas_km < distancia_camino:
        millas_f1 = round((distancia_camino - total_millas_km)/1.6,2)

    else:
        millas_f2 = round((total_millas_km - distancia_camino)/1.6, 2)

    return airports_c, total_distancia, total_millas_km, distancia_camino, millas_f1, millas_f2, lt_rta
def Requerimiento5(analyzer, ciudad):
    digraph = analyzer['digrafo']
    adyacentes = gr.adjacents(digraph, ciudad)
    total_afectados = lt.size(adyacentes)

    primeros_3 = lt.newList(datastructure = 'ARRAY_LIST')
    ultimos_3 = lt.newList(datastructure = 'ARRAY_LIST')

    if total_afectados <= 6:
        primeros_3 = adyacentes

    else:
        i = 1
        while i <= 3:
            x = lt.getElement(adyacentes, i)
            lt.addLast(primeros_3, x)
            i += 1

        j = 2
        while j >= 0:
            x = lt.getElement(adyacentes, total_afectados - j)
            lt.addLast(ultimos_3, x)
            j -= 1

    return primeros_3, ultimos_3, total_afectados

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

def getDataIATAList(analyzer, lista_iata):
    lt_rta = lt.newList(datastructure = 'ARRAY_LIST')
    lt_airports = analyzer['lt_airports']
    tam_lt_airports = lt.size(lt_airports)
    lista_iata = ms.sort(lista_iata, cmpAirportsAlfa)
    
    for iata in lt.iterator(lista_iata): 
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
def getDataIATAList2(analyzer, lista_iata):
    nd = analyzer['nodirigido']
    tam_lt_iata = lt.size(lista_iata)
    lt_rta = lt.newList(datastructure = 'ARRAY_LIST')

    i = 1
    j = 2
    while i <= (tam_lt_iata-1) and j <= tam_lt_iata:
        vertexa = lt.getElement(lista_iata, i)
        vertexb = lt.getElement(lista_iata, j)
        edge = gr.getEdge(nd, vertexa, vertexb)
        lt.addLast(lt_rta, edge)

        i += 1
        j += 1

    return lt_rta
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
    total_routes = lt.size(lt_routes)
    return total_routes

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

def cmpAirportsAlfa(iata1, iata2):
    if iata1 == iata2:
        return 0
    elif iata1 < iata2:
        return 1
    else:
        return 0
def cmpMinPq(iata1, iata2):
    return True
