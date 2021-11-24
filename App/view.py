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

routesfile = 'routes_full.csv'
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
        controller.loadDataRoutes(cont, routesfile)

        numvertex = controller.totalAirports(cont)
        numedges = controller.totalConnections(cont)

        numvertex2 = controller.totalAirports2(cont)
        numedges2 = controller.totalConnections2(cont)

        print('Número de vertices en el dígrafo: ' + str(numvertex))
        print('Número de arcos en el dígrafo: ' + str(numedges))

        print('Número de vertices en el grafo no dirigido: ' + str(numvertex2))
        print('Número de arcos en el grafo no dirigido: ' + str(numedges2))

        print('El limite de recursion actual es: ' + str(sys.getrecursionlimit()))

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

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
