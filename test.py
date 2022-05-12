import tkinter
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
root.mainloop()
