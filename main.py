import sys  # control del sistema
import pygame  # interfaz grafica
import tkinter.filedialog  # manejo de archivos
import tkinter  # interfaz grafica
from tkinter import *
import random
from tkinter import filedialog
from tkinter import font

# CTRL + ALT + L --> FORMAT
pygame.init()
ancho, alto = 1100, 700
velocidad = [2, 2]
color_fondo = pygame.color.Color("#040926")
color_menu_izquierdo = pygame.color.Color("#251351")
color_azul = pygame.color.Color("#EEABB3")
fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 18)
color_gris = pygame.color.Color("#7D2E68")
color_amarillo = pygame.color.Color("#f5f3bb")
color_amarillo_claro = pygame.color.Color("#f2f5ea")
color_rojo = pygame.color.Color("#CC2936")
color_texto = pygame.color.Color("#EEABB3")
levels = (range(32, 256, 32))
colores_programas = [color_amarillo]
boton_fcfs_active = False
boton_RR_active = False
boton_SJF_active = False
boton_EXP_active = False
boton_PRI_active = False

color_azul_oscuro = color_menu_izquierdo
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
pantalla = pygame.display.set_mode((ancho, alto))

# Cargue de archivos multimedia
pygame.display.set_caption("CH Maquina 2022")
pc_img = pygame.image.load("imgs/Captura.PNG")
impresora_img = pygame.image.load("imgs/Captura_1.PNG")
play_img = pygame.image.load("imgs/play.png")
play_img = pygame.transform.scale(play_img, (64, 64))
icono = pygame.image.load("imgs/icono.ico")
image = pygame.image.load("imgs/instruments.png").convert()

clock = pygame.time.Clock()  # reloj para controlar la velocidad de ejecucion del programa
pygame.display.set_icon(icono)
padding = 5

contador_paso_a_paso = 0

# Textos a mostrar en la interfaz, se manejan como variables ya que cambian en el transcurso de la ejecucion
texto_modo = "K E R N E L"
texto_codigo = "Aqui va el programa :)"
texto_variables = "Aqui van las variables"
texto_etiquetas = "Aqui van las etiquetas"
texto_pc = "texto ejemplo pc"
texto_impresora = "texto ejemplo impresora"
texto_paso = "PASO A PASO"

# Variables iniciales del ch cumputador
memoria = 100
kernel = 59
quantum = 5
memoria_principal = list(range(memoria + kernel))

# Variables globales
programas = []  # almacenamiento de los programas
acumulador = ['I', 0]
variables = {}
etiquetas = {}
resultado = None
contador = 0

# cada recuadro en la interfaz es una Surface dentro de pygame
lado_derecho_surface = pygame.Surface((216 - padding * 2, alto - 50))

# Variables auxiliares para ejecucion
paso_a_paso = False  # saber si se debe correr el modo paso a paso


# Clase que  muestra la parte scrolleabe
class ScrollBar(object):
    def __init__(self, image_height):
        self.y_axis = 0
        self.image_height = image_height
        self.change_y = 0

        bar_height = int((lado_derecho_surface.get_rect().height - 40) / (
                image_height / (lado_derecho_surface.get_rect().height * 1.0)))
        self.bar_rect = pygame.Rect(lado_derecho_surface.get_rect().width - 20, 20, 20, bar_height)
        self.bar_up = pygame.Rect(lado_derecho_surface.get_rect().width - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(lado_derecho_surface.get_rect().width - 20,
                                    lado_derecho_surface.get_rect().height - 20, 20, 20)

        self.bar_up_image = pygame.image.load("imgs/up.png").convert()
        self.bar_down_image = pygame.image.load("imgs/down.png").convert()

        self.on_bar = False
        self.mouse_diff = 0

    def update(self):
        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.image_height) < lado_derecho_surface.get_rect().height:
            self.y_axis = lado_derecho_surface.get_rect().height - self.image_height

        height_diff = self.image_height - lado_derecho_surface.get_rect().height

        scroll_length = lado_derecho_surface.get_rect().height - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20

        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (lado_derecho_surface.get_rect().height - 20):
                self.bar_rect.bottom = lado_derecho_surface.get_rect().height - 20

            self.y_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
        else:
            self.bar_rect.centery = scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 5
            elif self.bar_down.collidepoint(pos):
                self.change_y = -5

        if event.type == pygame.MOUSEBUTTONUP:
            self.change_y = 0
            self.on_bar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_y = 5
            elif event.key == pygame.K_DOWN:
                self.change_y = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.change_y = 0
            elif event.key == pygame.K_DOWN:
                self.change_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, color_gris, self.bar_rect)

        screen.blit(self.bar_up_image, (lado_derecho_surface.get_rect().width - 20, 0))
        screen.blit(self.bar_down_image,
                    (lado_derecho_surface.get_rect().width - 20, lado_derecho_surface.get_rect().height - 20))


scrollbar = ScrollBar((len(memoria_principal) * 1600) / 79.5)


def poner_boton(pos_x, pos_y, superficie):
    boton = pygame.Rect(pos_x, pos_y, (ancho / 7) + 20, 40)
    clickeable = pygame.draw.rect(superficie, color_azul, boton, 0, 15)
    return clickeable


def poner_textbox(pos_x, pos_y, superficie):
    boton = pygame.Rect(pos_x, pos_y, (ancho / 6), 500)
    clickeable = pygame.draw.rect(superficie, color_menu_izquierdo, boton, 0, 15)
    return clickeable


def metodo_fcfs(prog=None, variables=None, etiquetas=None, acumulador=None):
    resultado = None
    tiempos_llegada = []
    cant_instrucciones_programas = []
    for programa in programas:
        if prog and variables and etiquetas and acumulador:
            cant_instrucciones = 0
            for instruccion in programa:
                if type(instruccion) == str:
                    if not (instruccion.startswith("nueva") or instruccion.startswith(
                            "etiqueta") or instruccion.startswith("retorne")):
                        cant_instrucciones += 1
            if not (len(tiempos_llegada) > 0):
                tiempo_llegada = 0
            else:
                """
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                print("longitud de tiempos_llegad ", len(tiempos_llegada))
                print("Posicion de programa ", programas.index(programa))
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                """
                tiempo_llegada = (tiempos_llegada[programas.index(programa) - 1] + cant_instrucciones) / 4
                """print(" -- ", tiempos_llegada[programas.index(programa) - 1], " + ", cant_instrucciones, " / 4 = ",
                      tiempo_llegada)"""
            tiempos_llegada.append(tiempo_llegada)
            print("tiempos_llegada ", tiempos_llegada)
            cant_instrucciones_programas.append(cant_instrucciones)
            # print(">> instrucciones ", cant_instrucciones, " tiempo de llegada ", tiempo_llegada)
        resultado = ejecutar_programa(prog, variables, etiquetas, acumulador)
    return resultado


def metodo_RR(prog=None, variables=None, etiquetas=None, acumulador=None):
    for programa in programas:
        resultado = ejecutar_programa(prog, variables, etiquetas, acumulador)

    return resultado


def poner_controlador(pos_x, pos_y, superficie):
    boton = pygame.Rect(pos_x, pos_y, 50, 20)
    clickeable = pygame.draw.rect(superficie, color_azul, boton, 0, 10)
    return clickeable


def poner_botones(espaciado, contador):
    x = 50
    distancia = 50
    resultado = None

    aux = poner_boton(x, espaciado, pantalla)
    fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 22)
    texto = pygame.font.Font.render(fuente, texto_modo, False, color_amarillo)
    texto = pygame.transform.rotate(texto, 90)
    pantalla.blit(texto, [lado_izquierdo.left + 5, espaciado + aux.height / 4])

    fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 18)
    pantalla.blit((pygame.font.Font.render(fuente, "CARGAR .CH", False, color_fondo)),
                  [x + aux.width / 4, espaciado + aux.height / 4])
    espaciado += distancia
    btn_cargar = aux

    aux = poner_boton(x, espaciado, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "MEMORIA   : " + str(memoria), False, color_fondo)),
                  [x + aux.width / 8, espaciado + aux.height / 4])
    espaciado += distancia

    mas_kernel = poner_controlador(x + 185, espaciado, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "+", False, color_fondo)),
                  [x + 182 + mas_kernel.width / 2, espaciado])

    menos_kernel = poner_controlador(x + 185, espaciado + 25, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "-", False, color_fondo)),
                  [x + 182 + menos_kernel.width / 2, espaciado + 25])

    mas_memoria = poner_controlador(x + 185, espaciado - 50, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "+", False, color_fondo)),
                  [x + 182 + mas_memoria.width / 2, espaciado - 50])

    menos_memoria = poner_controlador(x + 185, espaciado - 25, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "-", False, color_fondo)),
                  [x + 182 + menos_memoria.width / 2, espaciado - 25])

    fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 15)
    boton_paso = poner_boton(x + 185, espaciado - 100, pantalla)
    if type(texto_paso) != str:
        if type(texto_paso) is list:
            pantalla.blit((pygame.font.Font.render(fuente, str(texto_paso[1]), False, color_fondo)),
                          [x + 170 + menos_memoria.width / 2, espaciado - 95])
        else:
            pantalla.blit((pygame.font.Font.render(fuente, "espacio libre en memoria", False, color_fondo)),
                          [x + 170 + menos_memoria.width / 2, espaciado - 95])
    else:
        pantalla.blit((pygame.font.Font.render(fuente, texto_paso, False, color_fondo)),
                      [x + 170 + menos_memoria.width / 2, espaciado - 95])

    fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 18)
    aux = poner_boton(x, espaciado, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "KERNEL       : " + str(kernel), False, color_fondo)),
                  [x + aux.width / 8, espaciado + aux.height / 4])

    espaciado += distancia
    aux = poner_textbox(x - x / 2, espaciado * 1.05, pantalla)

    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 12)
    if type(texto_codigo) == str:
        pantalla.blit((pygame.font.Font.render(fuente_aux, texto_codigo, False, color_texto)),
                      [aux.left + 5, aux.top + 5])
    else:
        mostrar_texto(texto_codigo, aux.left, aux.top)

    boton = pygame.Rect(x - x / 4, lado_derecho_surface.get_rect().bottom - 20, (ancho / 6.8), 40)
    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 17)
    editor = pygame.draw.rect(pantalla, color_rojo, boton, 0, 15)
    pantalla.blit((pygame.font.Font.render(fuente_aux, str("Editor"), False, color_texto)),
                  [editor.centerx - 15, editor.top + 5])
    espaciado_aux = 10
    boton1 = pygame.Rect(editor.right + 35, lado_derecho_surface.get_rect().bottom - 20, 60, 40)
    boton2 = pygame.Rect(boton1.right + espaciado_aux, lado_derecho_surface.get_rect().bottom - 20, 60, 40)
    boton3 = pygame.Rect(boton2.right + espaciado_aux, lado_derecho_surface.get_rect().bottom - 20, 60, 40)
    boton4 = pygame.Rect(boton3.right + espaciado_aux, lado_derecho_surface.get_rect().bottom - 20, 140, 40)
    boton5 = pygame.Rect(boton4.right + espaciado_aux, lado_derecho_surface.get_rect().bottom - 20, 80, 40)
    boton6 = pygame.Rect(boton5.right + espaciado_aux, lado_derecho_surface.get_rect().bottom - 20, 120, 40)

    if boton_fcfs_active:
        color_boton_fcfs = color_rojo
    else:
        color_boton_fcfs = color_gris
    if boton_RR_active:
        color_boton_rr = color_rojo
    else:
        color_boton_rr = color_gris
    if boton_SJF_active:
        color_boton_SJF = color_rojo
    else:
        color_boton_SJF = color_gris
    if boton_EXP_active:
        color_boton_EXP = color_rojo
    else:
        color_boton_EXP = color_gris
    if boton_PRI_active:
        color_boton_PRI = color_rojo
    else:
        color_boton_PRI = color_gris

    boton_fcfs = pygame.draw.rect(pantalla, color_boton_fcfs, boton1, 0, 15)
    boton_RR = pygame.draw.rect(pantalla, color_boton_rr, boton2, 0, 15)
    boton_SJF = pygame.draw.rect(pantalla, color_boton_SJF, boton3, 0, 15)
    boton_EXP = pygame.draw.rect(pantalla, color_boton_EXP, boton4, 0, 15)
    boton_PRI = pygame.draw.rect(pantalla, color_boton_PRI, boton5, 0, 15)
    boton_Quantum = pygame.draw.rect(pantalla, color_rojo, boton6, 0, 15)
    mas_Q = poner_controlador(boton_Quantum.right + espaciado_aux, lado_derecho_surface.get_rect().bottom - 25,
                              pantalla)
    menos_Q = poner_controlador(boton_Quantum.right + espaciado_aux, lado_derecho_surface.get_rect().bottom,
                                pantalla)

    pantalla.blit((pygame.font.Font.render(fuente_aux, str("FCFS"), False, color_texto)),
                  [boton_fcfs.centerx - 15, boton_fcfs.top + 5])
    pantalla.blit((pygame.font.Font.render(fuente_aux, str("RR"), False, color_texto)),
                  [boton_RR.centerx - 15, boton_RR.top + 5])
    pantalla.blit((pygame.font.Font.render(fuente_aux, str("SJF"), False, color_texto)),
                  [boton_SJF.centerx - 15, boton_SJF.top + 5])
    pantalla.blit((pygame.font.Font.render(fuente_aux, str(" SJF Expropiativo"), False, color_amarillo)),
                  [boton_EXP.centerx - 65, boton_EXP.top + 5])
    pantalla.blit((pygame.font.Font.render(fuente_aux, str("Prioridad"), False, color_amarillo)),
                  [boton_PRI.centerx - 35, boton_PRI.top + 5])
    pantalla.blit((pygame.font.Font.render(fuente_aux, ("Quantum : " + str(quantum)), False, color_amarillo)),
                  [boton_Quantum.centerx - 50, boton_Quantum.top + 5])
    pantalla.blit((pygame.font.Font.render(fuente_aux, " + ", False, color_fondo)),
                  [mas_Q.centerx - 8, mas_Q.centery - 10])
    pantalla.blit((pygame.font.Font.render(fuente_aux, " - ", False, color_fondo)),
                  [menos_Q.centerx - 8, menos_Q.centery - 10])

    if pygame.mouse.get_pressed()[0] and editor.collidepoint(pygame.mouse.get_pos()):
        editor_metodo()

    variables_textbox = pygame.Rect(aux.right + 25, espaciado * 1.05, (ancho / 6), 166)
    pygame.draw.rect(pantalla, color_amarillo, variables_textbox, 0, 15)

    etiquetas_textbox = pygame.Rect(aux.right + 25, espaciado * 2.20, (ancho / 6), 166)
    pygame.draw.rect(pantalla, color_amarillo, etiquetas_textbox, 0, 15)

    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 18)
    pantalla.blit((pygame.font.Font.render(fuente_aux, "VARIABLES", False, color_fondo)),
                  [variables_textbox.left + 5, variables_textbox.top + 5])

    pantalla.blit((pygame.font.Font.render(fuente_aux, "ETIQUETAS", False, color_fondo)),
                  [etiquetas_textbox.left + 5, etiquetas_textbox.top + 5])

    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 12)
    if type(texto_variables) == str:
        pantalla.blit((pygame.font.Font.render(fuente_aux, texto_variables, False, color_fondo)),
                      [variables_textbox.left + variables_textbox.width / 5, variables_textbox.centery])
    else:
        mostrar_texto(texto_variables, variables_textbox.left + 5, variables_textbox.top + 23, True)

    pantalla.blit((pygame.font.Font.render(fuente, "ACUMULADOR   : " + str(acumulador[1]), False, color_amarillo)),
                  [variables_textbox.left + 5, variables_textbox.bottom + 5])

    if type(texto_etiquetas) == str:
        pantalla.blit((pygame.font.Font.render(fuente_aux, texto_etiquetas, False, color_fondo)),
                      [etiquetas_textbox.left + etiquetas_textbox.width / 5, etiquetas_textbox.centery])
    else:
        mostrar_texto(texto_etiquetas, etiquetas_textbox.left + 5, etiquetas_textbox.top + 23, True)
    if paso_a_paso:
        cuadro_respuesta = pygame.draw.rect(pantalla, color_rojo, pygame.Rect(pantalla.get_rect().centerx / 1.5,
                                                                              pantalla.get_rect().bottom - 100,
                                                                              lado_derecho_surface.get_rect().width * 1.65,
                                                                              55), 0, 15)
        pantalla.blit((pygame.font.Font.render(fuente, "Paso siguiente", False, color_amarillo)),
                      [cuadro_respuesta.left + 25, cuadro_respuesta.top + 15])

        si = pygame.draw.rect(pantalla, color_amarillo,
                              pygame.Rect(cuadro_respuesta.centerx + 10, cuadro_respuesta.top + 5, 80, 40),
                              0, 8)
        pantalla.blit((pygame.font.Font.render(fuente, ">>", False, color_rojo)),
                      [si.centerx - 5, si.centery - 10])
        if pygame.mouse.get_pressed()[0] and si.collidepoint(pygame.mouse.get_pos()):
            return [btn_cargar, mas_memoria, menos_memoria, mas_kernel, menos_kernel, boton_paso, contador, resultado,
                    boton_fcfs, boton_RR, boton_SJF, boton_EXP, boton_PRI, mas_Q, menos_Q]

    return [btn_cargar, mas_memoria, menos_memoria, mas_kernel, menos_kernel, boton_paso, contador, resultado,
            boton_fcfs, boton_RR, boton_SJF, boton_EXP, boton_PRI, mas_Q, menos_Q]


#   filedialog
def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def editor_metodo():
    root = Tk()
    root.title('Editor')
    root.iconbitmap("imgs/icono.ico")
    root.geometry("1200x660")

    my_frame = Frame(root)
    my_frame.pack(pady=5)

    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side=RIGHT, fill=Y)

    my_text = Text(my_frame, width=97, height=25, font=("fonts/Roboto-Regular.ttf", 18), background="#040926",
                   selectforeground="#040926", fg="#f2f5ea", pady=5, padx=5,
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
    file_menu.add_command(label="Exit", command=root.destroy)

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
    root.mainloop()


def validar_sintaxis(linea):
    linea = linea.strip()
    linea = linea.replace("       ", " ")
    linea = linea.replace("      ", " ")
    linea = linea.replace("     ", " ")
    linea = linea.replace("    ", " ")
    linea = linea.replace("   ", " ")
    linea = linea.replace("  ", " ")
    linea = linea.replace(" ", " ")
    linea = linea = linea.split(" ")  # se quitan espacios innecesarios y se divide la linea en palabras

    # Se valida la longitud de la linea, que tenga las palabras correctas, asi como el tipo y demas
    if linea[0] == "cargue":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "almacene":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "nueva":
        if len(linea) > 4 and linea[2] == "C" and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        if (len(linea) == 4 or len(linea) == 3) and not linea[1].isdigit() \
                and linea[1][0].isalpha():
            if linea[2] == "I" or linea[2] == "C" or linea[2] == "R" or linea[2] == "L" or linea[2] == 0 \
                    or linea[2] == 1:
                return True
            return False
        return False
    elif linea[0] == "lea":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "sume":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "reste":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "multiplique":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "divida":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "potencia":
        if len(linea) == 2 and linea[1].isnumeric():
            return True
        return False
    elif linea[0] == "modulo":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "concatene":
        if len(linea) == 2:
            return True
        return False
    elif linea[0] == "elimine":
        if len(linea) == 2:
            return True
        return False
    elif linea[0] == "extraiga":
        if len(linea) == 2 and linea[1].isnumeric():
            return True
        return False
    elif linea[0] == "Y":
        if len(linea) == 4 and not linea[1].isdigit() and linea[1][0].isalpha() and not linea[2].isdigit() \
                and linea[2][0].isalpha() and not linea[3].isdigit() and linea[3][0].isalpha():
            return True
        return False
    elif linea[0] == "O":
        if len(linea) == 4 and not linea[1].isdigit() and linea[1][0].isalpha() and not linea[2].isdigit() \
                and linea[2][0].isalpha() and not linea[3].isdigit() and linea[3][0].isalpha():
            return True
        return False
    elif linea[0] == "NO":
        if len(linea) == 3 and not linea[1].isdigit() and linea[1][0].isalpha() and not linea[2].isdigit() \
                and linea[2][0].isalpha():
            return True
        return False
    elif linea[0] == "muestre":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "imprima":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "retorne":
        if len(linea) == 2 and linea[1].isnumeric():
            return True
        return False
    elif linea[0] == "vaya":
        if len(linea) == 2 and not linea[1].isdigit() and linea[1][0].isalpha():
            return True
        return False
    elif linea[0] == "vayasi":
        if len(linea) == 3 and not linea[1].isdigit() and linea[1][0].isalpha() and not linea[2].isdigit() \
                and linea[2][0].isalpha():
            return True
        return False
    elif linea[0] == "etiqueta":
        if len(linea) == 3 and not linea[1].isdigit() and linea[1][0].isalpha() and linea[2].isnumeric():
            return True
        return False
    elif linea[0].startswith("//"):
        return True
    else:
        return False


def mostrar_texto(texto, left, top, var=False):
    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 12)
    color = color_amarillo
    if var == True:
        color = color_fondo
    espaciado = 5
    for t in texto:
        pantalla.blit((pygame.font.Font.render(fuente_aux, t, False, color)),
                      [left + 5, top + espaciado])
        espaciado += 15


def manejo_archivo(ruta, variables, etiquetas):
    archivo = open(ruta, 'r')
    instrucciones = archivo.read().splitlines()
    aux = ""
    paso = True
    programa = []

    # Por cada instruccion se valida su sintaxis llamando a la funcion validar_sintaxis
    for i in instrucciones:
        if i != "":
            if validar_sintaxis(i):
                aux += i + "\n"
            else:
                print("Error en sintaxix, linea ", instrucciones.index(i), i)
                mostrarError("Errores mostrados en la consola")
                paso = False

    # Si la sintaxtis es valida se cargan las variables, etiquetas y de una vez se guarda en la variable global
    # de programas nuestro programa
    if paso:
        ejecuciones = []

        for linea in instrucciones:
            linea = linea.strip()
            linea = linea.replace("       ", " ")
            linea = linea.replace("      ", " ")
            linea = linea.replace("     ", " ")
            linea = linea.replace("    ", " ")
            linea = linea.replace("   ", " ")
            linea = linea.replace("  ", " ")
            linea = linea.replace(" ", " ")
            if linea != "":
                ejecuciones.append(linea)
            linea = linea.split(" ")
            if linea[0] == "nueva":
                if len(linea) == 4:
                    variables[linea[1]] = [linea[2], str(linea[3])]
                else:
                    if linea[2] == 'C':
                        if len(linea) == 2:
                            variables[linea[1]] = [linea[2], ' ']
                        elif len(linea) > 4:
                            cantidad_palabras = len(linea)
                            resultado = ""
                            for pos in range(3, cantidad_palabras):
                                resultado += " " + linea[pos]
                            variables[linea[1]] = [linea[2], resultado]
                    elif linea[2] == 'R':
                        variables[linea[1]] = [linea[2], '0']
                    elif linea[2] == 'L':
                        variables[linea[1]] = [linea[2], '0']
                    else:
                        variables[linea[1]] = [linea[2], '0']
            elif linea[0] == "etiqueta":
                etiquetas[linea[1]] = int(linea[2])

        for ej in ejecuciones:
            programa.append(ej)
        for et in etiquetas.items():
            programa.append(et)
        for va in variables.items():
            programa.append(va)
    return paso, aux, programa


f = "<No File Selected>"


def ejecucion(programa, acumulador, variables, etiquetas, texto_pc, continuar):
    acumulador_1 = acumulador
    variables_aux = variables
    etiquetas_aux = etiquetas
    texto_pc_aux = texto_pc
    texto_impresora_aux = "texto ejemplo impresora"

    for instruccion in programa:
        # print(">> ", programa.index(instruccion), " - ", instruccion)
        linea = instruccion.split(" ")
        if linea[0] == "nueva":

            # Estructura diccionario :
            # "nombre_variable": ["tipo","valor"]

            if linea[3]:
                variables_aux[linea[1]] = [linea[2], linea[3]]
            else:
                if [linea[2]] == 'C':
                    variables_aux[linea[1]] = [linea[2], ' ']
                elif [linea[2]] == 'R':
                    variables_aux[linea[1]] = [linea[2], '0']
                elif [linea[2]] == 'L':
                    variables_aux[linea[1]] = [linea[2], '0']
                else:
                    variables_aux[linea[1]] = [linea[2], '0']
        elif linea[0] == "cargue":
            acumulador_1 = variables_aux[linea[1]]
        elif linea[0] == "almacene":
            variables_aux[linea[1]] = acumulador_1
        elif linea[0] == "lea":
            aux = input("Ingrese el nuevo valor de la variable " + str(linea[1]) + " : ")
            particion = aux.partition('.')

            if aux.isdigit() and aux != '0' and aux != '1':
                variables_aux[linea[1]][1] = int(aux)
                variables_aux[linea[1]][0] = 'I'

            elif (particion[0].isdigit() and particion[1] == '.' and particion[2].isdigit()) or (
                    particion[0] == '' and particion[1] == '.' and particion[2].isdigit()) or (
                    particion[0].isdigit() and particion[1] == '.' and particion[2] == ''):
                variables_aux[linea[1]][1] = float(aux)
                variables_aux[linea[1]][0] = 'R'

            elif aux == '1' or aux == '0':
                if aux == '1':
                    variables_aux[linea[1]][1] = True
                else:
                    variables_aux[linea[1]][1] = False
                variables_aux[linea[1]][0] = 'L'
            else:
                variables_aux[linea[1]][1] = aux
                variables_aux[linea[1]][0] = 'C'

        elif linea[0] == "sume":
            if acumulador_1[0] == 'I' or acumulador_1[0] == 'R':
                if acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'I':
                    acumulador_1[1] = int(acumulador_1[1]) + int(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = int(acumulador_1[1]) + float(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'R' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = float(acumulador_1[1]) + float(variables_aux[linea[1]][1])
                else:
                    acumulador_1[1] = float(acumulador_1[1]) + int(variables_aux[linea[1]][1])

        elif linea[0] == "reste":
            # validar parte logica here
            if acumulador_1[0] == 'I' or acumulador_1[0] == 'R':
                if acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'I':
                    acumulador_1[1] = int(acumulador_1[1]) - int(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = int(acumulador_1[1]) - float(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'R' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = float(acumulador_1[1]) - float(variables_aux[linea[1]][1])
                else:
                    acumulador_1[1] = float(acumulador_1[1]) - int(variables_aux[linea[1]][1])

        elif linea[0] == "multiplique":
            if acumulador_1[0] == 'I' or acumulador_1[0] == 'R':
                if acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'I':
                    acumulador_1[1] = int(acumulador_1[1]) * int(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = int(acumulador_1[1]) * float(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'R' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = float(acumulador_1[1]) * float(variables_aux[linea[1]][1])
                else:
                    acumulador_1[1] = float(acumulador_1[1]) * int(variables_aux[linea[1]][1])

        elif linea[0] == "divida":
            if acumulador_1[0] == 'I' or acumulador_1[0] == 'R':
                if acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'I':
                    acumulador_1[1] = int(acumulador_1[1]) / int(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = int(acumulador_1[1]) / float(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'R' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = float(acumulador_1[1]) / float(variables_aux[linea[1]][1])
                else:
                    acumulador_1[1] = float(acumulador_1[1]) / int(variables_aux[linea[1]][1])

        elif linea[0] == "potencia":
            if acumulador_1[0] == 'I' or acumulador_1[0] == 'R':
                if acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'I':
                    acumulador_1[1] = int(acumulador_1[1]) ** int(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = int(acumulador_1[1]) ** float(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'R' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = float(acumulador_1[1]) ** float(variables_aux[linea[1]][1])
                else:
                    acumulador_1[1] = float(acumulador_1[1]) ** int(variables_aux[linea[1]][1])

        elif linea[0] == "modulo":
            if acumulador_1[0] == 'I' or acumulador_1[0] == 'R':
                if acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'I':
                    acumulador_1[1] = int(acumulador_1[1]) % int(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'I' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = int(acumulador_1[1]) % float(variables_aux[linea[1]][1])
                elif acumulador_1[0] == 'R' and variables_aux[linea[1]][0] == 'R':
                    acumulador_1[1] = float(acumulador_1[1]) % float(variables_aux[linea[1]][1])
                else:
                    acumulador_1[1] = float(acumulador_1[1]) % int(variables_aux[linea[1]][1])

        elif linea[0] == "concatene":
            acumulador_1 = str(acumulador_1) + str(variables_aux[linea[1]])
        elif linea[0] == "elimine":
            (str(acumulador_1)).replace(str(linea[1]), "")
        elif linea[0] == "extraiga":
            aux = []
            aux[:0] = str(acumulador_1)
            acumulador_1 = aux[linea[1]:]
        elif linea[0] == "Y":
            variables_aux[linea[3]] = variables_aux[linea[1]] and variables_aux[linea[2]]
        elif linea[0] == "O":
            variables_aux[linea[3]] = variables_aux[linea[1]] or variables_aux[linea[2]]
        elif linea[0] == "NO":
            variables_aux[linea[2]] = not variables_aux[linea[1]]
        elif linea[0] == "muestre":
            # Muestre por el monitor de pc
            texto_pc_aux = variables_aux[linea[1]]
        elif linea[0] == "imprima":
            texto_impresora_aux = variables_aux[linea[1]]
        elif linea[0] == "vaya":
            return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux
        elif linea[0] == "vayasi":
            if acumulador_1[1] > 0:
                """
                aux = programa[etiquetas_aux[linea[1]] + 1:]
                variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux = ejecucion(aux,
                                                                                                          acumulador_1,
                                                                                                          variables_aux,
                                                                                                          etiquetas_aux,
                                                                                                          texto_pc_aux)
                                                                                                          """
                return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux, True

            elif acumulador_1[1] < 0:
                """ aux = programa[etiquetas_aux[linea[2]] + 1:]
                               variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux = ejecucion(aux,
                                                                                                          acumulador_1,
                                                                                                          variables_aux,
                                                                                                          etiquetas_aux,
                                                                                                          texto_pc_aux)"""
                return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux, True
            else:
                pass
        elif linea[0] == "etiqueta":
            # etiqueta estructura:{'nombre':posicion}
            etiquetas_aux[linea[1]] = int(linea[2])

        elif linea[0] == "retorne":
            return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux, False

    return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux, False


def modo_paso_a_paso(acumulador, variables, etiquetas, instruccion):
    texto_pc = "texto ejemplo pc"
    texto_impresora = "texto ejemplo impresora"
    continuar = False
    linea = instruccion.split(" ")

    if linea[0] == "nueva":
        if len(linea) == 4:
            variables[linea[1]] = [linea[2], str(linea[3])]
        else:
            if linea[2] == 'C':
                if len(linea) == 2:
                    variables[linea[1]] = [linea[2], ' ']
                elif len(linea) > 4:
                    cantidad_palabras = len(linea)
                    resultado = ""
                    for pos in range(3, cantidad_palabras):
                        resultado += " " + linea[pos]
                    variables[linea[1]] = [linea[2], resultado]
            elif linea[2] == 'R':
                variables[linea[1]] = [linea[2], '0']
            elif linea[2] == 'L':
                variables[linea[1]] = [linea[2], '0']
            else:
                variables[linea[1]] = [linea[2], '0']
    elif linea[0] == "cargue":
        acumulador = [variables[linea[1]][0], variables[linea[1]][1]]
    elif linea[0] == "almacene":
        variables[linea[1]] = acumulador
    elif linea[0] == "lea":
        aux = input("Ingrese el nuevo valor de la variable " + str(linea[1]) + " : ")
        particion = aux.partition('.')

        if aux.isdigit() and aux != '0' and aux != '1':
            variables[linea[1]][1] = int(aux)
            variables[linea[1]][0] = 'I'

        elif (particion[0].isdigit() and particion[1] == '.' and particion[2].isdigit()) or (
                particion[0] == '' and particion[1] == '.' and particion[2].isdigit()) or (
                particion[0].isdigit() and particion[1] == '.' and particion[2] == ''):
            variables[linea[1]][1] = float(aux)
            variables[linea[1]][0] = 'R'

        elif aux == '1' or aux == '0':
            if aux == '1':
                variables[linea[1]][1] = True
            else:
                variables[linea[1]][1] = False
            variables[linea[1]][0] = 'L'
        else:
            variables[linea[1]][1] = aux
            variables[linea[1]][0] = 'C'

        # print(variables[linea[1]][1], type(variables[linea[1]]))

    elif linea[0] == "sume":
        if acumulador[0] == 'I' or acumulador[0] == 'R':
            if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                acumulador[1] = int(acumulador[1]) + int(variables[linea[1]][1])
            elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                acumulador[1] = int(acumulador[1]) + float(variables[linea[1]][1])

            elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                acumulador[1] = float(acumulador[1]) + float(variables[linea[1]][1])
            else:
                acumulador[1] = float(acumulador[1]) + int(variables[linea[1]][1])

    elif linea[0] == "reste":
        # validar parte logica here
        if acumulador[0] == 'I' or acumulador[0] == 'R':
            if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                acumulador[1] = int(acumulador[1]) - int(variables[linea[1]][1])
            elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                acumulador[1] = int(acumulador[1]) - float(variables[linea[1]][1])
            elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                acumulador[1] = float(acumulador[1]) - float(variables[linea[1]][1])
            else:
                acumulador[1] = float(acumulador[1]) - int(variables[linea[1]][1])

    elif linea[0] == "multiplique":
        if acumulador[0] == 'I' or acumulador[0] == 'R':
            if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                acumulador[1] = int(acumulador[1]) * int(variables[linea[1]][1])
            elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                acumulador[1] = int(acumulador[1]) * float(variables[linea[1]][1])
            elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                acumulador[1] = float(acumulador[1]) * float(variables[linea[1]][1])
            else:
                acumulador[1] = float(acumulador[1]) * int(variables[linea[1]][1])

    elif linea[0] == "divida":
        if acumulador[0] == 'I' or acumulador[0] == 'R':
            if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                acumulador[1] = int(acumulador[1]) / int(variables[linea[1]][1])
            elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                acumulador[1] = int(acumulador[1]) / float(variables[linea[1]][1])
            elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                acumulador[1] = float(acumulador[1]) / float(variables[linea[1]][1])
            else:
                acumulador[1] = float(acumulador[1]) / int(variables[linea[1]][1])

    elif linea[0] == "potencia":
        if acumulador[0] == 'I' or acumulador[0] == 'R':
            if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                acumulador[1] = int(acumulador[1]) ** int(variables[linea[1]][1])
            elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                acumulador[1] = int(acumulador[1]) ** float(variables[linea[1]][1])
            elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                acumulador[1] = float(acumulador[1]) ** float(variables[linea[1]][1])
            else:
                acumulador[1] = float(acumulador[1]) ** int(variables[linea[1]][1])

    elif linea[0] == "modulo":
        if acumulador[0] == 'I' or acumulador[0] == 'R':
            if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                acumulador[1] = int(acumulador[1]) % int(variables[linea[1]][1])
            elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                acumulador[1] = int(acumulador[1]) % float(variables[linea[1]][1])
            elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                acumulador[1] = float(acumulador[1]) % float(variables[linea[1]][1])
            else:
                acumulador[1] = float(acumulador[1]) % int(variables[linea[1]][1])

    elif linea[0] == "concatene":
        acumulador = str(acumulador) + str(variables[linea[1]])
    elif linea[0] == "elimine":
        (str(acumulador)).replace(str(linea[1]), "")
    elif linea[0] == "extraiga":
        aux = []
        aux[:0] = str(acumulador)
        acumulador = aux[linea[1]:]
    elif linea[0] == "Y":
        variables[linea[3]] = variables[linea[1]] and variables[linea[2]]
    elif linea[0] == "O":
        variables[linea[3]] = variables[linea[1]] or variables[linea[2]]
    elif linea[0] == "NO":
        variables[linea[2]] = not variables[linea[1]]
    elif linea[0] == "muestre":
        # Muestre por el monitor de pc
        texto_pc = variables[linea[1]]
    elif linea[0] == "imprima":
        texto_impresora = variables[linea[1]][1]
    elif linea[0] == "vaya":
        aux = programa[etiquetas[linea[1]]:]
        variables, acumulador, etiquetas, texto_pc, texto_impresora = ejecucion(aux, acumulador, variables,
                                                                                etiquetas, texto_pc, False)
    elif linea[0] == "vayasi":
        if acumulador[1] > 0:
            aux = programa[etiquetas[linea[1]] - 1:]

            variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                               variables,
                                                                                               etiquetas, texto_pc,
                                                                                               continuar)

            while continuar:
                variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                                   variables,
                                                                                                   etiquetas,
                                                                                                   texto_pc,
                                                                                                   continuar)
        elif acumulador[1] < 0:
            aux = programa[etiquetas[linea[2]] - 1:]
            variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                               variables,
                                                                                               etiquetas, texto_pc,
                                                                                               continuar)
            while continuar:
                variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                                   variables,
                                                                                                   etiquetas,
                                                                                                   texto_pc,
                                                                                                   continuar)
        else:
            pass

    elif linea[0] == "etiqueta":
        etiquetas[linea[1]] = int(linea[2])

    elif linea[0] == "retorne":
        return variables, acumulador, etiquetas, texto_pc, texto_impresora
    return variables, acumulador, etiquetas, texto_pc, texto_impresora


def ejecutar_programa(programa, variables, etiquetas, acumulador):
    texto_pc = "texto ejemplo pc"
    texto_impresora = "texto ejemplo impresora"
    pos = []
    continuar = False
    for instruccion in programa:
        if instruccion == "":
            pos.append(programa.index(instruccion))
    for p in pos:
        programa.pop(p)
    for instruccion in programa:
        instruccion = instruccion.strip()
        instruccion = instruccion.replace("       ", " ")
        instruccion = instruccion.replace("      ", " ")
        instruccion = instruccion.replace("     ", " ")
        instruccion = instruccion.replace("    ", " ")
        instruccion = instruccion.replace("   ", " ")
        instruccion = instruccion.replace("  ", " ")
        instruccion = instruccion.replace(" ", " ")
        linea = instruccion.split(" ")
        # print(">> ", programa.index(instruccion), " - ", instruccion)

        if linea[0] == "nueva":
            if len(linea) == 4:
                variables[linea[1]] = [linea[2], str(linea[3])]
            else:
                if linea[2] == 'C':
                    if len(linea) == 2:
                        variables[linea[1]] = [linea[2], ' ']
                    elif len(linea) > 4:
                        cantidad_palabras = len(linea)
                        resultado = ""
                        for pos in range(3, cantidad_palabras):
                            resultado += " " + linea[pos]
                        variables[linea[1]] = [linea[2], resultado]
                elif linea[2] == 'R':
                    variables[linea[1]] = [linea[2], '0']
                elif linea[2] == 'L':
                    variables[linea[1]] = [linea[2], '0']
                else:
                    variables[linea[1]] = [linea[2], '0']
        elif linea[0] == "cargue":
            acumulador = [variables[linea[1]][0], variables[linea[1]][1]]
        elif linea[0] == "almacene":
            variables[linea[1]] = acumulador
        elif linea[0] == "lea":
            aux = input("Ingrese el nuevo valor de la variable " + str(linea[1]) + " : ")
            particion = aux.partition('.')

            if aux.isdigit() and aux != '0' and aux != '1':
                variables[linea[1]][1] = int(aux)
                variables[linea[1]][0] = 'I'

            elif (particion[0].isdigit() and particion[1] == '.' and particion[2].isdigit()) or (
                    particion[0] == '' and particion[1] == '.' and particion[2].isdigit()) or (
                    particion[0].isdigit() and particion[1] == '.' and particion[2] == ''):
                variables[linea[1]][1] = float(aux)
                variables[linea[1]][0] = 'R'

            elif aux == '1' or aux == '0':
                if aux == '1':
                    variables[linea[1]][1] = True
                else:
                    variables[linea[1]][1] = False
                variables[linea[1]][0] = 'L'
            else:
                variables[linea[1]][1] = aux
                variables[linea[1]][0] = 'C'

        elif linea[0] == "sume":
            if acumulador[0] == 'I' or acumulador[0] == 'R':
                if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                    acumulador[1] = int(acumulador[1]) + int(variables[linea[1]][1])
                elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                    acumulador[1] = int(acumulador[1]) + float(variables[linea[1]][1])

                elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                    acumulador[1] = float(acumulador[1]) + float(variables[linea[1]][1])
                else:
                    acumulador[1] = float(acumulador[1]) + int(variables[linea[1]][1])

        elif linea[0] == "reste":
            # validar parte logica here
            if acumulador[0] == 'I' or acumulador[0] == 'R':
                if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                    acumulador[1] = int(acumulador[1]) - int(variables[linea[1]][1])
                elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                    acumulador[1] = int(acumulador[1]) - float(variables[linea[1]][1])
                elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                    acumulador[1] = float(acumulador[1]) - float(variables[linea[1]][1])
                else:
                    acumulador[1] = float(acumulador[1]) - int(variables[linea[1]][1])

        elif linea[0] == "multiplique":
            if acumulador[0] == 'I' or acumulador[0] == 'R':
                if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                    acumulador[1] = int(acumulador[1]) * int(variables[linea[1]][1])
                elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                    acumulador[1] = int(acumulador[1]) * float(variables[linea[1]][1])
                elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                    acumulador[1] = float(acumulador[1]) * float(variables[linea[1]][1])
                else:
                    acumulador[1] = float(acumulador[1]) * int(variables[linea[1]][1])

        elif linea[0] == "divida":
            if acumulador[0] == 'I' or acumulador[0] == 'R':
                if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                    acumulador[1] = int(acumulador[1]) / int(variables[linea[1]][1])
                elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                    acumulador[1] = int(acumulador[1]) / float(variables[linea[1]][1])
                elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                    acumulador[1] = float(acumulador[1]) / float(variables[linea[1]][1])
                else:
                    acumulador[1] = float(acumulador[1]) / int(variables[linea[1]][1])

        elif linea[0] == "potencia":
            if acumulador[0] == 'I' or acumulador[0] == 'R':
                if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                    acumulador[1] = int(acumulador[1]) ** int(variables[linea[1]][1])
                elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                    acumulador[1] = int(acumulador[1]) ** float(variables[linea[1]][1])
                elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                    acumulador[1] = float(acumulador[1]) ** float(variables[linea[1]][1])
                else:
                    acumulador[1] = float(acumulador[1]) ** int(variables[linea[1]][1])

        elif linea[0] == "modulo":
            if acumulador[0] == 'I' or acumulador[0] == 'R':
                if acumulador[0] == 'I' and variables[linea[1]][0] == 'I':
                    acumulador[1] = int(acumulador[1]) % int(variables[linea[1]][1])
                elif acumulador[0] == 'I' and variables[linea[1]][0] == 'R':
                    acumulador[1] = int(acumulador[1]) % float(variables[linea[1]][1])
                elif acumulador[0] == 'R' and variables[linea[1]][0] == 'R':
                    acumulador[1] = float(acumulador[1]) % float(variables[linea[1]][1])
                else:
                    acumulador[1] = float(acumulador[1]) % int(variables[linea[1]][1])

        elif linea[0] == "concatene":
            acumulador = str(acumulador) + str(variables[linea[1]])
        elif linea[0] == "elimine":
            (str(acumulador)).replace(str(linea[1]), "")
        elif linea[0] == "extraiga":
            aux = []
            aux[:0] = str(acumulador)
            acumulador = aux[linea[1]:]
        elif linea[0] == "Y":
            variables[linea[3]] = variables[linea[1]] and variables[linea[2]]
        elif linea[0] == "O":
            variables[linea[3]] = variables[linea[1]] or variables[linea[2]]
        elif linea[0] == "NO":
            variables[linea[2]] = not variables[linea[1]]
        elif linea[0] == "muestre":
            # Muestre por el monitor de pc
            texto_pc = variables[linea[1]]
        elif linea[0] == "imprima":
            texto_impresora = variables[linea[1]][1]
        elif linea[0] == "vaya":
            aux = programa[etiquetas[linea[1]]:]
            variables, acumulador, etiquetas, texto_pc, texto_impresora = ejecucion(aux, acumulador, variables,
                                                                                    etiquetas, texto_pc, False)
        elif linea[0] == "vayasi":
            if acumulador[1] > 0:
                aux = programa[etiquetas[linea[1]] - 1:]
                print("empieza desde ", aux)
                variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                                   variables,
                                                                                                   etiquetas, texto_pc,
                                                                                                   continuar)

                while continuar:
                    variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                                       variables,
                                                                                                       etiquetas,
                                                                                                       texto_pc,
                                                                                                       continuar)
                print("Termino")
            elif acumulador[1] < 0:
                aux = programa[etiquetas[linea[2]] - 1:]
                variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                                   variables,
                                                                                                   etiquetas, texto_pc,
                                                                                                   continuar)

                while continuar:
                    variables, acumulador, etiquetas, texto_pc, texto_impresora, continuar = ejecucion(aux, acumulador,
                                                                                                       variables,
                                                                                                       etiquetas,
                                                                                                       texto_pc,
                                                                                                       continuar)
            else:
                pass

        elif linea[0] == "etiqueta":
            etiquetas[linea[1]] = int(linea[2])

        elif linea[0] == "retorne":
            return variables, acumulador, etiquetas, texto_pc, texto_impresora
        else:
            pass
    return variables, acumulador, etiquetas, texto_pc, texto_impresora


def mostrar_variables(variables):
    llaves = variables.keys()
    res = ""
    for llave in llaves:
        if str(variables[llave][0]).lower() == 'c':
            res += llave + "     " + str(variables[llave][0]).lower() + " | '" + str(variables[llave][1]) + "'\n"
        else:
            res += llave + "     " + str(variables[llave][0]).lower() + " | " + str(variables[llave][1]) + "\n"
    res = res.split("\n")
    return res


def mostrar_etiquetas(etiquetas):
    llaves = etiquetas.keys()
    res = ""
    for llave in llaves:
        res += llave + " | " + str(etiquetas[llave]) + "\n"
    res = res.split("\n")
    return res


# Metodo que muestra en un recuadro con estilo cualquier mensaje de error
def mostrarError(texto):
    cuadro_error = pygame.draw.rect(pantalla, color_rojo, pygame.Rect(30, lado_derecho_surface.get_rect().bottom - 50,
                                                                      lado_derecho_surface.get_rect().width * 1.65, 55),
                                    0, 15)
    pantalla.blit((pygame.font.Font.render(fuente, str(texto), False, color_amarillo)),
                  [cuadro_error.left + 5, cuadro_error.top + 15])


# Muestra el array por pantalla
def cargar_memoria(programas):
    memoria_principal[0] = "Acumulador :" + str(acumulador[1])
    for k in range(kernel):
        memoria_principal[k + 1] = ("J" + str(k) + " Kernel")

    contador = 0
    for programa in programas:
        for instruccion in range(len(programa)):
            if type(programa[instruccion]) != tuple:
                memoria_principal[contador + kernel] = [("J" + str(contador + kernel)), programa[instruccion]]
            else:
                if type(programa[instruccion][1]) != list:
                    memoria_principal[contador + kernel] = [("J" + str(contador + kernel)), (
                            str(programa[instruccion][0]) + " " + str(programa[instruccion][1]))]
                else:
                    memoria_principal[contador + kernel] = [("J" + str(contador + kernel)), (
                            str(programa[instruccion][0]) + " " + str(programa[instruccion][1][0]) + " " + str(
                        programa[instruccion][1][1]))]
            contador += 1


# Muestra el array por pantalla de memoria
def mostrar_memoria():
    espaciado = 5
    aux = (len(memoria_principal) * lado_derecho_surface.get_rect().height) / 32
    memoria_surface = pygame.Surface((lado_izquierdo.width - 30, aux))
    memoria_surface.fill(color_azul_oscuro)
    fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 16)
    contador = 0
    for instrucccion in memoria_principal:
        if type(instrucccion) is list:
            memoria_surface.blit(
                (pygame.font.Font.render(fuente, str(instrucccion[0] + " " + str(instrucccion[1])), False,
                                         colores_programas[contador])),
                [memoria_surface.get_rect().left + 2, memoria_surface.get_rect().top + espaciado])

        else:
            memoria_surface.blit(
                (pygame.font.Font.render(fuente, str(instrucccion), False, colores_programas[contador])),
                [memoria_surface.get_rect().left + 2, memoria_surface.get_rect().top + espaciado])

        espaciado += 20
    lado_derecho_surface.blit(memoria_surface, (0, scrollbar.y_axis))


def paso_a_paso_programa(programa, texto_paso, texto_variables, texto_etiquetas, texto_impresora, texto_pc,
                         contador_paso_a_paso,
                         acumulador, variables, etiquetas):
    print("paso ", contador_paso_a_paso)
    # para el programa 0 ir a la instruccion i
    if contador_paso_a_paso == 0:
        acumulador = ['I', 0]
        variables = {}
        etiquetas = {}

    if contador_paso_a_paso < len(programa):
        instruccion = programa[contador_paso_a_paso]
        # si no es una tupla con variables, etiquetas, etc; lo imprimo
        if type(instruccion) != tuple:
            print(instruccion)
            texto_paso = str(instruccion)
            texto_variables = mostrar_variables(variables)
            texto_etiquetas = mostrar_etiquetas(etiquetas)
            ejecucion = modo_paso_a_paso(acumulador, variables, etiquetas, instruccion)
            print("retorno ", ejecucion)
            texto_impresora = ejecucion[4]
            texto_pc = ejecucion[3]

    print("---")
    contador_paso_a_paso += 1
    return texto_paso, texto_variables, texto_etiquetas, texto_impresora, texto_pc, contador_paso_a_paso, acumulador, variables, etiquetas


# Se ingresa al ciclo de pygame
while True:
    for event in pygame.event.get():
        # Muestra de componentes graficos
        pantalla.fill(color_fondo)
        pygame.draw.rect(pantalla, color_azul,
                         pygame.Rect(10, 10, (ancho / 5), lado_derecho_surface.get_rect().height + 23), 12, 15)

        lado_izquierdo = pygame.draw.rect(pantalla, color_gris,
                                          pygame.Rect(12, 12, (ancho / 5) - 3,
                                                      lado_derecho_surface.get_rect().height + 20), 0, 15)

        contador = poner_botones(20, contador)[6]
        resultado = poner_botones(20, contador)[7]
        res = poner_botones(20, contador)

        if resultado:
            texto_variables = mostrar_variables(resultado[0])
            acumulador = resultado[1]
            texto_etiquetas = mostrar_etiquetas(resultado[2])
            texto_paso = memoria_principal[contador + kernel]

        pc = pantalla.blit(pc_img, (pantalla.get_rect().width / 2 - 120, pantalla.get_rect().top + 5))
        pantalla.blit((pygame.font.Font.render(fuente, "texto ejemplo pc", False, color_amarillo)),
                      [pc.centerx, pc.top + 5])

        impresora = pantalla.blit(impresora_img, (pantalla.get_rect().width / 2 - 120, pc.bottom + 5))
        pantalla.blit((pygame.font.Font.render(fuente, str(texto_impresora), False, color_fondo)),
                      [impresora.centerx - 90, impresora.top + 15])

        pygame.draw.rect(pantalla, color_azul,
                         pygame.Rect(pc.right + 80, pantalla.get_rect().top + 5, (ancho / 5),
                                     lado_derecho_surface.get_rect().height + 26), 12, 15)

        pc = pantalla.blit(pc_img, (pantalla.get_rect().width / 2 - 120, pantalla.get_rect().top + 5))

        pantalla.blit((pygame.font.Font.render(fuente, str(texto_pc), False, color_fondo)),
                      [pc.centerx - pc.centerx / 4.5, pc.centery - pc.centery / 1.5])

        lado_derecho = pygame.draw.rect(pantalla, color_menu_izquierdo,
                                        pygame.Rect(pc.right + 82, pantalla.get_rect().top + 7, (ancho / 5) - 4,
                                                    lado_derecho_surface.get_rect().height + 20), 0, 15)

        boton = pygame.Rect(313, 70, 80, 80)
        play = pygame.draw.rect(pantalla, color_azul, boton, 0, 10)
        pantalla.blit(play_img, [play.left + 10, play.top + 10])

        # Si se sale de la equis se sale del sys
        if event.type == pygame.QUIT:
            sys.exit()

        # si seleccionamos con el mouse ingresa, alli se valida que boton fue seleccionado
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Boton cargue
            # Si se selecciona el boton de cargar .ch entra
            if poner_botones(20, contador)[0].collidepoint(pygame.mouse.get_pos()):
                # Si no hay valores para memoria y kernel muestra error
                if memoria == 0 or kernel == 0:
                    mostrarError("Establezca valores para memoria y kernel")
                else:
                    # Valida que sea el correcto espacio maximo
                    if (memoria + kernel) <= 5100:
                        f = prompt_file()
                        # Se llama a la funcion manejo_archivo que abre el cuadro de dialogo y trae el archivo para
                        # validar su sintaxix
                        programa = manejo_archivo(f, variables, etiquetas)

                        if programa[0]:
                            pantalla.fill(color_azul)
                            texto_codigo = programa[1].split("\n")
                        if programa[2]:
                            programas.append(programa[2])
                            cargar_memoria(programas)
                            color = pygame.color.Color(tuple(random.choice(levels) for _ in range(3)))
                            if color not in colores_programas:
                                colores_programas.append(color)
                            else:
                                while color in colores_programas:
                                    color = pygame.color.Color(tuple(random.choice(levels) for _ in range(3)))
                                colores_programas.append(color)
                            print(colores_programas)
                            # texto_variables = mostrar_variables(variables)
                            # texto_etiquetas = mostrar_etiquetas(etiquetas)
                    else:
                        mostrarError("Memoria principal con longitud superior")
            # Acciones para botones de aumento y dism para var kernel y memoria
            elif poner_botones(20, contador)[1].collidepoint(pygame.mouse.get_pos()):
                memoria += 10
            elif poner_botones(20, contador)[2].collidepoint(pygame.mouse.get_pos()) and memoria > 0:
                memoria -= 10
            elif poner_botones(20, contador)[3].collidepoint(pygame.mouse.get_pos()):
                kernel += 10
            elif poner_botones(20, contador)[4].collidepoint(pygame.mouse.get_pos()) and kernel > 0:
                kernel -= 10
            # Si ya se cargo el programa se pasa al modo usuario donde se habilita la opcion de play y paso a paso
            elif play.collidepoint(pygame.mouse.get_pos()):
                if len(programas) > 0:
                    if boton_SJF_active or boton_RR_active or boton_fcfs_active or boton_EXP_active:
                        texto_modo = "U S U A R I O"

                        if boton_fcfs_active:
                            print("Ejecutando FCFS")
                            print("...............")
                            for prog in programas:
                                print(variables, etiquetas, acumulador)
                                print("...............")
                                acumulador = ['I', 0]
                                resultado = metodo_fcfs(prog, variables, etiquetas, acumulador)
                                # resultado = ejecutar_programa(prog, variables, etiquetas, acumulador)

                        if boton_RR_active:
                            resultado = metodo_RR(prog, variables, etiquetas, acumulador)

                        """aqui"""
                        if resultado:
                            texto_variables = mostrar_variables(resultado[0])
                            texto_etiquetas = mostrar_etiquetas(resultado[2])
                            texto_pc = resultado[3]
                            texto_impresora = resultado[4]
                            acumulador = resultado[1]
                            print("resultado ", resultado)
                            for n in programas:
                                print("Programas >> ", n)
                    else:
                        mostrarError("Seleccione un algoritmo de planificacion")
                else:
                    mostrarError("No hay programas cargados aun")
            elif poner_botones(20, contador)[5].collidepoint(pygame.mouse.get_pos()):
                # entra si se selecciona el boton de paso a paso
                if boton_SJF_active or boton_RR_active or boton_fcfs_active or boton_EXP_active:
                    if len(programas) > 0:
                        texto_modo = "U S U A R I O"
                        # si hay programas cargados ya
                        print("paso ", contador_paso_a_paso)
                        # para el programa 0 ir a la instruccion i
                        if contador_paso_a_paso == 0:
                            acumulador = ['I', 0]
                            variables = {}
                            etiquetas = {}

                        if contador_paso_a_paso < len(programas[0]):
                            instruccion = programas[0][contador_paso_a_paso]
                            # si no es una tupla con variables, etiquetas, etc; lo imprimo
                            if type(instruccion) != tuple:
                                texto_paso = str(instruccion)
                                texto_variables = mostrar_variables(variables)
                                texto_etiquetas = mostrar_etiquetas(etiquetas)
                                ejecucion = modo_paso_a_paso(acumulador, variables, etiquetas, instruccion)
                                texto_impresora = ejecucion[4]
                                texto_pc = ejecucion[3]

                        contador_paso_a_paso += 1
                    else:
                        mostrarError("No hay programas cargados aun")
                else:
                    mostrarError("Seleccione un algoritmo de planificacion")
            elif poner_botones(20, contador)[8].collidepoint(pygame.mouse.get_pos()):
                if not boton_RR_active and not boton_SJF_active and not boton_EXP_active:
                    boton_fcfs_active = not boton_fcfs_active
                # metodo_fcfs()
            elif poner_botones(20, contador)[9].collidepoint(pygame.mouse.get_pos()):
                if not boton_fcfs_active and not boton_SJF_active and not boton_EXP_active and not boton_PRI_active:
                    boton_RR_active = not boton_RR_active
            elif poner_botones(20, contador)[10].collidepoint(pygame.mouse.get_pos()):
                if not boton_fcfs_active and not boton_RR_active and not boton_EXP_active and not boton_PRI_active:
                    boton_SJF_active = not boton_SJF_active
            elif poner_botones(20, contador)[11].collidepoint(pygame.mouse.get_pos()):
                if not boton_fcfs_active and not boton_RR_active and not boton_SJF_active and not boton_PRI_active:
                    boton_EXP_active = not boton_EXP_active
            elif poner_botones(20, contador)[12].collidepoint(pygame.mouse.get_pos()):
                if not boton_fcfs_active and not boton_RR_active and not boton_SJF_active and not boton_EXP_active:
                    boton_PRI_active = not boton_PRI_active
            elif poner_botones(20, contador)[13].collidepoint(pygame.mouse.get_pos()):
                if quantum >= 0:
                    quantum += 1
            elif poner_botones(20, contador)[14].collidepoint(pygame.mouse.get_pos()):
                if quantum > 0:
                    quantum -= 1

        scrollbar.event_handler(event)
    # Metodos graficos
    lado_derecho_surface.fill(pygame.color.Color("#EEABB3"))
    scrollbar.draw(lado_derecho_surface)

    # Muestra el array de memoria en pantalla
    mostrar_memoria()

    # Metodos graficos
    pantalla.blit(lado_derecho_surface, (872 + padding, 7 + padding))
    scrollbar.update()
    pygame.display.flip()
    clock.tick(30)
