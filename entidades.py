from asyncio.windows_events import NULL
import random
import math
from tkinter import SW
from unicodedata import numeric



class Fila:


    def __init__(self,mediaLlegadas, porcFamiliar, porcSimple, porcPostre, porc1Producto, porc2Producto, porc3Producto,mediaPreparacion, desvPreparacion, valorAUniforme, valorBUniforme, mediaEntrega, desviacionEntrega, tiempoAbandonoCola):
        
        self.mediaLlegadas = mediaLlegadas
        self.porcFamiliar = porcFamiliar
        self.porcSimple = porcSimple
        self.porcPostre = porcPostre
        self.mediaEntrega = mediaEntrega
        self.desviacionEntrega = desviacionEntrega
        self.tiempoAbandonoCola = tiempoAbandonoCola
        self.porc1Producto = porc1Producto
        self.porc2Producto = porc2Producto
        self.porc3Producto = porc3Producto
        self.mediaPreparacion = mediaPreparacion
        self.desvPreparacion = desvPreparacion
        self.valorAUniforme = valorAUniforme
        self.valorBUniforme = valorBUniforme

        self.reloj = 0.0
        self.nroFila = 0
        self.nroAuto = 0
        self.evento = "Inicializacion"
        self.rndLlegada = random.random()
        self.tiempoLlegada = -self.mediaLlegadas  * math.log(1-self.rndLlegada) 
        self.proxLlegada = self.tiempoLlegada + self.reloj
        self.horaAbandono = 0
        self.rndPreparacion1 = 0
        self.rndPreparacion2 = 0
        self.tipoDePedido = ""
        self.cantidadPedido = 0
        self.demoraPreparacion = 0
        self.finPreparacion = 0
        self.rndEntrega1 = 0
        self.rndEntrega2 = 0
        self.demoraEntrega = 0
        self.finEntrega = 0
        self.estadoServidor = "Libre"
        self.acuFamiliar = 0
        self.acuSimple = 0
        self.acuPostres = 0
        self.cola = []
        self.acuAuto = 0
        self.autoEnServidor = []
        self.vecLlegadas = [self.proxLlegada]
        self.vecAbandonos = []
        self.nroAutoAnt = 0

        


    def proximaFila(self):
        
        self.calcularProxEvento()
        self.nroFila += 1
        self.rndLlegada = random.random()
        self.tiempoLlegada = -(self.mediaLlegadas) * math.log(1-self.rndLlegada)
        self.proxLlegada = self.tiempoLlegada + self.reloj
        
        if self.evento == "Nueva llegada":
            if len(self.autoEnServidor) == 0 and len(self.cola) == 0:
                self.acuAuto += 1
                cliente = Auto("En Preparacion", self.acuAuto, self.reloj, None)
                self.nroAuto = self.acuAuto
                self.autoEnServidor = [cliente]
                self.vecLlegadas.pop(0)
                self.vecLlegadas.append(self.proxLlegada)
                self.vecLlegadas.sort()
                self.rndPreparacion1= random.random()
                self.rndPreparacion2= random.random()
                self.tipoDePedido = self.getTipPedido()
                self.cantidadPedido = self.getCantidad()
                self.demoraPreparacion = self.demoraPreparacionPedido()
                self.finPreparacion = self.demoraPreparacion + self.reloj
                self.getTipoPedido()
                self.getEstadoServidor()
                
            else:
                self.acuAuto += 1
                self.horaAbandono = self.reloj + self.tiempoAbandonoCola
                cliente = Auto("Cola", self.acuAuto, self.reloj, self.horaAbandono)
                self.nroAuto = self.acuAuto
                self.cola.append(cliente)
                self.cola.sort(key=lambda x: x.nroAuto)
                self.vecAbandonos.append(self.horaAbandono)
                self.vecAbandonos.sort()
                self.vecLlegadas.append(self.proxLlegada)
                self.vecLlegadas.sort()
                self.vecLlegadas.pop(0)
                self.getEstadoServidor()
            

                
            
        
        elif self.evento == "Nuevo abandono":
            self.nroAuto = self.cola[0].getNroAuto()
            self.cola.pop(0)
            self.vecAbandonos.pop(0)
            self.vecLlegadas.append(self.proxLlegada)
            self.vecLlegadas.sort()
            self.getEstadoServidor()

        elif self.evento == "Fin preparacion pedido":
            self.nroAuto = self.autoEnServidor[0].getNroAuto()
            self.rndEntrega1 = random.random()
            self.rndEntrega2 = random.random()
            self.demoraEntrega = (math.sqrt(-2 * math.log(self.rndEntrega1)) * math.cos(2*math.pi * math.radians(self.rndEntrega2))) * self.desviacionEntrega + self.mediaEntrega
            self.finEntrega = self.reloj + self.demoraEntrega
            self.autoEnServidor[0].estado = "Esperando entrega"
            self.vecLlegadas.append(self.proxLlegada)
            self.vecLlegadas.sort()
            self.nroAutoAnt = self.nroAuto
            self.getEstadoServidor()

        elif self.evento == "Fin entrega pedido":
            self.nroAuto = self.nroAutoAnt
            if len(self.cola) > 0:
                self.autoEnServidor = [self.cola[0]]
                self.cola.pop(0)
                self.vecAbandonos.pop(0)
                self.rndPreparacion1= random.random()
                self.rndPreparacion2= random.random()
                self.tipoDePedido = self.getTipPedido()
                self.cantidadPedido = self.getCantidad()
                self.demoraPreparacion = self.demoraPreparacionPedido()
                self.finPreparacion = self.demoraPreparacion + self.reloj
                self.vecLlegadas.append(self.proxLlegada)
                self.vecLlegadas.sort()
                self.getTipoPedido()
                self.getEstadoServidor()
        
            else:
                self.autoEnServidor = []  
                self.estadoServidor = "Libre"      
                self.vecLlegadas.append(self.proxLlegada)
                self.vecLlegadas.sort()

        return self


    def getTipoPedido(self):
        if self.tipoDePedido == "Familiar":
            self.acuFamiliar += self.cantidadPedido

        elif self.tipoDePedido == "Simple":
            self.acuSimple += self.cantidadPedido
        else:
            self.acuPostres += self.cantidadPedido
    

    def calcularProxEvento(self):
        if len(self.vecLlegadas) == 0:

            if len(self.vecAbandonos) > 0:
                self.reloj = min(self.vecAbandonos[0], max(self.finEntrega,self.finPreparacion))

                if self.reloj == self.finEntrega:
                    self.evento = "Fin entrega pedido"

                elif self.reloj == self.finPreparacion:
                    self.evento = "Fin preparacion pedido"

                else:
                    self.evento = "Nuevo abandono"

            else:
                self.reloj = min(max(self.finEntrega,self.finPreparacion))
                
                if self.reloj == self.finEntrega:
                    self.evento = "Fin entrega pedido"

                elif self.reloj == self.finPreparacion:
                    self.evento = "Fin preparacion pedido"
                
        
        elif len(self.cola) > 3:

            if len(self.vecAbandonos) > 0:
                self.reloj = min(self.vecAbandonos[0], max(self.finEntrega,self.finPreparacion),self.vecLlegadas[0])

                if self.reloj == self.finEntrega:
                    self.evento = "Fin entrega pedido"

                elif self.reloj == self.finPreparacion:
                    self.evento = "Fin preparacion pedido"

                elif self.reloj == self.vecLlegadas[0]:
                    self.vecLlegadas.pop(0)
                    self.calcularProxEvento()

                else:
                    self.evento = "Nuevo abandono"
            
            else:
                self.reloj = min(max(self.finEntrega,self.finPreparacion),self.vecLlegadas[0])

                if self.reloj == self.finEntrega:
                    self.evento = "Fin entrega pedido"

                elif self.reloj == self.finPreparacion:
                    self.evento = "Fin preparacion pedido"

                else:
                    self.vecLlegadas.pop(0)
                    self.calcularProxEvento()

        elif len(self.cola) < 4:

            if len(self.vecAbandonos) > 0:
                self.reloj = min(self.vecAbandonos[0], max(self.finEntrega,self.finPreparacion),self.vecLlegadas[0])

                if self.reloj == self.finEntrega:
                    self.evento = "Fin entrega pedido"

                elif self.reloj == self.finPreparacion:
                    self.evento = "Fin preparacion pedido"

                elif self.reloj == self.vecLlegadas[0]:
                    self.evento = "Nueva llegada"

                else:
                    self.evento = "Nuevo abandono"
            
            elif self.finPreparacion == 0:
                self.reloj = self.vecLlegadas[0]
                self.evento = self.evento = "Nueva llegada"

            elif (self.finEntrega <= self.reloj and self.finPreparacion <= self.reloj):
                self.reloj = self.vecLlegadas[0]
                self.evento = "Nueva llegada"

            else:
                self.reloj = min(max(self.finEntrega,self.finPreparacion),self.vecLlegadas[0])

                if self.reloj == self.finEntrega:
                    self.evento = "Fin entrega pedido"

                elif self.reloj == self.finPreparacion:
                    self.evento = "Fin preparacion pedido"

                else:
                    self.evento = "Nueva llegada"



    def calcularTiempoLlegada(self):
        return -(self.mediaLlegadas) * math.log(1-self.rndLlegada)

    def demoraPreparacionPedido(self):
        if self.tipoDePedido == "Familiar":
            self.demoraPreparacion = (5-(3/self.cantidadPedido))
        elif self.tipoDePedido == "Simple":
            self.demoraPreparacion = (((math.sqrt(-2*math.log(self.rndPreparacion1)) * math.cos(2 * math.pi * math.radians(self.rndPreparacion2))) * self.desvPreparacion + self.mediaPreparacion) * self.cantidadPedido)
        elif self.tipoDePedido == "Postre":
            self.demoraPreparacion = (self.valorAUniforme+(self.rndPreparacion1 * (self.valorBUniforme-self.valorAUniforme)))
        return self.demoraPreparacion

    def getTipPedido(self):
        if  self.rndPreparacion1 < (self.porcFamiliar/100):
            self.tipoDePedido = "Familiar"

        elif self.rndPreparacion1 < ((self.porcSimple/100) + (self.porcFamiliar/100)):
            self.tipoDePedido = "Simple"
        else:
            self.tipoDePedido = "Postre"

        return self.tipoDePedido


    def getEstadoServidor(self):
        if len(self.autoEnServidor) > 0:
            self.estadoServidor = "Ocupado"
        else:
            self.estadoServidor = "Libre"



    def getCantidad(self):
        if self.rndPreparacion2 < (self.porc1Producto/100):
            self.cantidadPedido = 1
        elif self.rndPreparacion2 < ((self.porc1Producto / 100) + (self.porc2Producto/100)):
            self.cantidadPedido = 2
        else:
            self.cantidadPedido = 3
        return self.cantidadPedido

    def valoresAMostrar(self):
        if (self.evento == "Nueva llegada" and len(self.cola) == 0) or self.evento == "Fin entrega pedido" and len(self.cola) > 0:
            autoEnservidor = self.autoEnServidor[0].getNroAuto()
            horaAbandono = ""
            rndPreparacion1 = round(self.rndPreparacion1,2)
            rndPreparacion2 = round(self.rndPreparacion2,2)
            tipoPedido = self.tipoDePedido
            cantidadPedido = self.cantidadPedido
            demoraPreparacion = round(self.demoraPreparacion,2)
            finPreparacion = round(self.finPreparacion,2)
            rndEntrega1 = ""
            rndEntrega2 = ""
            demoraEntrega = ""
            finEntrega  = ""
        
        elif self.evento == "Nueva llegada" and len(self.autoEnServidor) >  0:
            autoEnservidor = self.autoEnServidor[0].getNroAuto()
            horaAbandono = round(self.horaAbandono,2)
            rndPreparacion1 = ""
            rndPreparacion2 = ""
            tipoPedido = ""
            cantidadPedido = ""
            demoraPreparacion = ""
            finPreparacion = ""
            rndEntrega1 = ""
            rndEntrega2 = ""
            demoraEntrega = ""
            finEntrega  = ""

        elif self.evento == "Nuevo abandono":
            autoEnservidor = self.autoEnServidor[0].getNroAuto()
            horaAbandono = ""
            rndPreparacion1 = ""
            rndPreparacion2 = ""
            tipoPedido = ""
            cantidadPedido = ""
            demoraPreparacion = ""
            finPreparacion = ""
            rndEntrega1 = ""
            rndEntrega2 = ""
            demoraEntrega = ""
            finEntrega  = ""

        elif self.evento == "Fin preparacion pedido":
            autoEnservidor = self.autoEnServidor[0].getNroAuto()
            horaAbandono = ""
            rndPreparacion1 = ""
            rndPreparacion2 = ""
            tipoPedido = ""
            cantidadPedido = ""
            demoraPreparacion = ""
            finPreparacion = ""
            rndEntrega1 = round(self.rndEntrega1,2)
            rndEntrega2 = round(self.rndEntrega2,2)
            demoraEntrega = round(self.demoraEntrega,2)
            finEntrega  = round(self.finEntrega,2)

        elif (self.evento == "Fin entrega pedido" and len(self.cola) == 0 and len(self.autoEnServidor) > 0):
            autoEnservidor = self.autoEnServidor[0].getNroAuto()
            horaAbandono = ""
            rndPreparacion1 = ""
            rndPreparacion2 = ""
            tipoPedido = ""
            cantidadPedido = ""
            demoraPreparacion = ""
            finPreparacion = "" 
            rndEntrega1 = ""
            rndEntrega2 = ""
            demoraEntrega = ""
            finEntrega  = ""

        elif self.evento == "Inicializacion" or (self.evento == "Fin entrega pedido" and len(self.cola) == 0):
            autoEnservidor = ""
            horaAbandono = ""
            rndPreparacion1 = ""
            rndPreparacion2 = ""
            tipoPedido = ""
            cantidadPedido = ""
            demoraPreparacion = ""
            finPreparacion = ""
            rndEntrega1 = ""
            rndEntrega2 = ""
            demoraEntrega = ""
            finEntrega  = ""
        
        if len(self.cola) == 0:
            auto1Cola = "Libre"
            auto2Cola = "Libre"
            auto3Cola = "Libre"
            auto4Cola = "Libre"
        elif len(self.cola) == 1:
            auto1Cola = self.cola[0].getNroAuto()
            auto2Cola = "Libre"
            auto3Cola = "Libre"
            auto4Cola = "Libre"
        elif len(self.cola) == 2:
            auto1Cola = self.cola[0].getNroAuto()
            auto2Cola = self.cola[1].getNroAuto()
            auto3Cola = "Libre"
            auto4Cola = "Libre" 
        elif len(self.cola) == 3:
            auto1Cola = self.cola[0].getNroAuto()
            auto2Cola = self.cola[1].getNroAuto()
            auto3Cola = self.cola[2].getNroAuto()
            auto4Cola = "Libre"
        elif len(self.cola) == 4:
            auto1Cola = self.cola[0].getNroAuto()
            auto2Cola = self.cola[1].getNroAuto()
            auto3Cola = self.cola[2].getNroAuto()
            auto4Cola = self.cola[3].getNroAuto()
        
        return autoEnservidor, horaAbandono, rndPreparacion1, rndPreparacion2, tipoPedido, cantidadPedido, demoraPreparacion, finPreparacion, rndEntrega1, rndEntrega2, demoraEntrega, finEntrega, auto1Cola, auto2Cola, auto3Cola, auto4Cola

    def mostrarFila(self):
        return [self.nroFila, self.nroAuto, self.valoresAMostrar()[0], len(self.vecLlegadas), self.evento, round(self.reloj,2),
                round(self.rndLlegada,2), round(self.tiempoLlegada,2), round(self.proxLlegada,2),
                self.valoresAMostrar()[1], self.valoresAMostrar()[2], self.valoresAMostrar()[3],
                self.valoresAMostrar()[4], self.valoresAMostrar()[5], self.valoresAMostrar()[6],
                self.valoresAMostrar()[7], self.valoresAMostrar()[8], self.valoresAMostrar()[9],
                self.valoresAMostrar()[10], self.valoresAMostrar()[11], self.estadoServidor,
                len(self.cola), self.valoresAMostrar()[12], self.valoresAMostrar()[13], 
                self.valoresAMostrar()[14], self.valoresAMostrar()[15],
                self.acuFamiliar, self.acuSimple, self.acuPostres]
        

class Auto:
    def __init__(self,estado, nroAuto, horaLlegada, horaAbandono):
        self.estado = estado
        self.nroAuto = nroAuto
        self.horaLlegada = horaLlegada
        self.horaAbandono = horaAbandono
    
    def getNroAuto(self):
        return self.nroAuto