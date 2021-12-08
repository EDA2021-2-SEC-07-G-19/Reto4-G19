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
import csv
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
#======================================
# Inicialización del Catálogo de libros
#======================================
def Init():
    analyzer = model.newAnalyzer()
    
    return analyzer

#=================================
# Funciones para la carga de datos
#=================================
def loadData(analyzer, routesfile, airportsfile, cityfile):
    loadDataAirports(analyzer, airportsfile)
    loadDataRoutes(analyzer, routesfile)
    loadDataCiudades(analyzer, cityfile)

def loadDataAirports(analyzer, airportsfile):
    airportsfile = cf.data_dir + airportsfile
    input_file = csv.DictReader(open(airportsfile, encoding="utf-8"))

    for airport in input_file:
        model.addAirportGraphs(analyzer, airport)
        model.addAirportList(analyzer, airport)
        model.addAirportMap(analyzer, airport)

    return analyzer

def loadDataRoutes(analyzer, routesfile):
    routesfile = cf.data_dir + routesfile
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    
    for route in input_file:
        model.addRouteDiGraph(analyzer, route)
        model.addRouteList(analyzer, route)

    rutas = model.getRouteList(analyzer)
    for ruta in lt.iterator(rutas):
        model.addAirportRouteND(analyzer, ruta)
        

    return analyzer

def loadDataCiudades(analyzer, cityfile):
    cityfile = cf.data_dir + cityfile
    input_file = csv.DictReader(open(cityfile, encoding="utf-8"))

    for city in input_file:
        model.addCityMap(analyzer, city['city'], city)
        model.addCityList(analyzer, city)

    return analyzer

#==========================
# Funciones de ordenamiento
#==========================

#========================================
# Funciones de consulta sobre el catálogo
#========================================
def getVerticesDiGraph(analyzer):

    return model.getVerticesDiGraph(analyzer)

def getVerticesGraph(analyzer):

    return model.getVerticesGraph(analyzer)

def getDataIATA(analyzer, iata):

    return model.getDataIATA(analyzer, iata)

def getDataIATAList(analyzer, lista_iata):

    return model.getDataIATAList(analyzer, lista_iata)

def getCity(analyzer, city):
    
    return model.getCity(analyzer, city)

def TotalVerticesDiGraph(analyzer):

    return model.TotalVerticesDiGraph(analyzer)

def TotalEdgesDiGraph(analyzer):

    return model.TotalEdgesDiGraph(analyzer)

def TotalVerticesGraph(analyzer):

    return model.TotalVerticesGraph(analyzer)

def TotalEdgesGraph(analyzer):

    return model.TotalEdgesGraph(analyzer)

def TotalCiudades(analyzer):

    return model.TotalCiudades(analyzer)

def TotalRoutesDiGraph(analyzer):

    return model.TotalRoutesDiGraph(analyzer)

def requerimiento1(analyzer):

    mejores5=model.requerimiento1(analyzer)
    
    return mejores5

def requerimiento2(analyzer, codigo1, codigo2):

    informacion=model.requerimiento2(analyzer, codigo1, codigo2)

    return informacion

def Requerimiento4(analyzer, ciudad, millas):

    return model.Requerimiento4(analyzer, ciudad, millas)

def Requerimiento5(analyzer, ciudad):

    return model.Requerimiento5(analyzer, ciudad)
