#Se importan librerias 
import tkinter
from tkinter import ttk
from tkinter import messagebox
from pyswip import *

prolog = Prolog()
prolog.consult("../base_conocimiento.pl")

def capturarInformacion(combo,combo2,radioValue,combo3):
    juegos = []

    preferenciaTiempo = combo.get()
    preferenciaDecada = combo2.get()
    preferenciaNivelHabilidad = radioValue.get()
    preferenciaCategoria = combo3.get()

    #Dependiendo de las entradas a traves de la interfaz, se realizan diferentes consultas a la base de conocimientos.
    if (preferenciaNivelHabilidad == ""):
        tkinter.messagebox.showinfo(message="Debe seleccionar un nivel de habilidad", title="Alerta")
    if (preferenciaTiempo == "Menos de 30 minutos"):
            preferenciaTiempo = "Corta"
    elif (preferenciaTiempo == "Entre 30 y 90 minutos"):
        preferenciaTiempo = "Media"
    elif (preferenciaTiempo == "Más de 90 minutos"):
        preferenciaTiempo = "Larga"
    else:
        preferenciaTiempo = "Seleccione"

    if (preferenciaDecada == "1990-1999"):
        preferenciaDecada = "90"
    elif (preferenciaDecada == "2000-2009"):
        preferenciaDecada = "2000"
    elif (preferenciaDecada == "2010-2029"):
        preferenciaDecada = "10"
    else:
        preferenciaDecada = "Seleccione"

    if (preferenciaNivelHabilidad == "Novato"):
        preferenciaNivelHabilidad = "any"
    elif (preferenciaNivelHabilidad == "Experto"):
        preferenciaNivelHabilidad = "100"
    else:
        preferenciaNivelHabilidad = ""

    if (preferenciaCategoria == "Accion"):
        preferenciaCategoria = "accion"
    elif (preferenciaCategoria == "Aventura"):
        preferenciaCategoria = "aventura"
    elif (preferenciaCategoria == "Plataforma"):
        preferenciaCategoria = "plataforma"
    elif (preferenciaCategoria == "Deporte"):
        preferenciaCategoria = "deporte"
    elif (preferenciaCategoria == "Coches"):
        preferenciaCategoria = "coches"
    elif (preferenciaCategoria == "Terror"):
        preferenciaCategoria = "terror"
    else:
        preferenciaCategoria = "Seleccione"
        
    #En caso de que sean seleccionados todos los campos
    if (preferenciaTiempo != "Seleccione" and preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaCategoria != "Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoCDHT(" + '"'+preferenciaCategoria+'"' + "," + '"'+preferenciaDecada+'"' + "," '"'+preferenciaNivelHabilidad+'"' +","+'"'+preferenciaTiempo+'"' + ",X)"):
            juegos.append(consulta["X"])
    #En caso de que se seleccione Categoria, Decada y Habilidad
    elif (preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaCategoria != "Seleccione" and preferenciaTiempo=="Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoCDH(" + '"'+preferenciaCategoria+'"' + "," + '"'+preferenciaDecada+'"' + "," '"'+preferenciaNivelHabilidad+'"' +",X)"):
            juegos.append(consulta["X"])
    #En caso de que ingrese Decada, Habilidad, Tiempo.
    elif (preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaTiempo != "Seleccione" and preferenciaCategoria == "Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoDHT(" +'"'+preferenciaDecada+'"'+","+'"'+preferenciaNivelHabilidad+'"' +","+'"'+preferenciaTiempo+'"'+",X)"):
            juegos.append(consulta["X"])
    #En caso de que ingrese Categoria, Habilidad, Tiempo
    elif (preferenciaCategoria != "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaTiempo != "Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoCHT(" +'"'+preferenciaCategoria+'"'+","+'"'+preferenciaNivelHabilidad+'"' +","+'"'+preferenciaTiempo+'"'+",X)"):
            juegos.append(consulta["X"])
    #En caso que se seleccion Categoria y Habilidad
    elif (preferenciaCategoria != "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaDecada == "Seleccione" and preferenciaTiempo == "Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoCH(" + '"'+preferenciaCategoria+'"' + "," + '"'+preferenciaNivelHabilidad+'"' +",X)"):
            juegos.append(consulta["X"])
    #En caso de que ingrese Decada, Habilidad.
    elif (preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaTiempo == "Seleccione" and preferenciaCategoria == "Seleccione"):
    
        for consulta in prolog.query("seleccionarJuegoDH(" +'"'+preferenciaDecada+'"'+","+'"'+preferenciaNivelHabilidad+'"' +",X)"):
            juegos.append(consulta["X"])
    #En caso de que ingrese Habilidad, Tiempo.
    elif (preferenciaDecada == "Seleccione" and preferenciaNivelHabilidad != "" and preferenciaTiempo != "Seleccione" and preferenciaCategoria == "Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoHT(" +'"'+preferenciaNivelHabilidad+'"'+","+'"'+preferenciaTiempo+'"' +",X)"):
            juegos.append(consulta["X"])
    #En caso que solo se seleccione Habilidad
    elif (preferenciaNivelHabilidad != "" and preferenciaCategoria == "Seleccione" and preferenciaDecada == "Seleccione" and preferenciaTiempo == "Seleccione"):
        
        for consulta in prolog.query("seleccionarJuegoH(" +'"'+preferenciaNivelHabilidad+'"' +",X)"):
            juegos.append(consulta["X"])

    if(len(juegos) == 0):
        #En caso que se seleccion Categoria y Habilidad
        if (preferenciaCategoria != "Seleccione" and preferenciaNivelHabilidad != ""):
            
            for consulta in prolog.query("seleccionarJuegoCH(" + '"'+preferenciaCategoria+'"' + "," + '"'+preferenciaNivelHabilidad+'"' +",X)"):
                juegos.append(consulta["X"])
        #En caso que solo se seleccione Habilidad
        elif (preferenciaNivelHabilidad != ""):
            
            for consulta in prolog.query("seleccionarJuegoH(" +'"'+preferenciaNivelHabilidad+'"' +",X)"):
                juegos.append(consulta["X"])
        mensaje = juegos
    else:
        mensaje = juegos

    tkinter.messagebox.showinfo(message=mensaje, title="Resultados")

def ingresoSistema(inputNombre,ventana):
    nombre = str(inputNombre.get())
    ventana.destroy()

    selecciones =  tkinter.Tk()
    selecciones.geometry("600x450")
    selecciones.resizable(0, 0)
    selecciones.title("Seleccion de preferencias")

    #Cargar imagen para el fondo
    space = tkinter.PhotoImage( file = "./img/space.png")
    small_img=space.subsample(1,1)
    background = tkinter.Label(selecciones, image=small_img)
    background.space = space 
    background.place(x=0,y=0)

    mensaje = tkinter.Label(selecciones,text="Bienvenido "+nombre,bg = "#88cffa")
    mensaje.place(x=270, y=20)

    tiempo = tkinter.Label(selecciones,text="¿Con cuanto tiempo cuenta para dedicar al videojuego?",bg = "#88cffa")
    tiempo.place(x=50, y=60)

    combo = ttk.Combobox()
    combo = ttk.Combobox(state="readonly",values=["Menos de 30 minutos","Entre 30 y 90 minutos","Más de 90 minutos","No es relevante"])
    combo.set("Seleccione")
    combo.place(x=50, y=85)

    decada = tkinter.Label(selecciones,text="¿Es de su preferencia alguna decada en especifico?",bg = "#88cffa")
    decada.place(x=50, y=120)

    combo2 = ttk.Combobox()
    combo2 = ttk.Combobox(state="readonly",values=["1990-1999","2000-2009","2010-2029","No es relevante"])
    combo2.set("Seleccione")
    combo2.place(x=50, y=145)

    decada = tkinter.Label(selecciones,text="¿Que tan habil se considera?",bg = "#88cffa")
    decada.place(x=50, y=180)

    radioValue = tkinter.StringVar()

    rdioNovato = tkinter.Radiobutton(selecciones, text='Novato',
                             variable=radioValue, value='Novato')
    rdioExperto = tkinter.Radiobutton(selecciones, text='Experto',
                             variable=radioValue, value='Experto')
    
    rdioNovato.place(x=50, y=210)
    rdioExperto.place(x=150, y=210)

    categoria = tkinter.Label(selecciones,text="¿Es de su preferencia alguna categoria en especifico?",bg = "#88cffa")
    categoria.place(x=50, y=240)

    combo3 = ttk.Combobox()
    combo3 = ttk.Combobox(state="readonly",values=["Accion","Aventura","Plataforma","Deporte","Coches","Terror","No es relevante"])
    combo3.set("Seleccione")
    combo3.place(x=50, y=265)

    enviar = tkinter.Button(selecciones,text="Consultar",command=lambda: capturarInformacion(combo,combo2,radioValue,combo3))
    enviar.place(x=510, y=340)

def root():
    
    #Crear ventana
    ventana =  tkinter.Tk()
    ventana.geometry("600x330")
    ventana.resizable(0, 0)
    ventana.title("Bienvenido")
    #Cargar imagen para el fondo
    bg = tkinter.PhotoImage( file = "./img/mario.png")
    small_img=bg.subsample(1,1)
    background = tkinter.Label(ventana, image=small_img)
    background.bg = bg 
    background.place(x=0,y=0)

    #Mensaje de bienvenida
    bienvenida = tkinter.Label(ventana,text="Bienvenido/a al sistema de recomendacion de videojuegos",bg = "#88cffa")
    bienvenida.place(x=140,y=40)

    #Etiqueta 
    name = tkinter.Label(ventana,text="Ingrese su nombre: ",bg = "#88cffa")
    name.place(x=150,y = 150)

    #Input para el nombre
    inputNombre = tkinter.Entry(ventana)
    inputNombre.place(x=270,y = 150)

    #Boton para ingresar al sistema
    boton = tkinter.Button(ventana,text="Ingresar",command=lambda: ingresoSistema(inputNombre,ventana))
    boton.place(x=390,y = 205)

    #Se muestra la ventana
    ventana.mainloop()

if __name__ == "__main__":
    root()