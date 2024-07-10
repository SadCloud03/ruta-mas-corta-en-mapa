#calculador de rutas, encontrar la ruta mas corta entre dos caminos del mapa 
#debe tener obstaculos en el mapa y el algoritmo tiene que se capaz de encontrar aun asi la ruta mas corta
#se utiliza una matriz bidimencional 
#cada celda de la matriz tendra un valor que represente el tipo de terreno 

#implementar el algoritmo de buscqueda de ruta 

#vizualizar finalmente el mapa 

#agregar obstaculos 

#el usuario ingresa los puntos a buscar en el mapa 

#bibliotecas a usar:
import pygame 
import numpy as np
import random 
import heapq


#costantes a utilizar:
#que es lo que va a usar el mapa?
#dimensiones del mapa:
fila_mapa = 8
columna_mapa = 8
#generacion de mapa:
mapa = np.zeros((columna_mapa,fila_mapa), dtype=int)

#apartado de funciones:




#funcion generador de obstaculos 
def gen_ostaculos():
    while True:
        can_obstaculos = int(input("escriba en numeros cuantos obstaculos desea (el limite es 20): "))
        if 0 < can_obstaculos <= 20:
            obstaculos = [((random.randint(0, columna_mapa - 1 )), (random.randint(0, fila_mapa - 1))) for _ in range(can_obstaculos)]
            for x, y in obstaculos:
                mapa[y, x] = 1
            return mapa 
        else:
            print("la cantidad supera el limite.")



#funcion para generar imprevistos:
def imprevistos():
        while True:
            preg_inprevisto = int(input("en que numero de casilla se encuentra el inprevisto: "))
            preg_inprevisto -= 1

            columna = preg_inprevisto % columna_mapa
            fila = preg_inprevisto // fila_mapa

            if 0 <= columna < columna_mapa and 0 <= fila < fila_mapa:
                mapa[columna, fila] = 2
                break   
            else:
                print("la casilla esta fuera del rango de la matriz")

        print("\n\nmapa actializado:\n", mapa)


#funcion para que el usuario decida de donde a donde ir en el mapa 
def ubicaciones():
    for tipo in ['entrada', 'salida']:
        tamano_mapa = fila_mapa * columna_mapa
        print("el numero de casillas en el mapa es: ", tamano_mapa)

        if tipo == 'entrada':
            entrada = int(input("elija la casilla donde se encuentra (las casillas van de arriba a abajo): "))
            entrada -= 1

            columna = entrada % columna_mapa
            fila = entrada // fila_mapa

            mapa[columna, fila] = 5
            print("\nse asigno el punto de partida.\n", mapa)


        elif tipo == 'salida':
            salida = int(input("hasta que casilla quiere ir (las casillas van de arriba a abajo): "))
            salida -= 1

            columna = salida % columna_mapa
            fila = salida // fila_mapa

            mapa[columna, fila] = 6
            print("se asigno la llegada.\n", mapa)
    
    return mapa

def heuristica(entrada, salida):
    return abs(entrada[0] - salida[0]) + abs(entrada[1] - salida[1])

def A_star(mapa, entrada, salida):

    #dimensiones del mapa:
    filas, columnas = mapa.shape[0], mapa.shape[1]

    #direcciones posibles 
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    #cola de prioridad 
    heap = []
    heapq.heappush(heap, (0, entrada[0], entrada[1]))

    #los diccionarios a usar 
    costo_al_mom = {entrada: 0}
    viene_de = {entrada: None}

    while heap:
        current_cost, x, y = heapq.heappop(heap)

        #alcanzar el fin:
        if (x, y) == salida:
            camino = []
            nodo = salida 
            while nodo is not None:
                camino.append(nodo)
                nodo = viene_de[nodo]
            camino.reverse()
            return camino 
        
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy 
            new_cost = current_cost + 1
            
             # Verificar límites del mapa, obstáculos e imprevistos
            if 0 <= nx < filas and 0 <= ny < columnas and mapa[nx, ny] != 1:  # No es obstáculo
                if mapa[nx, ny] != 2:  # No es imprevisto
                    if (nx, ny) not in costo_al_mom or new_cost < costo_al_mom[(nx, ny)]:
                        costo_al_mom[(nx, ny)] = new_cost
                        priority = new_cost + heuristica((nx, ny), salida)
                        heapq.heappush(heap, (priority, nx, ny))
                        viene_de[(nx, ny)] = (x, y)

    return None 


def caminos_cortos():


    # presentar el mapa:
    print(f"\nEste es el mapa inicial:\n{mapa}")
    #generacion de obstaculos
    preg_obstaculos = str(input("desea generar obstaculos?(si/no): ")).lower()
    if preg_obstaculos == "si":
        gen_ostaculos()
        print("\n\nel mapa se actualizo:\n", mapa)
    else:
        print("\n\nel mapa no se actualizo:\n", mapa)


    #ubicaciones del usuario:
    preg_ubicaciones = str(input("le gustaria ir de un punto a otro?(si/no): ")).lower()
    if preg_ubicaciones == "si":
        ubicaciones()
        print("\n\neste es el mapa con los puntos asignados:\n", mapa)
    else:
        print("\n\nel mapa no tiene ubicacion ni llegada del usuario.")




    #decir que hay obstaculos:
    hay_imprevistos = str(input("hay inprevistos en el camino?(si/no): ")).lower()
    while hay_imprevistos == "si":
        imprevistos()
        hay_imprevistos = str(input("\nhay mas imprevistos en el camino?(si/no): ")).lower()



    #calcular ruta mas corta 
    if 5 in mapa and 6 in mapa:
        entrada = tuple(np.argwhere(mapa == 5)[0])
        salida = tuple(np.argwhere(mapa == 6)[0])
        ruta = A_star(mapa, entrada, salida)
        

    for ubicacion in ruta:
        try:
            mapa[ubicacion] = 7
        except:
            print("no se puede hacer la ruta")

    #la ruta mas rapida a la ubicacion final es:
    print("la ruta mas rapida a la ubicacion final es\n", mapa)
    

caminos_cortos()



        

    

