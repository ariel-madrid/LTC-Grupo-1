#Se importan librerias 
import tkinter
from tkinter import ttk
from tkinter import messagebox
from pyswip import *
from playsound import playsound
import multiprocessing

prolog = Prolog()
prolog.consult("../base_conocimiento.pl")
p = multiprocessing.Process(target=playsound, args=("mario.mp3",))

def capturarInformacion(combo,combo2,radioValue,combo3):
    juegos = []
    categorias = []
    speedrun = []
    preferenciaTiempo = combo.get()
    preferenciaDecada = combo2.get()
    preferenciaNivelHabilidad = radioValue.get()
    preferenciaCategoria = combo3.get()

    tmp = 0

    #Dependiendo de las entradas a traves de la interfaz, se realizan diferentes consultas a la base de conocimientos.
    if (preferenciaNivelHabilidad == ""):
        tkinter.messagebox.showinfo(message="Debe seleccionar un nivel de habilidad", title="Alerta")
        tmp = 1
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
    elif (preferenciaDecada == "2010-2019"):
        preferenciaDecada = "10"
    else:
        preferenciaDecada = "Seleccione"

    if (preferenciaNivelHabilidad == "Novato"):
        preferenciaNivelHabilidad = "ANY%"
    elif (preferenciaNivelHabilidad == "Experto"):
        preferenciaNivelHabilidad = "100%"
    else:
        preferenciaNivelHabilidad = ""

    if (preferenciaCategoria == "Accion"):
        preferenciaCategoria = "Accion"
    elif (preferenciaCategoria == "Aventura"):
        preferenciaCategoria = "Aventura"
    elif (preferenciaCategoria == "Plataforma"):
        preferenciaCategoria = "Plataforma"
    elif (preferenciaCategoria == "Deporte"):
        preferenciaCategoria = "Deporte"
    elif (preferenciaCategoria == "Coches"):
        preferenciaCategoria = "Coches"
    elif (preferenciaCategoria == "Terror"):
        preferenciaCategoria = "Terror"
    else:
        preferenciaCategoria = "Seleccione"

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
    combo2 = ttk.Combobox(state="readonly",values=["1990-1999","2000-2009","2010-2019","No es relevante"])
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

if __name__ == "__main__":
    root()
