"""import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import font

# CTRL + ALT + L --> FORMAT

root = Tk()
root.title('Titulo')
root.iconbitmap("imgs/library.ico")
root.geometry("1200x660")

my_frame = Frame(root)
my_frame.pack(pady=5)

text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), background="yellow", selectforeground="black",
               undo=True, yscrollcommand=text_scroll.set)
my_text.pack()

text_scroll.config(command=my_text.yview)
my_menu = Menu(root)
mensaje = "hola"
ruta = ""


def abrirArchivo():
    aux = tkinter.Tk()
    aux.withdraw()  # hide window
    archivo = tkinter.filedialog.askopenfilename(parent=aux)
    archivo = open(archivo, 'r')
    instrucciones = archivo.read()
    my_text.insert('insert', instrucciones)
    # print(my_text.get("1.0", "end-1c")) imprime el contenido de la caja de texto


def guardar_como():
    global ruta
    fichero = tkinter.filedialog.asksaveasfile(title="Guardar como", defaultextension=".ch", mode='w')
    ruta = fichero.name
    if fichero is not None:
        contenido = my_text.get(1.0, 'end-1c')  # recuperamos el texto
        fichero = open(ruta, 'w+')  # creamos el fichero o abrimos
        fichero.write(contenido)  # escribimos el texto
        fichero.close()

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open", command=abrirArchivo)
file_menu.add_command(label="Save", command=guardar_como)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="file", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

stringvar = StringVar(value=mensaje)
status_bar = Label(root, text=stringvar.get())
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

root.config(menu=my_menu)
root.mainloop()"""

class proceso(object):

    def __init__(self, id, rafaga, llegada):
        self.id = id
        self.rafaga = rafaga
        self.llegada = llegada
        self.rafagatmp = rafaga
        self.espera = 0
        self.retorno = 0
        self.finalizacion = 0


print("***********************************************")
print("************** Simulacion ROUND ROBIN *********")
print("***********************************************")
print("***********************************************")
print("*+-------------------------------------------+*")
print("*|      By FuriosoJack                       |*")
print("*+-------------------------------------------+*")
print("***********************************************")
print()
print()
try:
    # if(True):
    print("Ingrese el numero de procesos")
    nnumeros = int(input(">"))
    if (nnumeros > 0):
        listadeprocesos = []
        for i in range(nnumeros):
            tmpllegada = -1
            print("################### Proceso " + str(i + 1) + " ###############")
            while (tmpllegada < 0):
                print("Ingrese el tiempo de llegada del proceso")
                tmpllegada = int(input(">"))

            rafagatmp = 0
            while (rafagatmp < 1):
                print("Ingrese la rafaga del proceso>")
                rafagatmp = int(input(">"))
            # en el arreglo el primer item es el "id del proceso", luego la rafaga y ultimo la llegada
            listadeprocesos.append(proceso((i + 1), rafagatmp, tmpllegada))
            print("################### Fin del procesos ###############")
            print()
            print()
            print()
            print()
        print("Procesoss creados Con exito!!")
        print()
        quantum = 0
        swi = False
        while (quantum < 1):
            print("Ingrese el Quantum")
            quantum = int(input(">"))
        quantumtmp = quantum


        # metodo para ordenar los procesos por tiempo de llegada
        def ordenaInsersion(lista):
            for i in range(1, len(lista)):
                j = i
                while j > 0 and lista[j].llegada < lista[j - 1].llegada:
                    lista[j], lista[j - 1] = lista[j - 1], lista[j]
                    j = j - 1
            return lista


        listadeprocesos = ordenaInsersion(listadeprocesos)  # lista queda ordenada por tiempo de llegada
        print("[+] Se ordeno lista de procesos por tiempo de llegada")
        procesosEspejo = len(listadeprocesos)  # es la variable que controla los procesos que hacen falta por terminar
        tiempo = 0
        procesosCola = []
        procesoEjecusion = None  # variable que corresponde al proceso que actualmente se encuentra en ejecusion
        nproceso = 0  # variable utilizada para pasar al siguiente
        print("[+] Se establecieron varibles para el funcionamiento")
        print("@@@@@@@ Incicio del Algortimo  @@@@@@@@")
        sw = True  # Variable de control
        while (procesosEspejo > 0): # Mientras haya procesos para ejecutarse
            print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
            if (len(listadeprocesos) > nproceso and tiempo >= listadeprocesos[nproceso].llegada):
                print("[+]El proceso " + str(listadeprocesos[nproceso].id) + " se ingreso a la cola de listos")
                procesosCola.append(listadeprocesos[nproceso])
                nproceso = nproceso + 1

            else:
                if nproceso > 0 or len(procesosCola) > 0:
                    if (procesoEjecusion == None):
                        procesoEjecusion = procesosCola.pop(0)
                        sw = True
                        print("[+] Se saca el proceso " + str(procesoEjecusion.id) + " de la cola y se ejecuta.")
                    else:
                        if (sw):
                            if (procesoEjecusion.rafagatmp >= quantum):
                                procesoEjecusion.rafagatmp = procesoEjecusion.rafagatmp - quantum
                                print("[+] Se resta " + str(quantum) + " a la rafaga del proceso " + str(
                                    procesoEjecusion.id))
                                tiempo = tiempo + quantum
                                print("[+] Se aumenta" + str(quantum) + " al tiempo")
                            else:
                                tiempo = tiempo + procesoEjecusion.rafagatmp
                                print("[+] Se aumenta " + str(procesoEjecusion.rafagatmp) + " al tiempo")
                                print("[+] Se resta " + str(
                                    procesoEjecusion.rafagatmp) + " a la rafaga del proceso " + str(
                                    procesoEjecusion.id))
                                procesoEjecusion.rafagatmp = 0

                            if (procesoEjecusion.rafagatmp < 1):
                                print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
                                print("[+] El Proceso " + str(procesoEjecusion.id) + " finalizo.")
                                procesoEjecusion.finalizacion = tiempo
                                procesoEjecusion.retorno = procesoEjecusion.finalizacion - procesoEjecusion.llegada
                                procesoEjecusion.espera = procesoEjecusion.retorno - procesoEjecusion.rafaga
                                procesosEspejo = procesosEspejo - 1
                                procesoEjecusion = None

                            else:
                                sw = False
                        else:
                            procesosCola.append(procesoEjecusion)
                            print("[+] Se agrega el proceso " + str(
                                procesoEjecusion.id) + " que estaba en ejecusion a la cola de listos")
                            procesoEjecusion = None
                else:
                    tiempo = tiempo + 1
        print("@@@@@@@ Algoritmo Finalizado @@@@@@@@")
        print("")
        print()
        print()
        print("!!!!!!!!!!!!!! Resultados !!!!!")
        totalretorno = 0
        totalespera = 0
        for proceso in listadeprocesos:
            print("Proceso " + str(proceso.id) + " Finalizo: " + str(proceso.finalizacion) + " Espera: " + str(
                proceso.espera) + " Retorno: " + str(proceso.retorno))
            totalretorno = totalretorno + proceso.retorno
            totalespera = totalespera + proceso.espera
        print()
        print("Promedio de retorno: " + str(totalretorno / len(listadeprocesos)))
        print("Promedio de espera: " + str(totalespera / len(listadeprocesos)))
    else:
        print("No es valido")
except Exception as e:
    print(e)

