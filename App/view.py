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
import time
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
        print('\nCargando información de aeropuertos y rutas ....')
        print('\n')

        start_time = time.process_time()

        controller.loadData(cont, routesfile, airportsfile, cityfile)

        stop_time = time.process_time()

        elapsed_time_mseg = round((stop_time - start_time)*1000,2)

        print('El tiempo de procesamiento de la carga de datos es: ' + str(elapsed_time_mseg) + ' ms' + '\n')

        print('=== Airports-Routes DiGraph ===')
        numvertex = controller.TotalVerticesDiGraph(cont)
        print('Nodes: ' + str(numvertex) + ' loaded airports.')
        numedges = controller.TotalEdgesDiGraph(cont)
        print('Edges: ' + str(numedges) + ' loaded edges.')
        numroutes = controller.TotalRoutesDiGraph(cont)
        print('Routes: ' + str(numroutes) + ' loaded routes.')
        print('First & Last Airport loaded in DiGraph.')

        tabla1 = pt.PrettyTable(['IATA', 'Name', 'City', 'Country', 'Latitude', 'Longitude'])
        tabla1.max_width = 20
        prim_ult = controller.getVerticesDiGraph(cont)

        for airport in lt.iterator(prim_ult):
            tabla1.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']])

        tabla1.hrules = ALL
        print(tabla1)
        print('\n')

        print('=== Airports-Routes Graph ===')
        numvertex2 = controller.TotalVerticesGraph(cont)
        print('Nodes: ' + str(numvertex2) + ' loaded airports.')
        numedges2 = controller.TotalEdgesGraph(cont)
        print('Edges: ' + str(numedges2) + ' loaded edges.')
        print('First & Last Airport loaded in Graph.')

        tabla1_1 = pt.PrettyTable(['IATA', 'Name', 'City', 'Country', 'Latitude', 'Longitude'])
        tabla1_1.max_width = 20
        prim_ult = controller.getVerticesGraph(cont)

        for airport in lt.iterator(prim_ult):
            tabla1_1.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']])

        tabla1_1.hrules = ALL
        print(tabla1_1)
        print('\n')

        print('=== City Network ===')
        total_ciudades = controller.TotalCiudades(cont)
        print('The number of cities are: ' + str(total_ciudades[0]))
        print('First & Last cities loaded in data structure.')

        tabla1_2 = pt.PrettyTable(['City', 'Country', 'Latitude', 'Longitude', 'Population'])
        tabla1_2.max_width = 20
        prim_ult = controller.TotalCiudades(cont)

        for city in lt.iterator(prim_ult[1]):
            tabla1_2.add_row([city['city'], city['country'], city['lat'], city['lng'], city['population']])

        tabla1_2.hrules = ALL
        print(tabla1_2)
        print('\n')

        print('El limite de recursion actual es: ' + str(sys.getrecursionlimit()))

    elif int(inputs[0]) == 3:
        mejores5=controller.requerimiento1(cont)

        print('=========== Req No.1 Inputs =========')
        print('most connected airpotts in network (top 5)')
        print('=========== Req No.1 Answer =========')
        print('connected airports inside network:   ' + str(mejores5[1]) )
        print('TOP 5 most connected airports...')



        tablaO = pt.PrettyTable(['Name','City', 'Country', 'IATA', 'Conections', 'inbound', 'outbound'])
        tablaO.max_width = 20

        for i in range(1,6):
            aeropuerto = lt.getElement(mejores5[0],i)
            tablaO.add_row([aeropuerto['Name'], aeropuerto['City'], aeropuerto['Country'], aeropuerto['IATA'], aeropuerto['conections'], aeropuerto['inbound'], aeropuerto['outbound']])
        tablaO.hrules = ALL
        print(tablaO)


    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:

        #Ciudad Origen

        ciudadO = input('Dar nombre de la ciudad de origen que se desea consultar: ')
        listaHomonimos = controller.getCity(cont,ciudadO)
        tablaO = pt.PrettyTable(['Index','City', 'Latitude', 'Longitude', 'Country'])
        tablaO.max_width = 20

        for i in range(1,lt.size(listaHomonimos)+1):
            city = lt.getElement(listaHomonimos,i)
            tablaO.add_row([i,city['city'], city['lat'], city['lng'], city['country']])
        tablaO.hrules = ALL
        print(tablaO)

        indice = input('Seleccione la ciudad que desea utilizando el numero de indice: ')
        ciudadOElegida = lt.getElement(listaHomonimos, int(indice))
        print('La ciudad elegida es: ' )

        tablaOE = pt.PrettyTable(['City', 'Latitude', 'Longitude', 'Country', 'iso2', 'iso3'])
        tablaO.max_width = 20
        tablaOE.add_row([ciudadOElegida['city'], ciudadOElegida['lat'], ciudadOElegida['lng'], ciudadOElegida['country'], ciudadOElegida['iso2'], ciudadOElegida['iso3'] ])
        tablaOE.hrules = ALL
        print(tablaOE)

        ##Ciudad destino

        ciudadD = input('Dar nombre de la ciudad de destino que se desea consultar: ')
        listaHomonimos2 = controller.getCity(cont,ciudadD)

        tablaD = pt.PrettyTable(['Index','City', 'Latitude', 'Longitude', 'Country'])
        tablaD.max_width = 20

        for i in range(1,lt.size(listaHomonimos2)+1):
            city = lt.getElement(listaHomonimos2,i)
            tablaD.add_row([i,city['city'], city['lat'], city['lng'], city['country']])
        tablaD.hrules = ALL
        print(tablaD)

        indice=input('Seleccione la ciudad que desea utilizando el numero de indice: ')
        ciudadDElegida= lt.getElement(listaHomonimos2, int(indice))
        print('La ciudad elegida es: ' )

        tablaDE = pt.PrettyTable(['City', 'Latitude', 'Longitude', 'Country', 'iso2', 'iso3'])
        tablaD.max_width = 20
        tablaDE.add_row([ciudadOElegida['city'], ciudadOElegida['lat'], ciudadOElegida['lng'], ciudadOElegida['country'], ciudadOElegida['iso2'], ciudadOElegida['iso3'] ])
        tablaDE.hrules = ALL
        print(tablaDE)

    elif int(inputs[0]) == 6:
        
        ciudad = input('Ingrese la ciudad de origen (su código IATA): ')
        millas = input('Ingrese el número de millas que tiene: ')
        millas = float(millas)
        print('\n')

        start_time = time.process_time()

        requerimiento4 = controller.Requerimiento4(cont, ciudad, millas)

        stop_time = time.process_time()

        elapsed_time_mseg = round((stop_time - start_time)*1000,2)

        print('El tiempo de procesamiento del requerimiento elegido es: ' + str(elapsed_time_mseg) + ' ms' + '\n')

        print('=============== Req No. 4 Inputs ===============')
        print('Departure IATA Code: ' + str(ciudad))
        print('Available trave miles: ' + str(millas) + '\n')

        print('=============== Req No. 4 Answer ===============')
        print('+++ Departure Airport for IATA Code: ' + str(ciudad) + ' +++')

        tabla1_req4 = pt.PrettyTable(['IATA', 'Name', 'City', 'Country'])
        tabla1_2.max_width = 20
        airport = controller.getDataIATA(cont, ciudad)
        tabla1_req4.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country']])
        tabla1_req4.hrules = ALL
        print(tabla1_req4)
        print('\n')

        print('- Number of possible airports: ' + str(requerimiento4[0]))
        print('- Max traveling distance between airports: ' + str(requerimiento4[1]) + ' (km)')
        print('- Passenger available traveling miles: ' + str(requerimiento4[2]) + ' (km)')
        print('\n')

        print('+++ Longest possible route with airport ' + str(ciudad) + ' +++')
        print('- Longest possible path distance: ' + str(requerimiento4[3]) + ' (km)')
        print('- Longest possible path details:')

        tabla2_req4 = pt.PrettyTable(['Departure', 'Destination', 'Distance (km)'])
        tabla2_req4.max_width = 20

        rutas = requerimiento4[6]
        for ruta in lt.iterator(rutas):
            tabla2_req4.add_row([ruta['vertexA'], ruta['vertexB'], ruta['weight']])

        tabla2_req4.hrules = ALL
        print(tabla2_req4)
        print('\n')

        if requerimiento4[5] > 0:
            print('The passenger has left ' + str(requerimiento4[5]) + ' miles after the trip')

        else:
            print('The passenger needs ' + str(requerimiento4[4]) + ' miles to complete the trip')

    elif int(inputs[0]) == 7:

        ciudad = input('Ingrese el aeropuerto que está fuera de funcionamiento (su código IATA): ')
        print('\n')

        start_time = time.process_time()

        requerimiento5 = controller.Requerimiento5(cont, ciudad)

        stop_time = time.process_time()

        elapsed_time_mseg = round((stop_time - start_time)*1000,2)

        print('El tiempo de procesamiento del requerimiento elegido es: ' + str(elapsed_time_mseg) + ' ms' + '\n')

        print('=============== Req No. 5 Inputs ===============')
        print('Closing the airport with IATA code: ' + str(ciudad))
        print('\n')

        print('=============== Req No. 5 Answer ===============')
        print('There are ' + str(requerimiento5[2]) + ' airports affected by the removal of: ' + str(ciudad))
        print('The first & last 3 airports affected are:')
        primeros_3 = controller.getDataIATAList(cont, requerimiento5[0])
        ultimos_3 = controller.getDataIATAList(cont, requerimiento5[1])

        tabla_req5 = pt.PrettyTable(['IATA', 'Name', 'City', 'Country'])
        tabla_req5.max_width = 30

        if lt.size(primeros_3) > 3:
            for airport in lt.iterator(primeros_3):
                tabla_req5.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country']])

        else:
            for airport in lt.iterator(primeros_3):
                tabla_req5.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country']])

            for airport in lt.iterator(ultimos_3):
                tabla_req5.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country']])            

        tabla_req5.hrules = ALL
        print(tabla_req5)

    elif int(inputs[0]) == 8:
        pass

    elif int(inputs[0]) == 9:
        pass

    else:
        sys.exit(0)
sys.exit(0)
