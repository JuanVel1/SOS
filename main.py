import sys
import pygame
import tkinter.filedialog
import tkinter
from emoji import emojize

# CTRL + ALT + L --> FORMAT
pygame.init()
ancho, alto = 1100, 700
velocidad = [2, 2]
color_fondo = pygame.color.Color("#475B5A")
color_menu_izquierdo = pygame.color.Color("#BBBBBF")
color_azul = pygame.color.Color("#52D1DC")
fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 18)
color_gris = (197, 194, 197)
color_amarillo = pygame.color.Color("#f5f3bb")
color_amarillo_claro = pygame.color.Color("#f2f5ea")
color_rojo = pygame.color.Color("#CC2936")
color_azul_oscuro = pygame.color.Color("#284B63")
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("CH Maquina 2022")
pc_img = pygame.image.load("imgs/Captura.PNG")
impresora_img = pygame.image.load("imgs/impresora.PNG")
play_img = pygame.image.load("imgs/play.png")
clock = pygame.time.Clock()

icono = pygame.image.load("imgs/icono.png")
pygame.display.set_icon(icono)
hay_programa = False
texto_codigo = "Aqui va el programa :)"
texto_variables = "Aqui van las variables"
texto_etiquetas = "Aqui van las etiquetas"
texto_pc = "texto ejemplo pc"
texto_impresora = "texto ejemplo impresora"

# default_cursor = pygame.mouse.get_cursor()
# el chcomputador empieza con Z*10 + 50 posiciones de memoria para facilitar el proceso de pruebas.Z = 5
memoria = 100
# 10*Z + 9 posiciones.Z = 5
kernel = 59
memoria_principal = list(range(memoria + kernel))
programas = []
acumulador = ['I', 0]
image = pygame.image.load("imgs/instruments.png").convert()

padding = 5
lado_derecho_surface = pygame.Surface((216 - padding * 2, alto - 50))


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


# 1600 -->78

scrollbar = ScrollBar((len(memoria_principal) * 1600) / 79.5)


def poner_boton(pos_x, pos_y, superficie):
    boton = pygame.Rect(pos_x, pos_y, (ancho / 7), 40)
    clickeable = pygame.draw.rect(superficie, color_azul, boton, 0, 15)
    return clickeable


def poner_textbox(pos_x, pos_y, superficie):
    boton = pygame.Rect(pos_x, pos_y, (ancho / 6), 500)
    clickeable = pygame.draw.rect(superficie, color_azul, boton, 0, 15)
    return clickeable


def poner_controlador(pos_x, pos_y, superficie):
    boton = pygame.Rect(pos_x, pos_y, 50, 20)
    clickeable = pygame.draw.rect(superficie, color_azul, boton, 0, 10)
    return clickeable


def poner_botones(espaciado):
    x = 50
    distancia = 50

    aux = poner_boton(x, espaciado, pantalla)
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

    paso = poner_boton(x + 185, espaciado - 100, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "paso", False, color_fondo)),
                  [x + 170 + menos_memoria.width / 2, espaciado - 95])


    aux = poner_boton(x, espaciado, pantalla)
    pantalla.blit((pygame.font.Font.render(fuente, "KERNEL       : " + str(kernel), False, color_fondo)),
                  [x + aux.width / 8, espaciado + aux.height / 4])

    espaciado += distancia
    aux = poner_textbox(x - x / 2, espaciado * 1.05, pantalla)

    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 12)
    if type(texto_codigo) == str:
        pantalla.blit((pygame.font.Font.render(fuente_aux, texto_codigo, False, color_fondo)),
                      [aux.left + 5, aux.top + 5])
    else:
        mostrar_texto(texto_codigo, aux.left, aux.top)

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
        mostrar_texto(texto_variables, variables_textbox.left + 5, variables_textbox.top + 23)

    pantalla.blit((pygame.font.Font.render(fuente, "ACUMULADOR   : " + str(acumulador[1]), False, color_amarillo)),
                  [variables_textbox.left + 5, variables_textbox.bottom + 5])

    if type(texto_etiquetas) == str:
        pantalla.blit((pygame.font.Font.render(fuente_aux, texto_etiquetas, False, color_fondo)),
                      [etiquetas_textbox.left + etiquetas_textbox.width / 5, etiquetas_textbox.centery])
    else:
        mostrar_texto(texto_etiquetas, etiquetas_textbox.left + 5, etiquetas_textbox.top + 23)

    return [btn_cargar, mas_memoria, menos_memoria, mas_kernel, menos_kernel]


#   filedialog
def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def validar_sintaxis(linea):
    linea = linea.strip()
    linea = linea.replace("       ", " ")
    linea = linea.replace("      ", " ")
    linea = linea.replace("     ", " ")
    linea = linea.replace("    ", " ")
    linea = linea.replace("   ", " ")
    linea = linea.replace("  ", " ")
    linea = linea.replace(" ", " ")
    linea = linea = linea.split(" ")

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


def mostrar_texto(texto, left, top):
    fuente_aux = pygame.font.Font("fonts/Roboto-Regular.ttf", 12)
    espaciado = 5
    for t in texto:
        pantalla.blit((pygame.font.Font.render(fuente_aux, t, False, color_fondo)),
                      [left + 5, top + espaciado])
        espaciado += 15


def manejo_archivo(ruta):
    archivo = open(ruta, 'r')
    instrucciones = archivo.read().splitlines()
    aux = ""
    paso = True

    for i in instrucciones:
        if i != "":
            if validar_sintaxis(i):
                aux += i + "\n"
            else:
                print("Error en sintaxix, linea ", instrucciones.index(i), i)
                paso = False
                break
    return paso, aux


f = "<No File Selected>"


def ejecucion(programa, acumulador, variables, etiquetas, texto_pc):
    acumulador_1 = acumulador
    variables_aux = variables
    etiquetas_aux = etiquetas
    texto_pc_aux = texto_pc
    texto_impresora_aux = "texto ejemplo impresora"

    for instruccion in programa:
        print(">> ", programa.index(instruccion), " - ", instruccion)
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
                aux = programa[etiquetas_aux[linea[1]]:]
                variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux = ejecucion(aux,
                                                                                                          acumulador_1,
                                                                                                          variables_aux,
                                                                                                          etiquetas_aux,
                                                                                                          texto_pc_aux)
            elif acumulador_1[1] < 0:
                aux = programa[etiquetas_aux[linea[2]]:]
                variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux = ejecucion(aux,
                                                                                                          acumulador_1,
                                                                                                          variables_aux,
                                                                                                          etiquetas_aux,
                                                                                                          texto_pc_aux)
            else:
                pass
        elif linea[0] == "etiqueta":
            # etiqueta estructura:{'nombre':posicion}
            etiquetas_aux[linea[1]] = int(linea[2])

        elif linea[0] == "retorne":
            return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux

    return variables_aux, acumulador_1, etiquetas_aux, texto_pc_aux, texto_impresora_aux


def quitarSaltoDeLinea(programa):
    # ingresa string
    print(programa)


def ejecutar_programa(programa):
    acumulador = ['I', 0]
    variables = {}
    etiquetas = {}
    texto_pc = "texto ejemplo pc"
    texto_impresora = "texto ejemplo impresora"
    pos = []
    """
    acumulador estructura:['I', '5'] <class 'list'>
    """
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
            """
            Estructura diccionario :
            "nombre_variable": ["tipo","valor"]
            """
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
                                                                                    etiquetas, texto_pc)
        elif linea[0] == "vayasi":
            if acumulador[1] > 0:
                aux = programa[etiquetas[linea[1]]:]
                variables, acumulador, etiquetas, texto_pc, texto_impresora = ejecucion(aux, acumulador, variables,
                                                                                        etiquetas, texto_pc)
            elif acumulador[1] < 0:
                aux = programa[etiquetas[linea[2]]:]
                variables, acumulador, etiquetas, texto_pc, texto_impresora = ejecucion(aux, acumulador, variables,
                                                                                        etiquetas, texto_pc)
            else:
                pass

        elif linea[0] == "etiqueta":
            """
            etiqueta estructura:{'nombre':posicion}
            """
            etiquetas[linea[1]] = int(linea[2])
            # print(etiquetas)

        elif linea[0] == "retorne":
            programas.append(programa)
            memoria_principal[0] = "Acumulador :" + str(acumulador[1])
            for k in range(kernel):
                memoria_principal[k + 1] = ("J" + str(k) + " Kernel")
            contador = 0
            for prog in programas:
                for ins in range(len(prog)):
                    memoria_principal[contador + kernel] = [("J" + str(contador + kernel)), prog[ins]]
                    contador += 1

            return variables, acumulador, etiquetas, texto_pc, texto_impresora

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


def mostrarError(texto):
    print(texto)
    # dimensiones :  30 203 183 673
    cuadro_error = pygame.draw.rect(pantalla, color_rojo, pygame.Rect(30, lado_derecho_surface.get_rect().bottom - 50,
                                                                      lado_derecho_surface.get_rect().width * 1.65, 55),
                                    0, 15)
    pantalla.blit((pygame.font.Font.render(fuente, str(texto), False, color_amarillo)),
                  [cuadro_error.left + 5, cuadro_error.top + 15])


def mostrar_memoria():
    espaciado = 5
    # con el height actual muestra 32
    # cuanto height se necesita para mostrar memoria principal total
    # lado_derecho_surface.get_rect().height --> 32
    # ? --> len(memoria_principal)
    aux = (len(memoria_principal) * lado_derecho_surface.get_rect().height) / 32
    memoria_surface = pygame.Surface((lado_izquierdo.width - 30, aux))
    memoria_surface.fill(color_azul_oscuro)
    fuente = pygame.font.Font("fonts/Roboto-Regular.ttf", 16)

    for instrucccion in memoria_principal:
        if type(instrucccion) is list:
            memoria_surface.blit(
                (pygame.font.Font.render(fuente, str(instrucccion[0] + " " + instrucccion[1]), False, color_amarillo)),
                [memoria_surface.get_rect().left + 2, memoria_surface.get_rect().top + espaciado])
        else:
            memoria_surface.blit((pygame.font.Font.render(fuente, str(instrucccion), False, color_amarillo)),
                                 [memoria_surface.get_rect().left + 2, memoria_surface.get_rect().top + espaciado])
        espaciado += 20
    lado_derecho_surface.blit(memoria_surface, (0, scrollbar.y_axis))


while True:
    resultado = None
    for event in pygame.event.get():
        pantalla.fill(color_fondo)
        pygame.draw.rect(pantalla, color_azul,
                         pygame.Rect(10, 10, (ancho / 5), lado_derecho_surface.get_rect().height + 23), 12, 15)
        lado_izquierdo = pygame.draw.rect(pantalla, color_menu_izquierdo,
                                          pygame.Rect(12, 12, (ancho / 5) - 3,
                                                      lado_derecho_surface.get_rect().height + 23), 0, 15)


        poner_botones(20)
        pc = pantalla.blit(pc_img, (pantalla.get_rect().width / 2 - 120, pantalla.get_rect().top + 5))
        pantalla.blit((pygame.font.Font.render(fuente, "texto ejemplo pc", False, color_amarillo)),
                      [pc.centerx, pc.top + 5])

        impresora = pantalla.blit(impresora_img, (pantalla.get_rect().width / 2 - 120, pc.bottom + 5))
        pantalla.blit((pygame.font.Font.render(fuente, str(texto_impresora), False, color_fondo)),
                      [impresora.centerx - 90, impresora.top + 10])

        pygame.draw.rect(pantalla, color_azul,
                         pygame.Rect(pc.right + 80, pantalla.get_rect().top + 5, (ancho / 5),
                                     lado_derecho_surface.get_rect().height + 26), 12, 15)

        pc = pantalla.blit(pc_img, (pantalla.get_rect().width / 2 - 120, pantalla.get_rect().top + 5))

        pantalla.blit((pygame.font.Font.render(fuente, str(texto_pc), False, color_fondo)),
                      [pc.centerx - pc.centerx / 4.5, pc.centery - pc.centery / 1.5])

        lado_derecho = pygame.draw.rect(pantalla, color_menu_izquierdo,
                                        pygame.Rect(pc.right + 82, pantalla.get_rect().top + 7, (ancho / 5) - 4,
                                                    lado_derecho_surface.get_rect().height + 26), 0, 15)

        boton = pygame.Rect(313, 70, 80, 80)
        play = pygame.draw.rect(pantalla, color_azul, boton, 0, 10)
        pantalla.blit(play_img, [play.left + 10, play.top + 10])

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Boton cargue
            if poner_botones(20)[0].collidepoint(pygame.mouse.get_pos()):
                if memoria == 0 or kernel == 0:
                    mostrarError("Establezca valores para memoria y kernel")
                else:
                    if (memoria + kernel) <= 5100:
                        f = prompt_file()
                        programa = manejo_archivo(f)
                        if programa[0]:
                            pantalla.fill(color_azul)
                            texto_codigo = programa[1].split("\n")
                            if play_img.get_rect().collidepoint(pygame.mouse.get_pos()):
                                print("play")
                                resultado = ejecutar_programa(texto_codigo)
                            if resultado:
                                texto_variables = mostrar_variables(resultado[0])
                                texto_etiquetas = mostrar_etiquetas(resultado[2])
                                texto_pc = resultado[3]
                                texto_impresora = resultado[4]
                                acumulador = resultado[1]

                    else:
                        mostrarError("Memoria principal con longitud superior")

            # Acciones para botones de aumento y dism para var kernel y memoria
            elif poner_botones(20)[1].collidepoint(pygame.mouse.get_pos()):
                memoria += 10
            elif poner_botones(20)[2].collidepoint(pygame.mouse.get_pos()) and memoria > 0:
                memoria -= 10
            elif poner_botones(20)[3].collidepoint(pygame.mouse.get_pos()):
                kernel += 10
            elif poner_botones(20)[4].collidepoint(pygame.mouse.get_pos()) and kernel > 0:
                kernel -= 10
                # [btn_cargar, mas_memoria, menos_memoria, mas_kernel, menos_kernel]

        scrollbar.event_handler(event)

    lado_derecho_surface.fill((255, 255, 255))
    # lado_derecho_surface.blit(image, (0, scrollbar.y_axis))
    lado_derecho_surface.fill(color_amarillo)
    scrollbar.draw(lado_derecho_surface)
    mostrar_memoria()
    pantalla.blit(lado_derecho_surface, (872 + padding, 7 + padding))
    scrollbar.update()
    pygame.display.flip()
    clock.tick(30)
