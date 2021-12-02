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
        model.addAirport(analyzer, airport)
        model.addAirportList(analyzer, airport)

    return analyzer

def loadDataRoutes(analyzer, routesfile):
    routesfile = cf.data_dir + routesfile
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    
    for route in input_file:
        model.addRoute(analyzer, route)
        model.addAirportRouteND(analyzer, route)

    return analyzer

def loadDataCiudades(analyzer, cityfile):
    cityfile = cf.data_dir + cityfile
    input_file = csv.DictReader(open(cityfile, encoding="utf-8"))

    for city in input_file:
        model.addCity(analyzer, city['city'], city)
        model.addCity2(analyzer, city)

    return analyzer

#==========================
# Funciones de ordenamiento
#==========================

#========================================
# Funciones de consulta sobre el catálogo
#========================================
def totalAirports(analyzer):

    return model.totalAirports(analyzer)

def totalConnections(analyzer):

    return model.totalConnections(analyzer)

def totalAirports2(analyzer):

    return model.totalAirports2(analyzer)

def totalConnections2(analyzer):

    return model.totalConnections2(analyzer)

def TotalAirports(map_airports):

    return model.TotalAirports(map_airports)

def TotalCiudades(analyzer):

    return model.TotalCiudades(analyzer)

def getCity(analyzer, city):
    
    return model.getCity(analyzer, city)