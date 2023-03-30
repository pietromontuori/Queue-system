import copy
from math import sqrt
import entidades as entity



def empezarSimulacion(mediaLlegadas,porcFamiliar,porcSimple,porcPostre,porc1Producto, porc2Producto, porc3Producto,mediaPreparacion, desvPreparacion, valorAUniforme, valorBUniforme, mediaEntrega,desviacionEntrega,tiempoAbandonoCola):
    global fila
    fila = entity.Fila(mediaLlegadas,porcFamiliar,porcSimple,porcPostre, porc1Producto, porc2Producto, porc3Producto,mediaPreparacion, desvPreparacion, valorAUniforme, valorBUniforme, mediaEntrega,desviacionEntrega,tiempoAbandonoCola)
    salida = mostrarFila(fila.mostrarFila())
    return salida

def mostrarFila(v):
     temp = copy.deepcopy(v)
     return temp
    

def calcularSiguienteFila():
    global fila
    fila = fila.proximaFila()
    temp = mostrarFila(fila.mostrarFila())
   
    return temp

def limpiarDatos():
    global fila
    fila.cola.clear()
    fila.autoEnServidor.clear()
    return fila