import gestor
import tkinter as tk
from tkinter import ttk
import entidades



def btnSimularClick():
    cleanTable(treeResolucion)
    minutos = int(cajaMinutosSimular.get())
    desde = int(cajaParamMostarDesde.get())
    hasta = int(cajaCantMostrar.get())+desde
    mediaLlegadas = int(cajaMediaLlegadas.get())
    porcFamiliar = int(cajaPorcFamiliar.get())
    porcSimple = int(cajaPorcSimple.get())
    porcPostre = int(cajaPorcPostre.get())
    mediaEntrega = float(cajaMediaEntrega.get())
    desviacionEntrega = float(cajaDesviacionEntrega.get())
    tiempoAbandonoCola = int(cajaTiempoAbandono.get())
    porc1Producto = int(caja1Cantidad.get())
    porc2Producto = int(caja2Cantidades.get())
    porc3Producto = int(caja3Cantidades.get())
    mediaPreparacion = int(cajaPrepSimpleMedia.get())
    desvPreparacion = int(cajaPrepSimpleDesv.get())
    valorAUniforme = int(cajaPrepPostreA.get())
    valorBUniforme = int(cajaPrepPostreB.get())

    insertarFila(treeResolucion, gestor.empezarSimulacion(mediaLlegadas,porcFamiliar,porcSimple,porcPostre,porc1Producto, porc2Producto, porc3Producto,mediaPreparacion, desvPreparacion, valorAUniforme, valorBUniforme,mediaEntrega,desviacionEntrega,tiempoAbandonoCola), 0)

    i = round(gestor.fila.reloj,0)

    while i < minutos:
        filaSimulada = gestor.calcularSiguienteFila()
        if i >= desde and i < hasta:
            insertarFila(treeResolucion, filaSimulada, i)
        i = round(gestor.fila.reloj,0)
    insertarFila(treeResolucion, gestor.calcularSiguienteFila(), minutos)

    acuFamiliar = gestor.fila.acuFamiliar
    acuSimple = gestor.fila.acuSimple
    acuPostre = gestor.fila.acuPostres

    resultado(acuFamiliar,acuSimple,acuPostre)
    
    del gestor.fila

    #gestor.limpiarDatos()
    
   



def habilitarBoton():
    botonSimular["state"] = "normal"


def cleanTable(tabla):
    tabla.delete(*tabla.get_children())


def insertarFila(treeview, fila, n):

    if gestor.fila.nroFila % 2 == 0:
        treeview.insert(parent='', index='end', text=str(n), values=fila, tags = ("even"))
    else:
        treeview.insert(parent='', index='end', text=str(n), values=fila, tags = ("odd"))


# Interfaz
miWindow = tk.Tk()  # Creacion de la ventana contenedora
miWindow.title("Ejercicio 284 - Montuori 79064")
miWindow.geometry("1500x780")
miWindow.resizable(False, False)
# Pestaña
nb = ttk.Notebook(miWindow)
nb.pack(fill='both', expand='yes')

# Creamos Pestañas
p1 = ttk.Frame(nb)


# Interacciones y objetos
# Parametros adicionales:
cajaMinutosSimular = tk.Entry(p1, width=6)
cajaMinutosSimular.insert(0, 480)
lblMinutosSimular = tk.Label(p1, text="Minutos a simular")
cajaMinutosSimular.place(x=130, y=10)
lblMinutosSimular.place(x=5, y=10)


cajaMediaLlegadas = tk.Entry(p1, width=6)
cajaMediaLlegadas.insert(0, 2)
lblMediaLlegadas = tk.Label(p1, text="Media de llegadas")
cajaMediaLlegadas.place(x=130, y=40)
lblMediaLlegadas.place(x=5, y=40)


cajaPorcFamiliar = tk.Entry(p1, width=6)
cajaPorcFamiliar.insert(0, 20)
lblPorcFamiliar = tk.Label(p1, text="% Familiar")
cajaPorcFamiliar.place(x=275, y=10)
lblPorcFamiliar.place(x=200, y=10)


cajaPorcSimple = tk.Entry(p1, width=6)
cajaPorcSimple.insert(0, 50)
lblPorcSimple = tk.Label(p1, text="% Simple")
cajaPorcSimple.place(x=275, y=40)
lblPorcSimple.place(x=200, y=40)


cajaPorcPostre = tk.Entry(p1, width=6)
cajaPorcPostre.insert(0, 30)
lblPorcPostre = tk.Label(p1, text="% Postre")
cajaPorcPostre.place(x=275, y=70)
lblPorcPostre.place(x=200, y=70)


caja1Cantidad = tk.Entry(p1, width=6)
caja1Cantidad.insert(0, 50)
lbl1Cantidad = tk.Label(p1, text="% 1 Unidad")
caja1Cantidad.place(x=440, y=10)
lbl1Cantidad.place(x=350, y=10)


caja2Cantidades = tk.Entry(p1, width=6)
caja2Cantidades.insert(0, 30)
lbl2Cantidades = tk.Label(p1, text="% 2 Unidades")
caja2Cantidades.place(x=440, y=40)
lbl2Cantidades.place(x=350, y=40)


caja3Cantidades = tk.Entry(p1, width=6)
caja3Cantidades.insert(0, 20)
lbl3Cantidades = tk.Label(p1, text="% 3 Unidades")
caja3Cantidades.place(x=440, y=70)
lbl3Cantidades.place(x=350, y=70)


lblPreparacion = tk.Label(p1, text="Preparación")
lblPreparacion.place(x=510, y=40)


lblPrepSimple = tk.Label(p1, text="Tipo Simple:")
lblPrepSimple.place(x=610, y=10)


cajaPrepSimpleMedia = tk.Entry(p1, width=6)
cajaPrepSimpleMedia.insert(0, 2)
lblPrepSimpleMedia = tk.Label(p1, text="Media")
cajaPrepSimpleMedia.place(x=680, y=40)
lblPrepSimpleMedia.place(x=610, y=40)

cajaPrepSimpleDesv = tk.Entry(p1, width=6)
cajaPrepSimpleDesv.insert(0, 1)
lblPrepSimpleDesv = tk.Label(p1, text="Desviación")
cajaPrepSimpleDesv.place(x=680, y=70)
lblPrepSimpleDesv.place(x=610, y=70)




lblPrepPostre = tk.Label(p1, text="Tipo Postre:")
lblPrepPostre.place(x=750, y=10)


cajaPrepPostreA = tk.Entry(p1, width=6)
cajaPrepPostreA.insert(0, 1)
lblPrepPostreA = tk.Label(p1, text="Valor A")
cajaPrepPostreA.place(x=820, y=40)
lblPrepPostreA.place(x=750, y=40)


cajaPrepPostreB = tk.Entry(p1, width=6)
cajaPrepPostreB.insert(0, 2)
lblPrepPostreB = tk.Label(p1, text="Valor B")
cajaPrepPostreB.place(x=820, y=70)
lblPrepPostreB.place(x=750, y=70)


cajaMediaEntrega = tk.Entry(p1, width=6)
cajaMediaEntrega.insert(0, 0.5)
lblMediaEntrega = tk.Label(p1, text="Media entrega:")
cajaMediaEntrega.place(x=1030, y=10)
lblMediaEntrega.place(x=900, y=10)


cajaDesviacionEntrega = tk.Entry(p1, width=6)
cajaDesviacionEntrega.insert(0, 0.25)
lblDesviacionEntrega = tk.Label(p1, text="Desviacion entrega:")
cajaDesviacionEntrega.place(x=1030, y=40)
lblDesviacionEntrega.place(x=900, y=40)


cajaTiempoAbandono = tk.Entry(p1, width=6)
cajaTiempoAbandono.insert(0, 8)
lblTiempoAbandono = tk.Label(p1, text="Tiempo abandono:")
cajaTiempoAbandono.place(x=1030, y=70)
lblTiempoAbandono.place(x=900, y=70)


cajaParamMostarDesde = tk.Entry(p1, width=6)
cajaParamMostarDesde.insert(0, 0)
lblParamMostarDesde = tk.Label(p1, text="Mostrar desde:")
cajaParamMostarDesde.place(x=1230, y=10)
lblParamMostarDesde.place(x=1100, y=10)

cajaCantMostrar = tk.Entry(p1, width=6)
cajaCantMostrar.insert(0, 480)
lblCantMostrar = tk.Label(p1, text="Cantidad a mostrar:")
cajaCantMostrar.place(x=1230, y=40)
lblCantMostrar.place(x=1100, y=40)

def resultado(familiar,simple,postre):
    lblResultado = tk.Label(p1, text="Resultado: Se vendieron {} de tipo familiar, {} de tipo simple, y {} de tipo postre.".format(familiar,simple,postre), font=("Courier 13 bold"))
    lblResultado.place(x=10, y=710)



botonSimular = tk.Button(p1, text="Simular", padx=10,
                         pady=5, command=btnSimularClick, state="normal")
botonSimular.place(x=1300, y=10)



# Treeview Resolucion del ejercicio

headerColas =  ["Fila", "Auto", "Auto en servidor", "Autos x llegar" ,"       Evento      ", "Reloj",
                    "RND Llegadas", "Tiempo llegada", "Hora llegada",
                    "Hora abandono", "RND 1 PREP.",
                    "RND2 PREP.", "Tipo pedido",
                    "Cantidad", "Demora",
                    "Hora fin prep.", "RND1 entrega", "RND2 entrega", 
                    "Demora", "Hora entrega", "Estado Servidor", 
                    "Cant. Cola", "Auto 1 en cola","Auto 2 en cola","Auto 3 en cola","Auto 4 en cola",
                    "Ac. Familiar", "Ac. Simple", "Ac. Postre"]
treeResolucion = ttk.Treeview(p1, height=29, column=[
                              f"#{cantidad}" for cantidad in range(1, len(headerColas) + 1)], show='headings')
treeResolucion.place(x=8, y=95)


for i in range(len(headerColas)):
    treeResolucion.column("#" + str(i + 1), anchor=tk.CENTER, width=50, minwidth=len(headerColas[i]) * 8 + 5,
                          stretch=True)
    treeResolucion.heading("#" + str(i + 1), text=headerColas[i])
    
vsb = ttk.Scrollbar(p1, orient="vertical", command=treeResolucion.yview)
vsb.pack(side='right', fill='y')
treeResolucion.configure(yscrollcommand=vsb.set)
vsb = ttk.Scrollbar(p1, orient="horizontal", command=treeResolucion.xview)
vsb.pack(side='bottom', fill='x')
treeResolucion.tag_configure("odd",background="#eee")
treeResolucion.tag_configure("even",background="#ddd")
treeResolucion.configure(xscrollcommand=vsb.set)






# Añadimos Pestañas al window
nb.add(p1, text="Ejercicio")


miWindow.mainloop()