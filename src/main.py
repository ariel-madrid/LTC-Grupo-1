#Se importan librerias 
import tkinter
from tkinter import ttk
from tkinter import messagebox
from pyswip import *
from playsound import playsound
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control
from random import randint 
from random import seed 

seed(1)

prolog = Prolog()
prolog.consult("base_conocimiento.pl")
p = multiprocessing.Process(target=playsound, args=("mario.mp3",))

def capturarInformacion(combo,combo2,radioValue):
    juegos = []
    categorias = []
    speedrun = []
    preferenciaTiempo = combo.get()
    preferenciaDecada = int(combo2.get())
    preferenciaNivelHabilidad = radioValue.get()
    #preferenciaCategoria = combo3.get()
    
    num_exp = 0
    num_time = 0
    num_dec = 0
    tmp = 0

    #Dependiendo de las entradas a traves de la interfaz, se realizan diferentes consultas a la base de conocimientos.
    if (preferenciaNivelHabilidad == ""):
        tkinter.messagebox.showinfo(message="Debe seleccionar un nivel de habilidad", title="Alerta")
        tmp = 1
    if (preferenciaTiempo == "Menos de 30 minutos"):
        preferenciaTiempo = "Corta" #Poner valor numerico
        num_time = 14.5

    elif (preferenciaTiempo == "Entre 30 y 90 minutos"):
        preferenciaTiempo = "Media"
        num_time = 40

    elif (preferenciaTiempo == "Más de 90 minutos"):
        preferenciaTiempo = "Larga"
        num_time = 100

    else:
        preferenciaTiempo = "Seleccione"
        num_time = 0

    if (preferenciaDecada >= 1990 and preferenciaDecada < 2000):
        num_dec = preferenciaDecada
        preferenciaDecada = "90" #Poner valor numerico

    elif (preferenciaDecada >= 2000 and preferenciaDecada < 2010):
        num_dec = preferenciaDecada
        preferenciaDecada = "2000"
        
    elif (preferenciaDecada >= 2010 and preferenciaDecada < 2020):
        num_dec = preferenciaDecada
        preferenciaDecada = "10"
        
    else:
        preferenciaDecada = "Seleccione"
        num_dec = randint(1990,2019)

    if (preferenciaNivelHabilidad == "Novato"):
        preferenciaNivelHabilidad = "ANY%" #Poner valor numerico
        num_exp = 2.5

    elif (preferenciaNivelHabilidad == "Experto"):
        preferenciaNivelHabilidad = "100%"
        num_exp = 7.5

    else:
        preferenciaNivelHabilidad = ""
        num_exp = 0

    preferenciaCategoria = escogerCategoria(num_exp, num_time, num_dec)
    
    if (preferenciaCategoria == "Accion"):
        preferenciaCategoria = "Accion"
    elif (preferenciaCategoria == "Aventura"):
        preferenciaCategoria = "Aventura"
    elif (preferenciaCategoria == "Plataforma"):
        preferenciaCategoria = "Plataforma"
    elif (preferenciaCategoria == "Coches"):
        preferenciaCategoria = "Coches"
    elif (preferenciaCategoria == "Terror"):
        preferenciaCategoria = "Terror"
    else:
        preferenciaCategoria = "Seleccione"

    
    ''''''
    '''
    POSIBLES COMBINACIONES DE ENTRADAS PARA LAS CONSULTAS DE PROLOG
    juego(X,a,b,c,_) - 1
    juego(x,a,_,c,d) - 2
    juego(x,_,b,c,d) - 3
    juego(x,a,_,c,_) - 4
    juego(x,_,b,c,_) - 5
    juego(x,_,_,c,d) - 6
    juego(x,_,_,c,_) - 7
    juego(X,a,b,c,d) - 8
    '''
    
    a = preferenciaCategoria
    b = preferenciaDecada
    c = preferenciaNivelHabilidad
    d = preferenciaTiempo

    #1
    if (preferenciaCategoria != "Seleccione" and preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo == "Seleccione"):

        for consulta in prolog.query("juego("+"X," + "'"+a+"'" + "," + '"'+b+'"' + "," + '"'+c+'"'+ "," + "_" +")"):
            juegos.append(consulta["X"])
            categorias.append(a)
            speedrun.append(c)
    #2
    elif (preferenciaCategoria != "Seleccione" and preferenciaDecada == "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo != "Seleccione"):

        for consulta in prolog.query("juego("+"X," + "'"+a+"'" + "," + "_" + "," + '"'+c+'"' + "," + '"'+d+'"' +")"):
            juegos.append(consulta["X"])
            categorias.append(a)
            speedrun.append(c)
    #3
    elif (preferenciaCategoria == "Seleccione" and preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo != "Seleccione"):

        for consulta in prolog.query("juego("+"X," + 'Y' + "," + '"'+b+'"' + "," + '"'+c+'"' + "," + '"'+d+'"' +")"):
            juegos.append(consulta["X"])
            categorias.append(consulta["Y"])
            speedrun.append(c)
    #4
    elif (preferenciaCategoria != "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo == "Seleccione" and preferenciaDecada == "Seleccione"):
        for consulta in prolog.query("juego("+"X," +"'"+a+"'"  + "," + "_" + "," + '"'+c+'"' + "," + "_" +")"):
            juegos.append(consulta["X"])
            categorias.append(a)
            speedrun.append(c)

    #5
    elif (preferenciaCategoria == "Seleccione" and preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo == "Seleccione"):

        for consulta in prolog.query("juego("+"X," + 'Y' + "," + '"'+b+'"' + "," + '"'+c+'"' + "," + "_" +")"):
            juegos.append(consulta["X"])
            categorias.append(consulta["Y"])
            speedrun.append(c)

    #6
    elif (preferenciaCategoria == "Seleccione" and preferenciaDecada == "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo != "Seleccione"):

        for consulta in prolog.query("juego("+"X," + 'Y' + "," + "_" + "," + '"'+c+'"' + "," + '"'+d+'"' +")"):
            juegos.append(consulta["X"])
            categorias.append(consulta["Y"])
            speedrun.append(c)
    #7
    elif (preferenciaCategoria == "Seleccione" and preferenciaDecada == "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo == "Seleccione"):

        for consulta in prolog.query("juego("+"X," + 'Y' + "," + "_" + "," + '"'+c+'"' + "," + "_" +")"):
            juegos.append(consulta["X"])
            categorias.append(consulta["Y"])
            speedrun.append(c)

    #8
    elif (preferenciaCategoria != "Seleccione" and preferenciaDecada != "Seleccione" and preferenciaNivelHabilidad != "Seleccione" and preferenciaTiempo != "Seleccione"):

        for consulta in prolog.query("juego("+"X," + "'"+a+"'" + "," + '"'+b+'"' + "," + '"'+c+'"' + "," + '"'+d+'"' +")"):
            juegos.append(consulta["X"])
            categorias.append(a)
            speedrun.append(c)

    #Si no se encuentran juegos para las preferencias
    if (len(juegos) < 1 and tmp!=1):
        juegos = []
        # En caso que se seleccion Categoria y Habilidad
        if (preferenciaCategoria != "Seleccione" and preferenciaNivelHabilidad != ""):
            for consulta in prolog.query("juego("+"X," +"'"+a+"'"  + "," + "_" + "," + '"'+c+'"' + "," + "_" +")"):
                juegos.append(consulta["X"])
                categorias.append(a)
                speedrun.append(c)

            tkinter.messagebox.showinfo(
                message="No se encontraron juegos para sus preferencias.\nSe recomiendan los siguientes para las preferencias: \n\n- "
                        + preferenciaNivelHabilidad + "\n\n- " + preferenciaCategoria,
                title="Alerta")
        # En caso que solo se seleccione Habilidad
        elif (preferenciaNivelHabilidad != ""):

            for consulta in prolog.query("juego("+"X," + 'Y' + "," + "_" + "," + '"'+c+'"' + "," + "_" +")"):
                juegos.append(consulta["X"])
                categorias.append(consulta["Y"])
                speedrun.append(preferenciaNivelHabilidad)
            tkinter.messagebox.showinfo(message="No se encontraron juegos para sus preferencias.\n\nSe recomiendan los siguientes para las preferencias: \n\n- "+preferenciaNivelHabilidad, title="Recomendaciones")
    if (len(juegos) > 3):
        juegos = juegos[0:3]
        categorias = categorias[0:3]
        speedrun = speedrun[0:3]
    if (tmp != 1):
        p.terminate()
        tkinter.messagebox.showinfo(message="Los siguientes juegos le van a gustar",title="Recomendaciones")
        # Ventana que muestra los juegos.}
        recomendaciones = tkinter.Tk()
        recomendaciones.geometry("800x250")
        recomendaciones.resizable(0, 0)
        recomendaciones.title("Recomendacion de Videojuegos")

        mensaje = tkinter.Label(recomendaciones, text="Los siguientes juegos le van a gustar", bg="#88cffa")
        mensaje.place(x=200, y=10)

        columnas = ("Juego", "Categoria", "Modo SpeedRun")
        treeview = ttk.Treeview(recomendaciones, height=10, show="headings", columns=columnas)

        treeview.column("Juego", width=300, anchor='center')
        treeview.column("Categoria", width=100, anchor='center')
        treeview.column("Modo SpeedRun", width=100, anchor='center')

        treeview.heading("Juego", text="Juego")
        treeview.heading("Categoria", text="Categoria")
        treeview.heading("Modo SpeedRun", text="Modo SpeedRun")

        for i in range(len(juegos)):
            treeview.insert('', i, values=(juegos[i], categorias[i], speedrun[i]))

        treeview.pack()

def stopMusic():
    p.terminate()

def ingresoSistema(inputNombre,ventana):
    nombre = str(inputNombre.get())

    if (nombre == ""):
        tkinter.messagebox.showinfo(message="Debe ingresar un nombre", title="Alerta")
        return
    p.start()
    ventana.destroy()

    selecciones =  tkinter.Tk()
    selecciones.geometry("600x450")
    selecciones.resizable(0, 0)
    selecciones.title("Seleccion de preferencias")

    #Cargar imagen para el fondo
    space = tkinter.PhotoImage( file = "./img/fondo4.png")
    #small_img=space.subsample(1,1)
    background = tkinter.Label(selecciones, image=space)
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
    combo2 = ttk.Combobox(state="readonly",
        values=["1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",
                "2000","2001","2002","2003","2004","2005","2006","2007","2008","2009",
                "2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","No es relevante"])
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

    enviar = tkinter.Button(selecciones,text="Consultar",command=lambda: capturarInformacion(combo,combo2,radioValue))
    enviar.place(x=510, y=340)

    apagar = tkinter.Button(selecciones, text="Apagar Música",command=lambda: stopMusic())
    apagar.place(x=50, y=340)

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

def escogerCategoria(exp_value, time_value, dec_value):
    x_experiencia = np.arange(0,12,1)
    x_tiempo = np.arange(0,120,1)
    x_decada = np.arange(1990,2023,1)

    x_categoria = np.arange(1,34,1)

    experiencia = control.Antecedent(x_experiencia,"Experiencia")
    tiempo = control.Antecedent(x_tiempo,"Tiempo")
    decada = control.Antecedent(x_decada,"Decada")
    categoria = control.Consequent(x_categoria,"Categoria",'centroid')

    # Funciones de membresia
    experiencia["Novato"] = fuzz.trimf(x_experiencia, [0, 0, 5])
    experiencia["Experto"] = fuzz.trimf(x_experiencia, [5, 10, 10])

    tiempo["Poco"] = fuzz.zmf(x_tiempo, 0, 29)
    tiempo["Medio"] = fuzz.pimf(x_tiempo, 20, 35, 45, 60)
    tiempo["Mucho"] = fuzz.smf(x_tiempo, 60, 120)

    decada["Noventas"] = fuzz.trimf(x_decada, [1990,1995,2000])
    decada["Dosmil"] = fuzz.trimf(x_decada, [2000,2005,2010])
    decada["Dosmildiez"] = fuzz.trimf(x_decada, [2010,2015,2019])

    categoria["Accion"] = fuzz.zmf(x_categoria, 0,7)
    categoria["Plataforma"] = fuzz.pimf(x_categoria, 6,8,12,14)
    categoria["Coches"] = fuzz.trimf(x_categoria, [14,18,21])
    categoria["Aventura"] = fuzz.smf(x_categoria, 21,28)
    categoria["Terror"] = fuzz.trimf(x_categoria, [29,33,33])

    regla1 = control.Rule(tiempo["Poco"] & experiencia["Experto"] & decada["Noventas"], categoria["Terror"])
    regla2 = control.Rule(tiempo["Mucho"] & experiencia["Novato"], categoria["Plataforma"])
    regla3 = control.Rule(tiempo["Medio"] & experiencia["Experto"] & decada["Dosmildiez"], categoria["Coches"])
    regla4 = control.Rule(tiempo["Mucho"] & experiencia["Novato"], categoria["Aventura"])
    regla5 = control.Rule((tiempo["Poco"] | experiencia["Novato"]) & decada["Noventas"], categoria["Plataforma"])
    regla6 = control.Rule(tiempo["Poco"] & experiencia["Experto"] & decada["Dosmil"], categoria["Plataforma"])
    regla7 = control.Rule(tiempo["Mucho"] | experiencia["Experto"], categoria["Accion"])
    regla8 = control.Rule(tiempo["Poco"] & experiencia["Novato"], categoria["Plataforma"])

    categoriaCtrl = control.ControlSystem([regla1,regla2,regla3,regla4,regla5,regla6,regla7,regla8])
    categoriaSim = control.ControlSystemSimulation(categoriaCtrl)

    #Inputs
    categoriaSim.input['Experiencia'] = exp_value
    categoriaSim.input['Tiempo'] = time_value
    categoriaSim.input['Decada'] = dec_value
    categoriaSim.compute()
    cat_value = categoriaSim.output['Categoria']

    print(cat_value)

    experiencia.view()
    tiempo.view()
    decada.view()
    categoria.view()

    categoria.view(sim=categoriaSim)

    if(cat_value >= 0.0 and cat_value <= 6.5):
        categoria = "Accion"
    elif(cat_value > 6.5 and cat_value <= 14.0):
        categoria = "Plataforma" 
    elif(cat_value > 14.0 and cat_value <= 21.0):
        categoria = "Coches"
    elif(cat_value > 21.0 and cat_value <= 28.5):
        categoria = "Aventura"
    elif(cat_value > 28.5 and cat_value < 33):
        categoria = "Terror"
        
    return categoria

if __name__ == "__main__":
    root()



