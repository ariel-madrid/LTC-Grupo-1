""""
**Inferencia de Mamdani**
1.   Fuzzificacion de las variables de entrada.
2.   Evaluacion de las reglas.
3.   Agregacion de las salidas de las reglas.
4.   Defuzzificacion -> Utilizando centroide de area.
"""

#Se importan librerias 
import tkinter
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control
from random import randint
from random import seed

#Lista que contiene los juegos.
listaJuegos = []

class Juego:
    def __init__(self,nombre,genero,decada,dificultad,tiempo):
        self.nombre = nombre
        self.genero = genero
        self.decada = decada
        self.dificultad = dificultad
        self.tiempo = tiempo

def leerJuegos():
    juegos = open('./base_conocimiento.txt')
    for linea in juegos:
        informacion = linea.split(",")

        if (len(informacion)>1):
            informacion[4] = informacion[4].rstrip()
            listaJuegos.append(Juego(informacion[0],informacion[1],informacion[2],informacion[3],informacion[4]))
    juegos.close()

def obtenerCategoria(exp,time,dec,entradas):
    exp_value = exp
    time_value = time
    dec_value = dec
    #Dominios
    x_experiencia = np.arange(1,5,1)
    x_tiempo = np.arange(0,120,1)
    x_decada = np.arange(1990,2023,1)
    x_categoria = np.arange(0,33,1)

    # Funciones de pertenencia
    experiencia_novato = fuzz.trimf(x_experiencia, [1, 2, 3])
    experiencia_experto= fuzz.trimf(x_experiencia, [2, 3, 4])

    tiempo_poco = fuzz.zmf(x_tiempo, 0, 29)
    tiempo_medio = fuzz.pimf(x_tiempo, 20, 35, 45, 60)
    tiempo_mucho = fuzz.smf(x_tiempo, 55, 120)

    decada_noventas = fuzz.trimf(x_decada, [1990,1995,1999])
    decada_dosmil = fuzz.trimf(x_decada, [1999,2005,2009])
    decada_dosmildiez = fuzz.trimf(x_decada, [2009,2015,2019])

    categoria_accion = fuzz.zmf(x_categoria, 0,7)
    categoria_plataforma= fuzz.pimf(x_categoria, 6,8,12,14)
    categoria_coches = fuzz.trimf(x_categoria, [14,18,21])
    categoria_aventura = fuzz.smf(x_categoria, 21,28)
    categoria_terror = fuzz.trimf(x_categoria, [29,32,32])


    #Graficar funciones de pertenencia
    fig1,ax1 = plt.subplots(figsize=(6,5))

    ax1.plot(x_experiencia,experiencia_novato,'b',linewidth=1.5,label="Novato")
    ax1.plot(x_experiencia,experiencia_experto,'g',linewidth=1.5,label="Experto")
    ax1.set_title('Experiencia')
    ax1.legend()

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    ax2.plot(x_tiempo,tiempo_poco,'b',linewidth=1.5,label="Poco")
    ax2.plot(x_tiempo,tiempo_medio,'g',linewidth=1.5,label="Medio")
    ax2.plot(x_tiempo,tiempo_mucho,'r',linewidth=1.5,label="Mucho")
    ax2.set_title('Tiempo')
    ax2.legend()

    fig3, ax3 = plt.subplots(figsize=(6, 5))
    ax3.plot(x_decada,decada_noventas,'b',linewidth=1.5,label="90s")
    ax3.plot(x_decada,decada_dosmil,'g',linewidth=1.5,label="00s")
    ax3.plot(x_decada, decada_dosmildiez, 'r', linewidth=1.5, label="2010s")
    ax3.set_title('Decada')
    ax3.legend()

    fig4, ax4 = plt.subplots(figsize=(6, 5))
    ax4.plot(x_categoria, categoria_plataforma, 'b', linewidth=1.5, label="Plataforma")
    ax4.plot(x_categoria, categoria_terror, 'g', linewidth=1.5, label="Terror")
    ax4.plot(x_categoria, categoria_aventura, 'r', linewidth=1.5, label="Aventura")
    ax4.plot(x_categoria, categoria_accion, 'c', linewidth=1.5, label="Accion")
    ax4.plot(x_categoria, categoria_coches, 'm', linewidth=1.5, label="Coches")
    ax4.set_title('Categoria')
    ax4.legend()

    #Fuzzificar los valores de entrada

    exp_level_novato = fuzz.interp_membership(x_experiencia, experiencia_novato, exp_value)
    exp_level_experto = fuzz.interp_membership(x_experiencia, experiencia_experto, exp_value)

    tiempo_level_poco = fuzz.interp_membership(x_tiempo, tiempo_poco, time_value)
    tiempo_level_medio = fuzz.interp_membership(x_tiempo, tiempo_medio, time_value)
    tiempo_level_mucho = fuzz.interp_membership(x_tiempo, tiempo_mucho, time_value)

    decada_level_noventas = fuzz.interp_membership(x_decada, decada_noventas, dec_value)
    decada_level_dosmil = fuzz.interp_membership(x_decada, decada_dosmil, dec_value)
    decada_level_dosmildiez = fuzz.interp_membership(x_decada, decada_dosmildiez, dec_value)

    #Evaluacion de las reglas y Agregacion de las salidas de las reglas.

    # ---------------
    #Reglas con 3 entradas:
    if (entradas == 3):
        #Regla 1 -> tiempo["Poco"] & experiencia["Experto"] & decada["Noventas"], categoria["Terror"]
        active_rule1 = np.fmin(tiempo_level_poco, np.fmin(exp_level_experto,decada_level_noventas))
        categoria_activation_terror = np.fmin(active_rule1, categoria_terror)  # removed entirely to 0

        #Regla 2 -> tiempo["Mucho"] & decada["Dosmildiez"] & experiencia["Novato"] => Accion
        active_rule13 = np.fmin(tiempo_level_mucho,np.fmin(decada_level_dosmildiez,exp_level_novato))
        categoria_activation_accion3 = np.fmin(active_rule13,categoria_accion)

        #Regla 3 -> tiempo["Medio"] & experiencia["Experto"] & decada["Dosmildiez"], categoria["Coches"]
        active_rule3 = np.fmin(tiempo_level_medio, np.fmin(exp_level_experto,decada_level_dosmildiez))
        categoria_activation_coches = np.fmin(active_rule3, categoria_coches)

        #Regla 4 -> tiempo["Poco"] & experiencia["Experto"] & decada["Dosmil"], categoria["Plataforma"]
        active_rule6 = np.fmin(tiempo_level_poco,np.fmin(exp_level_experto,decada_level_dosmil))
        categoria_activation_plataforma3 = np.fmin(active_rule6, categoria_plataforma)

        #Regla 5 -> tiempo["Medio"] & decada["Dosmil"] & experiencia["Novato"], categoria["Aventura"]
        active_rule12 = np.fmin(tiempo_level_medio,np.fmin(decada_level_dosmil,exp_level_novato))
        categoria_activation_aventura3 = np.fmin(active_rule12,categoria_aventura)

        #Regla 6 -> tiempo["Poco"] & experiencia["Novato"] & decada["Noventas"], categoria["Aventura"]
        active_rule10 = np.fmin(tiempo_level_poco,np.fmin(exp_level_novato,decada_level_noventas))
        categoria_activation_aventura2 = np.fmin(active_rule10,categoria_aventura)

        #Regla 7 -> tiempo["Poco"] & experiencia["Novato"] & decada["Dosmil"] => Coches
        active_rule14 = np.fmin(tiempo_level_poco,np.fmin(exp_level_novato,decada_level_dosmil))
        categoria_activation_coches3 = np.fmin(active_rule14,categoria_coches)

        #Regla 8 -> tiempo["Mucho"] & experiencia["Experto"] & decada["Dosmildiez"] => Terror
        active_rule15 = np.fmin(tiempo_level_mucho,np.fmin(exp_level_experto,decada_level_dosmildiez))
        categoria_activation_terror2 = np.fmin(active_rule15,categoria_terror)

        #Regla 9 -> tiempo["Mucho"] & experiencia["Experto"] & decada["Dosmil"] => Plataforma
        active_rule16 = np.fmin(tiempo_level_mucho,np.fmin(exp_level_experto,decada_level_dosmil))
        categoria_activation_plataforma5 = np.fmin(active_rule16,categoria_plataforma)

        #Agregacion para 3 entradas
        aggregated = np.fmax(categoria_activation_terror,
                             np.fmax(categoria_activation_accion3,
                                     np.fmax(categoria_activation_coches,
                                             np.fmax(categoria_activation_plataforma3,
                                                     np.fmax(categoria_activation_aventura3,
                                                             np.fmax(categoria_activation_aventura2,
                                                                     np.fmax(categoria_activation_coches3,
                                                                             np.fmax(categoria_activation_terror2,categoria_activation_plataforma5))))))))
    elif (entradas == 2):
        #Reglas con 2 entradas:

        #Regla 10 -> tiempo["Mucho"] & experiencia["Novato"], categoria["Plataforma"]
        active_rule2 = np.fmin(tiempo_level_mucho, exp_level_novato)
        categoria_activation_plataforma = np.fmin(active_rule2,categoria_plataforma)

        #Regla 11 -> tiempo["Medio"] & experiencia["Novato"], categoria["Aventura"]
        active_rule4 = np.fmin(tiempo_level_medio, exp_level_novato)
        categoria_activation_aventura = np.fmin(active_rule4, categoria_aventura)

        #Regla 12 -> (tiempo["Poco"] | decada["Noventas"]) => experiencia["Novato"], categoria["Plataforma"]
        active_rule5 = np.fmin(np.fmax(tiempo_level_poco,decada_level_noventas),exp_level_novato)
        categoria_activation_plataforma2 = np.fmin(active_rule5,categoria_plataforma)

        #Regla 13 -> tiempo["Poco"] & experiencia["Novato"], categoria["Plataforma"]
        active_rule8 = np.fmin(tiempo_level_poco,exp_level_novato)
        categoria_activation_plataforma4 = np.fmin(active_rule8,categoria_plataforma)

        #Regla 14 -> tiempo["Mucho"] & experiencia["Experto"], categoria["Terror"]
        active_rule9 = np.fmin(tiempo_level_mucho,exp_level_experto)
        categoria_activation_terror = np.fmin(active_rule9,categoria_terror)

        #Regla 15 -> (tiempo["Mucho"] |  decada["Dosmil"]) & (experiencia["Experto"], categoria["Coches"]
        active_rule11 = np.fmin(np.fmax(tiempo_level_mucho,decada_level_dosmil),exp_level_experto)
        categoria_activation_coches2 = np.fmin(active_rule11,categoria_coches)

        aggregated = np.fmax(categoria_activation_plataforma,
                             np.fmax(categoria_activation_aventura,
                                     np.fmax(categoria_activation_plataforma2,
                                                     np.fmax(categoria_activation_plataforma4,
                                                             np.fmax(categoria_activation_terror,categoria_activation_coches2)))))
    elif (entradas == 1):
        #Regla 16 -> tiempo["Mucho"] | experiencia["Experto"], categoria["Accion"]
        active_rule7 = np.fmax(tiempo_level_mucho,exp_level_experto)
        categoria_activation_accion = np.fmin(active_rule7,categoria_accion)
        aggregated = categoria_accion

    # ---------------
    #Defuzzificacion utilizando el centroide de area.
    categoria_valor = fuzz.defuzz(x_categoria, aggregated, 'centroid')

    # Grafica de valor defuzzificado
    categoria_activation = fuzz.interp_membership(x_categoria, aggregated, categoria_valor)

    # ---------------
    fig, ax0 = plt.subplots(figsize=(8, 3))
    categoria0 = np.zeros_like(x_categoria)
    ax0.plot(x_categoria, categoria_accion, 'b', linewidth=0.5, linestyle='--', )
    ax0.plot(x_categoria, categoria_plataforma, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(x_categoria, categoria_coches, 'r', linewidth=0.5, linestyle='--')
    ax0.plot(x_categoria, categoria_aventura, 'r', linewidth=0.5, linestyle='--')
    ax0.plot(x_categoria, categoria_terror, 'r', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_categoria, categoria0, aggregated, facecolor='Orange', alpha=0.7)
    ax0.plot([categoria_valor, categoria_valor], [0, categoria_activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Pertenencia agregada y linea de resultado')

    # ---------------
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    plt.tight_layout()

    return categoria_valor

def capturarInformacion(combo1,combo2,radio):
    #Se inicializan variables de utilidad.
    entradas = 0
    num_exp = 0
    num_time = 0
    num_dec = 0

    #---------------
    if (combo2.get() == "No es relevante" or combo2.get() == "Seleccione"):
        num_dec = randint(1990,2022)
        preferenciaDecada = 0
    else:
        preferenciaDecada = int(combo2.get())
        entradas += 1

    # ---------------
    #Se asignan valores a las preferencias de entrada del usuario.
    preferenciaTiempo = combo1.get()
    preferenciaNivelHabilidad = radio.get()
    if (preferenciaNivelHabilidad == ""):
        tkinter.messagebox.showinfo(message="Debe seleccionar un nivel de habilidad", title="Alerta")
        return

    # ---------------
    if (preferenciaTiempo == "Menos de 30 minutos"):
        preferenciaTiempo = "Corta"  # Poner valor numerico
        num_time = 14.5
        entradas += 1
    elif (preferenciaTiempo == "Entre 30 y 90 minutos"):
        preferenciaTiempo = "Media"
        num_time = 40
        entradas += 1
    elif (preferenciaTiempo == "Más de 90 minutos"):
        preferenciaTiempo = "Larga"
        num_time = 100
        entradas += 1
    else:
        preferenciaTiempo = "Seleccione"
        num_time = -1

    # ---------------
    if (preferenciaDecada >= 1990 and preferenciaDecada < 2000):
        num_dec = preferenciaDecada
        preferenciaDecada = "90"  # Poner valor numerico
    elif (preferenciaDecada >= 2000 and preferenciaDecada < 2010):
        num_dec = preferenciaDecada
        preferenciaDecada = "2000"
    elif (preferenciaDecada >= 2010 and preferenciaDecada < 2020):
        num_dec = preferenciaDecada
        preferenciaDecada = "10"
    else:
        preferenciaDecada = "Seleccione"
        num_dec = -1

    # ---------------
    if (preferenciaNivelHabilidad == "Novato"):
        preferenciaNivelHabilidad = "ANY%"  # Poner valor numerico
        num_exp = 1.5
        entradas += 1
    elif (preferenciaNivelHabilidad == "Experto"):
        preferenciaNivelHabilidad = "100%"
        num_exp = 3.5
        entradas += 1
    else:
        preferenciaNivelHabilidad = ""
        num_exp = 0

    #Obtener la categoria de preferencia mediante la Inferencia de Mamdani
    preferenciaCategoria = obtenerCategoria(num_exp, num_time, num_dec,entradas)

    # ---------------
    #Asignar un valor linguistico al valor de retorno.
    if (preferenciaCategoria >= 0.0 and preferenciaCategoria <= 6.5):
        categoria = "Accion"
    elif (preferenciaCategoria > 6.5 and preferenciaCategoria <= 14.0):
        categoria = "Plataforma"
    elif (preferenciaCategoria > 14.0 and preferenciaCategoria <= 21.5):
        categoria = "Coches"
    elif (preferenciaCategoria > 22 and preferenciaCategoria <= 28.5):
        categoria = "Aventura"
    elif (preferenciaCategoria > 28.5 and preferenciaCategoria < 33):
        categoria = "Terror"

    # ---------------
    #Obtener los juegos que cumplan con las preferencias del usuario
    juegosAdecuados = []
    for juego in listaJuegos:
        if (preferenciaDecada == "Seleccione" and preferenciaTiempo != "Seleccione"):
            if (juego.genero == categoria and juego.dificultad == preferenciaNivelHabilidad and juego.tiempo == preferenciaTiempo):
                juegosAdecuados.append(juego)
        elif(preferenciaDecada != "Seleccione" and preferenciaTiempo == "Seleccione"):
            if(juego.genero == categoria and juego.dificultad == preferenciaNivelHabilidad and juego.decada == preferenciaDecada):
                juegosAdecuados.append(juego)
        elif(preferenciaTiempo == "Seleccione" and preferenciaDecada == "Seleccione"):
            if (juego.genero == categoria and juego.dificultad == preferenciaNivelHabilidad):
                juegosAdecuados.append(juego)
        else:
            if (juego.genero == categoria and juego.dificultad == preferenciaNivelHabilidad and juego.decada == preferenciaDecada and juego.tiempo == preferenciaTiempo):
                juegosAdecuados.append(juego)

    # ---------------
    tkinter.messagebox.showinfo(message="Los juegos de la categoria "+categoria+" le van a gustar", title="Recomendaciones")
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

    i = 1
    for juego in juegosAdecuados:
        treeview.insert('', i, values=(juego.nombre, juego.genero, juego.dificultad))
        i +=1

    treeview.pack()
    plt.show()

#Entradas: nombre de usuario y ventana principal.
#Salidas:
#Funcionamiento: Genera la vista de seleccion de preferencias.
def ingresoSistema(inputNombre, ventana):
    nombre = str(inputNombre.get())

    if (nombre == ""):
        tkinter.messagebox.showinfo(message="Debe ingresar un nombre", title="Alerta")
        return
    ventana.destroy()

    selecciones = tkinter.Tk()
    selecciones.geometry("600x450")
    selecciones.resizable(0, 0)
    selecciones.title("Seleccion de preferencias")

    # Cargar imagen para el fondo
    space = tkinter.PhotoImage(file="./img/fondo4.png")
    # small_img=space.subsample(1,1)
    background = tkinter.Label(selecciones, image=space)
    background.space = space
    background.place(x=0, y=0)

    mensaje = tkinter.Label(selecciones, text="Bienvenido " + nombre, bg="#88cffa")
    mensaje.place(x=270, y=20)

    tiempo = tkinter.Label(selecciones, text="¿Con cuanto tiempo cuenta para dedicar al videojuego?", bg="#88cffa")
    tiempo.place(x=50, y=60)

    combo = ttk.Combobox()
    combo = ttk.Combobox(state="readonly", values=["Menos de 30 minutos", "Entre 30 y 90 minutos", "Más de 90 minutos",
                                                   "No es relevante"])
    combo.set("Seleccione")
    combo.place(x=50, y=85)

    decada = tkinter.Label(selecciones, text="¿Es de su preferencia alguna decada en especifico?", bg="#88cffa")
    decada.place(x=50, y=120)

    combo2 = ttk.Combobox()
    combo2 = ttk.Combobox(state="readonly",
                          values=["1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999",
                                  "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
                                  "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019",
                                  "No es relevante"])
    combo2.set("Seleccione")
    combo2.place(x=50, y=145)

    decada = tkinter.Label(selecciones, text="¿Que tan habil se considera?", bg="#88cffa")
    decada.place(x=50, y=180)

    radioValue = tkinter.StringVar()

    rdioNovato = tkinter.Radiobutton(selecciones, text='Novato',
                                     variable=radioValue, value='Novato')
    rdioExperto = tkinter.Radiobutton(selecciones, text='Experto',
                                      variable=radioValue, value='Experto')

    rdioNovato.place(x=50, y=210)
    rdioExperto.place(x=150, y=210)

    enviar = tkinter.Button(selecciones, text="Consultar",
                            command=lambda: capturarInformacion(combo, combo2, radioValue))
    enviar.place(x=510, y=340)

#Entradas:
#Salidas:
#Funcionamiento: Crea la ventana principal.

def root():
    # Crear ventana
    ventana = tkinter.Tk()
    ventana.geometry("600x330")
    ventana.resizable(0, 0)
    ventana.title("Bienvenido")
    # Cargar imagen para el fondo
    bg = tkinter.PhotoImage(file="./img/mario.png")
    small_img = bg.subsample(1, 1)
    background = tkinter.Label(ventana, image=small_img)
    background.bg = bg
    background.place(x=0, y=0)

    # Mensaje de bienvenida
    bienvenida = tkinter.Label(ventana, text="Bienvenido/a al sistema de recomendacion de videojuegos", bg="#88cffa")
    bienvenida.place(x=140, y=40)

    # Etiqueta
    name = tkinter.Label(ventana, text="Ingrese su nombre: ", bg="#88cffa")
    name.place(x=150, y=150)

    # Input para el nombre
    inputNombre = tkinter.Entry(ventana)
    inputNombre.place(x=270, y=150)

    # Boton para ingresar al sistema
    boton = tkinter.Button(ventana, text="Ingresar", command=lambda: ingresoSistema(inputNombre, ventana))
    boton.place(x=390, y=205)

    # Se muestra la ventana
    ventana.mainloop()

def main():
    leerJuegos()
    root()

if (__name__ == "__main__"):
    main()