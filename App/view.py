"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
import prettytable as pt
from prettytable import PrettyTable, ALL
assert cf

sys.setrecursionlimit(2 ** 20)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print('1- Inicializar Analizador')
    print('2- Cargar información en el catálogo')
    print('3- Requerimiento 1')
    print('4- Requerimiento 2')
    print('5- Requerimiento 3')
    print('6- Requerimiento 4')
    print('7- Requerimiento 5')
    print('8- Requerimiento 6')
    print('9- Requerimiento 7')
    print('0- Salir')
    print("*******************************************")

routesfile = 'routes-utf8-small.csv'
airportsfile = 'airports-utf8-small.csv'
cityfile = 'worldcities-utf8.csv'
cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.Init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de aeropuertos y rutas ....")
        controller.loadData(cont, routesfile, airportsfile, cityfile)

        numvertex = controller.totalAirports(cont)
        numedges = controller.totalConnections(cont)

        numvertex2 = controller.totalAirports2(cont)
        numedges2 = controller.totalConnections2(cont)

        airports = controller.TotalAirports(cont)

        ciudades = controller.TotalCiudades(cont)

        print('Número de aeropuertos en el dígrafo: ' + str(numvertex))
        print('Número de rutas aereas en el dígrafo: ' + str(numedges))
        print('\n')

        print('Número de aeropuertos en el grafo no dirigido: ' + str(numvertex2))
        print('Número de rutas aereas en el grafo no dirigido: ' + str(numedges2))
        print('\n')

        print('El total de ciudades cargadas es: ' + str(ciudades[0]) + ' y los datos de la última ciudad cargada son: ')
        print(ciudades[1])
        print('\n')

        print('El total de aeropuertos cargados es: ' + str(airports[0]) + ' y los datos del primer aeropuerto cargado son: ')
        print(airports[1])
        print('\n')

        print('El limite de recursion actual es: ' + str(sys.getrecursionlimit()))

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        ciudadO= input('dar nombre de la ciudad de origen que se desea consultar')
        listaHomonimos=controller.getCity(cont,ciudadO)
        tablaO = pt.PrettyTable(['index','city', 'latitud', 'longitud', 'country'])
        tablaO.max_width = 8

        for i in range(1,lt.size(listaHomonimos)+1):
            city = lt.getElement(listaHomonimos,i)
            tablaO.add_row([i,city['city'], city['lat'], city['lng'], city['country']])
        tablaO.hrules = ALL
        print(tablaO)

        indice=input('Seleccione la ciudad que desea utilizando el numero de indice')
        ciudadOElegida= lt.getElement(listaHomonimos, int(indice))
        print('la ciudad elegida es: ' )

        tablaOE = pt.PrettyTable(['city', 'latitud', 'longitud', 'country', 'iso2', 'iso3'])
        tablaO.max_width = 8
        tablaOE.add_row([ciudadOElegida['city'], ciudadOElegida['lat'], ciudadOElegida['lng'], ciudadOElegida['country'], ciudadOElegida['iso2'], ciudadOElegida['iso3'] ])
        tablaOE.hrules = ALL
        print(tablaOE)

        ##Ciudad destino

        ciudadD= input('dar nombre de la ciudad de destino que se desea consultar')
        listaHomonimos2=controller.getCity(cont,ciudadD)

        tablaD = pt.PrettyTable(['index','city', 'latitud', 'longitud', 'country'])
        tablaD.max_width = 8

        for i in range(1,lt.size(listaHomonimos2)+1):
            city = lt.getElement(listaHomonimos2,i)
            tablaD.add_row([i,city['city'], city['lat'], city['lng'], city['country']])
        tablaD.hrules = ALL
        print(tablaD)

        indice=input('Seleccione la ciudad que desea utilizando el numero de indice')
        ciudadDElegida= lt.getElement(listaHomonimos2, int(indice))
        print('la ciudad elegida es: ' )

        tablaDE = pt.PrettyTable(['city', 'latitud', 'longitud', 'country', 'iso2', 'iso3'])
        tablaD.max_width = 8
        tablaDE.add_row([ciudadOElegida['city'], ciudadOElegida['lat'], ciudadOElegida['lng'], ciudadOElegida['country'], ciudadOElegida['iso2'], ciudadOElegida['iso3'] ])
        tablaDE.hrules = ALL
        print(tablaDE)



    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 8:
        pass

    elif int(inputs[0]) == 9:
        pass

    else:
        sys.exit(0)
sys.exit(0)
