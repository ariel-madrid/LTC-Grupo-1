import tkinter
from tkinter import ttk
nombre = ""

def capturarInformacion(combo,combo2,radioValue,combo3):
    preferenciaTiempo = combo.get()
    preferenciaDecada = combo2.get()
    preferenciaNivelHabilidad = radioValue.get()
    preferenciaCategoria = combo3.get()
    print(preferenciaTiempo)        
    print(preferenciaDecada)    
    print(preferenciaNivelHabilidad)
    print(preferenciaCategoria)
def ingresoSistema():
    nombre = str(inputNombre.get())
    ventana.destroy()

    selecciones =  tkinter.Tk()
    selecciones.geometry("600x400")
    selecciones.resizable(0, 0)
    selecciones.title("Seleccion de preferencias")

    selecciones.columnconfigure(0, weight=2)
    selecciones.columnconfigure(1, weight=4)
    selecciones.columnconfigure(2, weight=4)

    selecciones.rowconfigure(0, weight=2)
    selecciones.rowconfigure(1, weight=2)
    selecciones.rowconfigure(2, weight=2)

    mensaje = tkinter.Label(selecciones,text="Bienvenido "+nombre,bg = "#88cffa")
    mensaje.grid(column=0, row=0,sticky=tkinter.N)

    tiempo = tkinter.Label(selecciones,text="¿Con cuanto tiempo cuenta para dedicar al videojuego?",bg = "#88cffa")
    tiempo.place(x=50, y=50)

    combo = ttk.Combobox()
    combo = ttk.Combobox(state="readonly",values=["Menos de 30 minutos","Entre 30 y 90 minutos","Más de 90 minutos"])
    combo.set("Seleccione")
    combo.place(x=50, y=75)

    decada = tkinter.Label(selecciones,text="¿Es de su preferencia alguna decada en especifico?",bg = "#88cffa")
    decada.place(x=50, y=110)

    combo2 = ttk.Combobox()
    combo2 = ttk.Combobox(state="readonly",values=["1990-1999","2000-2009","2010-2029","No es relevante"])
    combo2.set("Seleccione")
    combo2.place(x=50, y=135)

    decada = tkinter.Label(selecciones,text="¿Que tan habil se considera?",bg = "#88cffa")
    decada.place(x=50, y=170)

    radioValue = tkinter.StringVar()

    rdioOne = tkinter.Radiobutton(selecciones, text='Novato',
                             variable=radioValue, value='Novato') 
    rdioTwo = tkinter.Radiobutton(selecciones, text='Experimentado',
                             variable=radioValue, value='Experimentado') 
    rdioThree = tkinter.Radiobutton(selecciones, text='Experto',
                             variable=radioValue, value='Experto')
    
    rdioOne.place(x=50, y=200)
    rdioTwo.place(x=130, y=200)
    rdioThree.place(x=250, y=200)

    categoria = tkinter.Label(selecciones,text="¿Es de su preferencia alguna categoria en especifico?",bg = "#88cffa")
    categoria.place(x=50, y=230)

    combo3 = ttk.Combobox()
    combo3 = ttk.Combobox(state="readonly",values=["Accion","Aventura","Plataforma","Deporte","Coches","Terror"])
    combo3.set("Seleccione")
    combo3.place(x=50, y=255)

    enviar = tkinter.Button(selecciones,text="Consultar",command=lambda: capturarInformacion(combo,combo2,radioValue,combo3))
    enviar.place(x=510, y=330)

#Crear ventana
ventana =  tkinter.Tk()
ventana.geometry("600x300")
ventana.resizable(0, 0)
ventana.title("Bienvenido")
#Cargar imagen para el fondo
bg = tkinter.PhotoImage( file = "./img/mario.png")

background = tkinter.Label(ventana, image = bg)
background.place(x = 0,y = 0)

#Configurar el grid
ventana.columnconfigure(0, weight=4)
ventana.columnconfigure(1, weight=8)
ventana.columnconfigure(2, weight=4)
ventana.rowconfigure(0, weight=4)
ventana.rowconfigure(1, weight=4)
ventana.rowconfigure(2, weight=4)

bienvenida = tkinter.Label(ventana,text="Bienvenido/a al sistema de recomendacion de videojuegos",bg = "#88cffa")
bienvenida.grid(column=1, row=0)

name = tkinter.Label(ventana,text="Ingrese su nombre: ",bg = "#88cffa")
name.grid(column=0, row=1,sticky=tkinter.W, padx=8, pady=8)

inputNombre = tkinter.Entry(ventana)
inputNombre.grid(column=1,row=1,padx=8, pady=8)

boton = tkinter.Button(ventana,text="Ingresar",command=lambda: ingresoSistema())
boton.grid(column=2,row=1,sticky=tkinter.E, padx=8, pady=8)

ventana.mainloop()

