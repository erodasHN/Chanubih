#!/usr/bin/env python3
# coding:latin-1

from ephem import *
import time
from datetime import datetime
from math import *
import numpy as np
import matplotlib
import matplotlib.patches as patches
import matplotlib.image as mpimg
import matplotlib.ticker as ticker
import io
import os
from tkinter import *
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

matplotlib.use('TkAgg')
global_lugar = Observer()
global_flag_lugar_defecto = 1
global_flag_fecha_defecto = 1

# Initial coordinates of the observer

# Armenia
#global_lugar.lat = '39:33:57.6'
#global_lugar.long = '46:01:42.32'
#global_lugar.date = '2020/3/21'
#global_lugar.elevation = 1800.

# El Puente
#global_lugar.lat = '15.109722'
#global_lugar.long = '-88.79111'
#global_lugar.date = '781/2/8'
#global_lugar.elevation = 478.

# OACS2 - UNAH
global_lugar.lat = '14.0875'
global_lugar.long = '-87.1595'
global_lugar.date = '2020/1/23'
global_lugar.elevation = 1077.

# Cuevas de Ayasta
#global_lugar.lat = '13.931388889'
#global_lugar.long = '-87.2138889'
#global_lugar.date = '2020/3/21'
#global_lugar.elevation = 1077.

# Cuevas de Ayasta2
#global_lugar.lat = '13.932'
#global_lugar.long = '-87.214'
#global_lugar.date = '2020/3/21'
#global_lugar.elevation = 1077.

# Copán Ruinas - Gran Plaza
#global_lugar.lat = '14.839692'
#global_lugar.long = '-89.141994'
#global_lugar.date = '722/3/15'
#global_lugar.elevation = 750.
global_lugar.epoch = global_lugar.date

global f, a, aci, althorg, fig2, ax2, canvas2, ancho_centro, alt_centro, global_n_cuerpoc, diagtype

ancho_centro, alt_centro = 1150, 450

class Chanubih:

    def __init__(self, parent,ancho_p, alto_p):

        global aci, fig2, ax2, canvas2, ancho_centro, alt_centro, global_n_cuerpoc, diagtype, althorg

        def evaluar_e(event):
            global_lugar.date = ent1_fecha.get()+" "
            global_lugar.epoch = global_lugar.date
            print("Fecha de trabajo:",global_lugar.date)

        def evaluar():
            global_lugar.date = ent1_fecha.get()+" "
            global_lugar.epoch = global_lugar.date
            print("Fecha de trabajo:",global_lugar.date)

        def evaluarl_e(event):
            global_lugar.lat = ent1_lugar.get()
            global_lugar.long = ent2_lugar.get()
            global_lugar.elevation = float(ent3_lugar.get())
            print("Datos de trabajo:\nLatitud",global_lugar.lat,"\nLongitud:",global_lugar.long,"\nAltura (msnm):",global_lugar.elevation)

        def evaluarl():
            global_lugar.lat = ent1_lugar.get()
            global_lugar.long = ent2_lugar.get()
            global_lugar.elevation = float(ent3_lugar.get())

        def evaluarA():
            global aci
            aci = float(ent1_alinmtoi.get())

        def evaluarA_e(event):
            global aci
            aci = float(ent1_alinmtoi.get())

        def evaluarAHG():
            global althorg
            althorg = float(ent1_alinmtod.get())
            if althorg > 30.:
                althorg = 30.
                self.v_aviso("Height of window cannot be greater than 30 degrees", "PLEASE CHECK!")
            elif althorg < 5:
                althorg = 5.
                self.v_aviso("Height of window cannot be smaller than 5 degrees", "PLEASE CHECK!")

        def evaluarAHG_e(event):
            global althorg
            althorg = float(ent1_alinmtod.get())
            if althorg > 30.:
                althorg = 30.
                self.v_aviso("Height of horizon cannot be greater than 30 degrees", "PLEASE CHECK!")
            elif althorg < 5:
                althorg = 5.
                self.v_aviso("Height of horizon cannot be smaller than 5 degrees", "PLEASE CHECK!")


        self.myparent = parent

        self.ventana = Frame(parent)                            # Builds Chan U'Bih window
        self.ventana.pack()
        aci = 0.
        althorg = 25.0
        global_n_cuerpoc = "Sun"

        # Creates the cavities within the Chan Ubih screen
        self.creditos = Frame(self.ventana, borderwidth = 2, height = 60, width = ancho_centro, relief = RIDGE)
        self.centro = Frame(self.ventana, borderwidth = 2, height = alt_centro, width = ancho_centro, relief = RIDGE)
        self.aceptar = Frame(self.ventana, borderwidth = 2, height = 30, width = ancho_centro, relief = RIDGE)

        # Creates the cavities within the central cavity
        self.centro_izq = Frame(self.centro,borderwidth = 2, height = alt_centro, width = ancho_centro/2, relief = RIDGE)
        self.centro_der = Frame(self.centro,borderwidth = 2, height = alt_centro, width = ancho_centro/2, relief = RIDGE)

        # Defining color of cavities
        color_fecha = "#90A4AE"
        color_fecha_label = "#78909C" #"#797589"
        color_lugar = "#90A4AE"
        color_lugar_label = "#78909C" #"#758589"
        color_astro = "#78909C" #"#758983"
        color_astro_label = "#78909C" #"#758983"
        color_otrosf = "#78909C"
        color_otrosf_label = "#78909C" #"#757B89"

        # Creates cavities within the larger left cavity
        self.fecha = Frame(self.centro_izq, borderwidth = 5, height=alt_centro/8, width = ancho_centro/4, background = color_fecha, relief = RIDGE)
        self.lugar = Frame(self.centro_izq, borderwidth = 5, height=alt_centro/4+2, width = ancho_centro/4, background = color_lugar, relief = RIDGE)
        self.alinmto = Frame(self.centro_izq, borderwidth = 5, height = alt_centro/8, width = ancho_centro/4, background = color_lugar, relief = RIDGE)
        self.alinmtoi = Frame(self.alinmto, borderwidth = 5, height = alt_centro/8, width = ancho_centro/8, background = color_lugar, relief = RIDGE)
        self.alinmtod = Frame(self.alinmto, borderwidth = 5, height = alt_centro/8, width = ancho_centro/8, background = color_lugar, relief = RIDGE)
        self.otrosf = Frame(self.centro_izq, borderwidth = 5, height = alt_centro/4, width = ancho_centro/4, background = color_otrosf, relief = RIDGE)
        self.astro = Frame(self.centro_izq, borderwidth = 5, height = alt_centro/4, width = ancho_centro/4, background = color_astro, relief = RIDGE)
        self.framegt_s = Frame(self.centro_izq, borderwidth = 5, height = alt_centro/4, width = ancho_centro/4, background = color_astro, relief = RIDGE)
        self.graphtype = Frame(self.framegt_s, borderwidth = 5, height = alt_centro/8, width = ancho_centro/8, background = color_astro, relief = RIDGE)
        self.savepic = Frame(self.framegt_s, borderwidth = 5, height = alt_centro/8, width = ancho_centro/8, background = color_astro, relief = RIDGE)
        self.results = Frame(self.centro_izq, borderwidth = 5, height = alt_centro/8, width = ancho_centro/4, background = color_otrosf, relief = RIDGE)

        # Creates right cavity, in which diagrams will be hosted and prepares its properties
        self.grafico = Frame(self.centro_der, height = alt_centro, width = ancho_centro/2, background="white", relief = RIDGE)

        fig = Figure(figsize=(8.6,7.45))
        ax = fig.add_subplot(111)

        fig.tight_layout()
        ax.set_xlim(0.,1.)
        ax.set_ylim(0.,1.)
        ax.set_axis_off()

        fig2 = Figure(figsize=(4.0,0.9))
        ax2 = fig2.add_subplot(111)
        fig2.tight_layout()
        ax2.set_xlim(0.,0.5)
        ax2.set_ylim(0.,0.1)
        ax2.set_axis_off()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.results)
        canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas2._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.grafico.pack(side=TOP,expand=YES, fill=BOTH)

        # Makes visible the cavities within Chan Ubih
        self.creditos.pack(side=TOP,expand=YES, fill=BOTH)
        self.centro.pack(expand=YES, fill=BOTH)
        self.aceptar.pack(expand=YES, fill=BOTH)

        self.centro_der.pack(side=RIGHT, expand=YES)
        self.centro_izq.pack(side=TOP, expand=YES)
        self.fecha.pack(side = TOP, expand=YES, fill = BOTH)
        self.lugar.pack(expand = YES, fill = BOTH)
        self.alinmto.pack(expand=YES, fill = BOTH)
        self.alinmtoi.pack(side=LEFT, expand = NO, fill=X)
        self.alinmtod.pack(side=TOP, expand = YES, fill=X)

        self.otrosf.pack(expand = YES, fill=BOTH)
        self.astro.pack(expand = YES, fill=BOTH)
        self.framegt_s.pack(expand = YES, fill = BOTH)
        self.graphtype.pack(side = LEFT, expand = NO, fill=X)
        self.savepic.pack(side = TOP, expand = YES, fill=X)
        self.results.pack(expand = YES, fill=BOTH)

        # Defining the specs for each of the created cavities
        # Font size for spaces within frames
        font4space = tkFont.Font(size = 1)
        font4labels = tkFont.Font(size = 6)
        font4buttons = tkFont.Font(size = 7)
        font4moon = tkFont.Font(size = 9)

        # Label the title of the Credits frame ##############################
        row_cred = Frame(self.creditos)
        lab_cred = Label(row_cred, width = 126, text="Archaeoastronomy Software")
        lab_cred.pack(side = TOP)
        lab2_cred = Label(row_cred, width = 126, text=u'Credits: (c) 2021 Eduardo Rodas', font = font4labels)  # \u037B
        lab2_cred.pack()
        row_cred.pack(side=TOP, fill=X, padx=5, pady=1)

        # Getting the date      #################################################
        row1_fecha = Frame(self.fecha, relief = RIDGE, borderwidth = 2) # Heading for the frame that captures dates
        row2_fecha = Frame(self.fecha, highlightthickness = 0)
        row5_fecha = Frame(self.fecha, highlightthickness = 0)
        row6_fecha = Button(self.fecha, text = "Confirm data",command = evaluar, background="#B0BEC5", font = font4buttons)
        row6_fecha.bind("<Return>", evaluar_e)

        lab1_fecha = Label(row1_fecha, width=37, text="DATE", background = color_fecha_label)
        lab2_fecha = Label(row2_fecha, width=19, text="Date (yyyy/mm/dd):", background = color_fecha)
        ent1_fecha = Entry(row2_fecha, background = "white")
        ent1_fecha.bind=("<Return>", evaluar_e)
        lab5_fecha = Label(row5_fecha, width=39, text=" ", background = color_fecha, font = font4space)
        fechayhora = str(date(global_lugar.date))
        pos_espacio = fechayhora.find(" ")
        fecha = fechayhora[:pos_espacio]
        hora = fechayhora[pos_espacio+1:]
        ent1_fecha.insert(0,fecha)

        row1_fecha.pack(side=TOP, fill=BOTH)
        row2_fecha.pack(side=TOP, fill=BOTH)
        row5_fecha.pack(side=TOP, fill=BOTH)
        row6_fecha.pack(side=TOP)

        lab1_fecha.pack(side=TOP, fill=BOTH, expand=YES)
        lab2_fecha.pack(side=LEFT, fill=BOTH, expand=YES)
        lab5_fecha.pack(side=LEFT, fill=BOTH, expand=YES)
        ent1_fecha.pack(side=LEFT, expand=YES, fill=BOTH)

        # Getting the site's coordinates        ###################################
        row1_lugar = Frame(self.lugar, borderwidth = 2, relief = RIDGE)   # Encabezado del recuadro para captura de fechas
        row2_lugar = Frame(self.lugar, highlightthickness = 0)
        row4_lugar = Frame(self.lugar, highlightthickness = 0)
        row6_lugar = Frame(self.lugar, highlightthickness = 0)
        row7_lugar = Frame(self.lugar, highlightthickness = 0, background = color_fecha)
        row8_lugar = Button(self.lugar, text = "Confirm data", command = evaluarl, background="#B0BEC5", font = font4buttons)

        lab1_lugar = Label(row1_lugar, width=37, text="LOCATION", background = color_lugar_label)
        lab2_lugar = Label(row2_lugar, width=19, text=u"Latitude(\u00B1dd:mm:ss):", background = color_lugar)
        ent1_lugar = Entry(row2_lugar, background = "white")
        ent1_lugar.bind=('<Return>',evaluarl)
        lab4_lugar = Label(row4_lugar, width=19, text=u"Longitude:(\u00B1ddd:mm:ss)", background = color_lugar)
        ent2_lugar = Entry(row4_lugar, background = "white")
        ent2_lugar.bind=('<Return>',evaluarl)
        lab6_lugar = Label(row6_lugar, width=19, text="Elevation (masl):", background = color_lugar)
        ent3_lugar = Entry(row6_lugar, background = "white")
        ent3_lugar.bind=('<Return>',evaluarl)
        lab7_lugar = Label(row7_lugar, width=19, text=" ", background = color_lugar, font = font4space)

        ent1_lugar.insert(0,str(global_lugar.lat))
        ent2_lugar.insert(0,str(global_lugar.long))
        ent3_lugar.insert(0,float(global_lugar.elevation))

        row1_lugar.pack(side=TOP, fill=BOTH)
        row2_lugar.pack(side=TOP, fill=BOTH)
        row4_lugar.pack(side=TOP, fill=BOTH)
        row6_lugar.pack(side=TOP, fill=BOTH)
        row7_lugar.pack(side=TOP, fill=BOTH, expand = YES)
        row8_lugar.pack(side=TOP)
        lab1_lugar.pack(side=TOP, fill=BOTH, expand=YES)
        lab2_lugar.pack(side=LEFT, fill=BOTH, expand=YES)
        lab4_lugar.pack(side=LEFT, fill=BOTH, expand=YES)
        lab6_lugar.pack(side=LEFT, fill=BOTH, expand=YES)
        lab7_lugar.pack(side=LEFT, fill=BOTH, expand=YES)
        ent1_lugar.pack(side=LEFT, expand=YES, fill=BOTH)
        ent2_lugar.pack(side=LEFT, expand=YES, fill=BOTH)
        ent3_lugar.pack(side=LEFT, expand=YES, fill=BOTH)

        # Getting the azimuth of the archaeological structure       ####################################
        row1_alinmtoi = Frame(self.alinmtoi, borderwidth = 1)   # Heading of the frame to capture azimuth of alignment
        row2_alinmtoi = Frame(self.alinmtoi, highlightthickness = 0)
        row3_alinmtoi = Frame(self.alinmtoi, highlightthickness = 0)
        row4_alinmtoi = Button(self.alinmtoi, text = "Confirm data", command = evaluarA, background="#B0BEC5", font = font4buttons)
        row4_alinmtoi.bind=('<Return>',evaluarA_e)

        lab1_alinmtoi = Label(row1_alinmtoi, width=18, text="ALIGNMENT TO EVALUATE", background = color_lugar_label)
        lab2_alinmtoi = Label(row2_alinmtoi, width=15, text=u"Azimuth(\u00B1dd.xx):", background = color_lugar)
        ent1_alinmtoi = Entry(row2_alinmtoi, background = "white", width=10)
        lab3_alinmtoi = Label(row3_alinmtoi, width=5, text=" ", background = color_lugar, font = font4space)
        ent1_alinmtoi.insert(0,aci)

        row1_alinmtoi.pack(side=TOP, fill=BOTH)
        row2_alinmtoi.pack(side=TOP)
        row3_alinmtoi.pack(side=TOP)
        row4_alinmtoi.pack(side=TOP)

        lab1_alinmtoi.pack(side=TOP, expand=YES, fill=BOTH)
        lab2_alinmtoi.pack(side=LEFT, expand=NO, fill=BOTH)
        lab3_alinmtoi.pack(side=LEFT, expand=NO)
        ent1_alinmtoi.pack(side=LEFT, expand=NO)


        # Getting the height to show in graph       ####################################
        row1_alinmtod = Frame(self.alinmtod, borderwidth = 1)   # Heading of the frame to capture azimuth of alignment
        row2_alinmtod = Frame(self.alinmtod, highlightthickness = 0)
        row3_alinmtod = Frame(self.alinmtod, highlightthickness = 0)
        row4_alinmtod = Button(self.alinmtod, text = "Confirm data", command = evaluarAHG, background="#B0BEC5", font = font4buttons)
        row4_alinmtod.bind=('<Return>',evaluarAHG_e)

        lab1_alinmtod = Label(row1_alinmtod, width=18, text="HEIGHT TO SHOW IN GRAPH", background = color_lugar_label)
        lab2_alinmtod = Label(row2_alinmtod, width=10, text=u"Height(dd\u00B0):", background = color_lugar)
        ent1_alinmtod = Entry(row2_alinmtod, background = "white", width=10)
        lab3_alinmtod = Label(row3_alinmtod, width=5, text=" ", background = color_lugar, font = font4space)
        ent1_alinmtod.insert(0,althorg)

        row1_alinmtod.pack(side=TOP, fill=BOTH)
        row2_alinmtod.pack(side=TOP)
        row3_alinmtod.pack(side=TOP)
        row4_alinmtod.pack(side=TOP)

        lab1_alinmtod.pack(side=TOP, expand=YES, fill=BOTH)
        lab2_alinmtod.pack(side=LEFT, expand=NO, fill=BOTH)
        lab3_alinmtod.pack(side=LEFT, expand=NO)
        ent1_alinmtod.pack(side=LEFT, expand=NO)

        # Selecting the celestial body to graph     ##################################################
        self.foto_sol = PhotoImage(file = "kin_ico.gif")
        self.foto_luna = PhotoImage(file = "Yueliang_ico.gif")
        self.foto_venus = PhotoImage(file = "Tanit_ico.gif")
        
        self.dropVar = StringVar()
        row1_astro = Frame(self.astro, relief = RIDGE, borderwidth = 2)   # Heading of the frame to select the celestial body to graph
        row2_astro = Button(self.astro, command = lambda arg1="Sun": self.graficar(arg1, fig, ax, canvas,0))
        row2_astro.configure (text = " Graph Sun ", image  = self.foto_sol, width = 89, height = 38, background="#90A4AE")
        row3_astro = Button(self.astro, command = lambda arg1="Moon": self.graficar(arg1, fig, ax, canvas,0))
        row3_astro.configure (text = "Graph Moon", image  = self.foto_luna, width = 89, height = 38, background="#90A4AE")
        row4_astro = Button(self.astro, command = lambda arg1="Sun Events": self.graficar2(arg1, fig, ax, canvas,0))
        row4_astro.configure (text = "Graph Venus", image  = self.foto_venus, width = 89, height = 38, background="#90A4AE") 

        # This is a button that gives access to a menu, where the user chooses from various stars the one to graph  #############################
        optionList = ["Venus","Jupiter","Mars","Antares", "Aldebaran", "Pleyades", "Capella", "Sirius","Arcturus","Fomalhaut"]
        self.dropVar.set("Venus") # This is the default selection
        row5_astro = OptionMenu(self.astro, self.dropVar,*optionList, command = lambda arg1 =self.dropVar: self.graficar(arg1, fig, ax, canvas,1))
        row5_astro.configure (width = 14, height = 2, pady = -1, background="#90A4AE")

        lab1_astro = Label(row1_astro, width=40, text="SELECT A CELESTIAL BODY TO GRAPH", background = color_astro_label)

        row1_astro.pack(side=TOP, fill=BOTH)
        row2_astro.pack(side=LEFT)
        row3_astro.pack(side=LEFT)
        row4_astro.pack(side=LEFT)
        row5_astro.pack(side=LEFT)

        lab1_astro.pack(side=TOP, fill=BOTH, expand=YES)

        # Selecting the computation of other celestial phenomena            ############################################
        row1_otrosf = Frame(self.otrosf, relief = RIDGE, borderwidth = 2)   # Heading of the frame for selection of celestial phenomema to compute
        row2_otrosf = Button(self.otrosf, command = self.coincidir_sol)
        row2_otrosf.configure (text = "Coincidence\nSun-Azimuth", font=font4moon, background="#90A4AE", width = 9)
        row3_otrosf = Button(self.otrosf, command = lambda arg1=0: self.decsluna(arg1))
        row3_otrosf.configure (text = "Major\nlunar\nstandstill", height=2, padx=-1, font=font4moon, background="#90A4AE", width = 9)
        row4_otrosf = Button(self.otrosf, command = lambda arg1=1: self.decsluna(arg1))
        row4_otrosf.configure (text = "Minor\nLunar\nstandstill", height=2, padx=-1, font=font4moon, background="#90A4AE", width = 9)
        row5_otrosf = Button(self.otrosf, command = self.decsvenus)
        row5_otrosf.configure (text = "Max/Min\ndec.Venus", font=font4moon, background="#90A4AE", width = 7)
        row6_otrosf = Button(self.otrosf, command = self.pstz)
        row6_otrosf.configure (text = "Sun passing\nthrough Zenith", font=font4moon, background="#90A4AE", width = 9)

        lab1_otrosf = Label(row1_otrosf, width=38, text="COMPUTE TOPOCENTRICAL EVENTS", background = color_otrosf_label)

        row1_otrosf.pack(side=TOP, fill=BOTH)
        row2_otrosf.pack(side=LEFT)
        row3_otrosf.pack(side=LEFT)
        row4_otrosf.pack(side=LEFT)
        row5_otrosf.pack(side=LEFT)
        row6_otrosf.pack(side=LEFT)

        lab1_otrosf.pack(side=TOP, fill=BOTH, expand=YES)

        # Selecting type of graph to draw           ########################################################
        row1_gt = Frame(self.graphtype, borderwidth = 1)
        optionList2 = ["Cartesian Diagram", "Zotti Diagram"]
        self.dropVar2 = StringVar()
        self.dropVar2.set(optionList2[0]) # This is the default selection
        row2_gt = OptionMenu(self.graphtype, self.dropVar2,*optionList2, command = lambda diagtype: self.graficar(global_n_cuerpoc, fig, ax, canvas,1))
        row2_gt.configure (width = 11, height = 1, background="#90A4AE")

        lab1_gt = Label(row1_gt, width=21, text="DIAGRAM TYPE", background = color_lugar_label)

        row1_gt.pack(side=TOP, fill=X)
        row2_gt.pack(side=TOP, fill=X)
        row2_gt.config(relief=GROOVE, bd=2, background = color_lugar_label)
        lab1_gt.pack(side=TOP, fill=X, expand=NO)

        # Button for saving diagram             ################################################
        row1_sp = Frame(self.savepic, borderwidth = 1)
        row2_sp = Button(self.savepic, command = lambda dpi = 300: self.savepic_r(fig, ax, canvas, dpi))
        row2_sp.configure (text = "Save", width = 9, height = 1, background="#90A4AE")
        lab1_sp = Label(row1_sp, width=9, text="SAVE DIAGRAM", background = color_lugar_label)
        row1_sp.pack(side=TOP, fill=X)
        lab1_sp.pack(side=TOP, fill=X, expand=NO)
        row2_sp.pack(side=TOP, fill=X)

        # Software termination button           ###########################################################
        self.boton_2 = Button(self.aceptar, command = self.salida, text="Exit", background = "#D46A6A", width = 15)
        self.boton_2.pack(side = RIGHT)
        self.boton_2.bind("Return", self.salida)

#*******************************************************
    def savepic_r(self,fig,ax,canvas,dpi_u):

        fields = "Enter a name for the file:"
        fname_0 = os.path.expanduser("~")
        fname_0 = os.path.join(fname_0,"Diagram.png")
        print(fname_0)

        def exitfunction():
            obtalt.destroy()

        def retornar(alt):
            fname = alt.get()    ##### Gets the name of the file where the diagram will be saved
            print("Nombre del archivo: ",fname)
            canvas.print_figure(fname,dpi=dpi_u)
            exitfunction()

        def makeform(obtalt, fields, wwidth, fname): ## This function in intended to work within savepic_r,
            entries = ""            ## only gives shape to widget to capture name of file where diagram
            row = Frame(obtalt)     ## will be saved for a later review
            lab = Label(row, width=wwidth, text=fields, anchor='w')
            ent = Entry(row)
            ent.insert(0,str(fname))
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            return ent

        obtalt=Tk()                     ## Main routine to display a window that captures the filename
        wwidth = 30                     ## of file where diagram will be stored. 
        ents=makeform(obtalt,fields, wwidth, fname_0)
        b1 = Button(obtalt, text='Confirm Name of File', command=(lambda altura=ents: retornar(altura)))
        b1.focus_force()
        b1.pack(side=LEFT, padx=5, pady=5)
        b1.bind('Return', (lambda event, altura=ents: retornar(altura)))
        b2 = Button(obtalt, text='Cancel', command=exitfunction)
        b2.pack(side=RIGHT, padx=5, pady=5)

        obtalt_xpos=int((screen_width - wwidth * 5 - 10*5) / 2)
        obtalt_ypos=int((screen_height * 0.5))
        obtalt.title(" SAVING THE CURRENTLY SHOWN DIAGRAM")
        obtaltWindowPosition="+" + str(obtalt_xpos) + "+" + str(obtalt_ypos)
        obtalt.geometry(obtaltWindowPosition)

        obtalt.mainloop()

#*****************************************************
    def salida(self):
        self.myparent.destroy()

#*****************************************************
    def mensaje(self, fig2, ax2, canvas2, *args): # Writes message in the messaging area according to computed results

        ax2.clear()
        ax2.set_axis_off()
        alin_hor = ['center','center']
        alin_ver = ['bottom', 'top']
        i = 0
        for arg in args:
            ax2.text(-0.12,2.0-(0.47*float(i)), arg,
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=8.5, color='black',
                transform=ax2.transAxes)
            i += 1

        canvas2.draw()

#**********************************************************
    def v_aviso(self, fields, titulo):

        def salir():
            aviso.destroy()    # This command destroys the window
            aviso.quit()       # This command returns control of the program flow to the routine that invoked it

        def salir_a(event):
            salir()
                    
        def makeform(aviso, fields, ancho): ## Esta funcion solo es para uso dentro de v_aviso()
            entries = ""         ## y da forma al widget para capturar el dato requerido                
            row = Frame(aviso)
            lab = Label(row, width = ancho, text=fields)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            return

        aviso = Tk()
        i = fields.find("\n")
        if i == 0:
            ancho = len(fields)
        else:
            ancho = i
        ents = makeform(aviso, fields, ancho)
        screen_width=aviso.winfo_screenwidth()
        screen_height=aviso.winfo_screenheight()

        aviso_xpos = int((screen_width - ancho * 5 - 10*5) / 2)
        aviso_ypos = int((screen_height * 0.5))
        aviso.title(titulo)
        avisoWindowPosition="+" + str(aviso_xpos) + "+" + str(aviso_ypos)
        aviso.geometry(avisoWindowPosition)

        txt_button = "Aceptar"
        b1 = Button(aviso, text=txt_button, command = salir)
        b1.bind('<Return>', (lambda event, ents: salir))
        b1.pack(side = TOP, padx = 5, pady = 5)
        b1.focus_force()

        aviso.mainloop()

#************************************************************
    def CALtoJDE(self,fecha):
        length = len(fecha)
        i = 0
        Y = ""
        while fecha[i] != "/":
            Y = Y + fecha[i]
            i += 1
        i += 1
        M = ""
        while fecha[i] != "/":
            M = M + fecha[i]
            i += 1
        i += 1
        D = ""
        while fecha[i] != " ":
            D = D + fecha[i]
            i += 1

        y, m, d = int(float(Y)), int(float(M)), float(D)

        if m < 3:
            y = y-1
            m = m=m+12

        if y+m/12.+d/365.2422 >= 1582.791068639: # This is in the Gregorian Calendar
            A = int(y/100)
            B = 2 - A + int(A/4)
        else:                                   # This is in the Julian Calendar
            B = 0

        jde = int(365.25*(y+4716))+int(30.6001*(m+1))+d+B-1524.5

        return jde

#************************************************************
    def JDEtoCAL(self,JDE,frac):  # Rutina para obtener la fecha en calendario gregoriano a partir de dias julianos
        JDE = JDE + 0.5
        Z = int(JDE)
        F = JDE - Z
        if Z < 2299161:
            A = Z
        else:
            alfa = int((Z - 1867216.25)/36524.25)
            A = Z + 1 + alfa - int(alfa/4)
        B = A + 1524
        C = int((B - 122.1) / 365.25)
        D = int(365.25 * C)
        E = int((B - D)/ 30.6001)
        dia = B - D - int(30.6001 * E) + F
        diae = int(dia)
        hora = float(int((dia - diae) * 240))/10
        if E < 14:
            mes = E - 1
        else:
            mes = E - 13
        if mes > 2:
            anio = C - 4716
        else:
            anio = C - 4715
        if dia < 10:
            diae = "0" + str(diae)
        else:
            diae = str(diae)
        if frac == 0:
            fecha = str(anio) + "/" + str(mes) + "/" + diae + " "
        else:
            fecha = str(anio) + "/" + str(mes) + "/" + str(dia) + " "
        return fecha

#**************************************************************************
    def coincidir_sol(self): # Routine to compute dates that Sun passes through azimuth under study (if it does happen)

        global fig2, ax2, canvas2, global_lugar, aci
        fields = "Height of horizon at this azimuth"
        bandera = True

        # Computes local horizon
        horizonte = self.horizon(float(global_lugar.lat)*180./np.pi, float(global_lugar.long)*180./np.pi)

############ EVALUATES POSSIBILITY OF ALIGNMENT BETWEEN STRUCTURE'S ORIENTATION AND SUNRISE ##############

############# COMPUTES OBLICUITY OF ECLIPTIC AT THE EPOCH CORRESPONDING TO THE CURRENT DATE
        JDE = self.CALtoJDE(str(global_lugar.date))
        Tcalc = (JDE - 2451545.) / 36525.
        Tcalc2 = Tcalc*Tcalc
        Tcalc3 = Tcalc2*Tcalc
        epsilon_0 = 23.439291111 + (-46.815 *Tcalc - 0.00059 *Tcalc2 + 0.001813 *Tcalc3)/3600.
        # Computes correction to the mean obliquity of the ecliptic, due to nutation
        Omega_epsi0 = (125.04452 - 1934.136261*Tcalc + 0.0020708*Tcalc2 + Tcalc3/450000.)*pi/180.
        L_epsi0 = (280.4665 + 36000.7698*Tcalc)*pi/180.
        Lp_epsi0 = (218.3165 + 481267.8813*Tcalc)*pi/180.
        depsilon_0= 9.2*cos(Omega_epsi0)+0.57*cos(2*L_epsi0)+0.1*cos(2*Lp_epsi0)-0.09*cos(2*Omega_epsi0)
        epsilon = epsilon_0 + depsilon_0/3600.

############# FINDS HEIGHT OF HORIZON WHERE THE ORIENTATION POINTS TO AND COMPUTES CORRESPONDING DECLINATION ##########
        A = float(int(aci))
        B = float(horizonte[int(A)])
        C = float(int(aci+1.))
        D = float(horizonte[int(C)])
        # Computes horizon height at that azimuth, by using proportions between integer azimuth values
        alt_aci = (aci-A)*(D-B)/(C-A) + B
        # Computes declination of Sun, corresponding to that Azimuth and Altitude above the horizon
        dec_aci = sin(global_lugar.lat) * sin(alt_aci*np.pi/180.)
        dec_aci = dec_aci + cos(global_lugar.lat) * cos(alt_aci*np.pi/180.)*cos(aci*np.pi/180.)
        dec_aci = asin(dec_aci) * 180. / np.pi
        # Compares the obtained declination to the maximum the Sun can reach at that date
        if dec_aci > epsilon or dec_aci < -epsilon:
            self.v_aviso("No coincidence can exist between structure's alignment and sunrise/sunset at this azimuth", "PLEASE CHECK!")
            bandera = False

        if bandera:
########################################################################################################################
##########          COMPUTES DECLINATION THE SUN WOULD HAVE IF IT WERE ALIGNED TO THE STRUCTURE             ############
########################################################################################################################
            dec_solar = dec_aci
            if dec_solar >= 0:
                signo_dec = "+"
            else:
                signo_dec = "-"
                dec_solar = dec_solar * -1.
            dec_solarg = int(dec_solar)
            dec_solarm = int((dec_solar-dec_solarg)*60.)
            dec_solars = ((dec_solar-dec_solarg)*60.-dec_solarm)*60.
            dec_solar = str(dec_solarg)+':'+str(dec_solarm)+':'+str(int(dec_solars*10.)/10.)
            print("Sun's declination:", signo_dec+dec_solar)

########### COMPUTES DATES THAT THE SUN REACHES AZIMUTH TO EVALUATE, FINDING THE DIFFERENCE BETWEEN ############
########### EVALUATED AZIMUTH AND SUN'S AZIMUTH. WHEN THIS DIFFERENCE IS MINUMUM, COINCIDENCE OCCURS ###########

            s = Sun()
            o = Observer()
            o.date = global_lugar.date
            o.lat = global_lugar.lat
            o.long = global_lugar.long
            o.elevation = global_lugar.elevation
            o.horizon = str(alt_aci)
            o.date = previous_solstice(o.date)
            s.compute(o)
            if aci < 180.:
                o.date=str(s.rise_time)
            else:
                o.date =str(s.set_time)
            s.compute(o)

            # Computes the date the Sun reaches this declination
            diferencia = abs(float(s.az)*180/np.pi - aci)
            i = 0
            while abs(float(s.az)*180/np.pi - aci) <= diferencia and i < 183:
                diferencia = abs(float(s.az)*180/np.pi - aci)
                o.date = o.date + (24*hour)
                s.compute(o)
                if aci < 180.:
                    o.date=str(s.rise_time)
                else:
                    o.date = str(s.set_time)
                s.compute(o)
                i += 1
            o.date = o.date - 24*hour  # Primera fecha encontrada en que el Sol pasa por ese acimut
            d1 = o.date
            print("Intentos:",i)
            print("d1=", d1)

            o.date = next_solstice(o.date)
            s.compute(o)
            if aci < 180.:
                o.date=str(s.rise_time)
            else:
                o.date =str(s.set_time)
            s.compute(o)

            diferencia = abs(float(s.az)*180/np.pi - aci)
            i = 0
            while abs(float(s.az)*180/np.pi - aci) <= diferencia and i < 183:
                diferencia = abs(float(s.az)*180/np.pi - aci)
                o.date = o.date + (24*hour)
                s.compute(o)
                if aci < 180.:
                    o.date=str(s.rise_time)
                else:
                    o.date = str(s.set_time)
                s.compute(o)
                i += 1
            o.date = o.date - 24*hour  # Segunda fecha encontrada en que el Sol pasa por ese acimut
            d2 = o.date
            print("Intentos:",i)
            print("d2=", d2)

            msj0 = "COINCIDENCE SUN - AZIMUTH"
            m1_1 = str(float(int(aci*1000.))/1000.)
            msj1 = u"Declination of Sun when in azimuth " + m1_1 + " : " + dec_solar
            msj2 = "Dates that Sun passes through these azimuth, for latitude "+str(o.lat)
            msj3 = " "
            msj4 = d1
            msj5 = 'or'
            msj6 = d2
            self.mensaje(fig2, ax2, canvas2, msj0, msj2, msj3, msj4, msj5, msj6)

#**************************************************************
    def coincidir_sol_a(self):
        self.coincidir_sol()

#*************************************************************
    def pstz(self): # Routine to compute dates when Sun passes through Zenith (if possible)

            global fig2, ax2, canvas2, global_lugar
            fields = "Height of horizon at this point"
            bandera = True

            print("Finding date of the passing of the Sun through the Zenith")
            print("Computing ...")
############ EVALUA SI ES POSIBLE EL PASO DEL SOL POR EL CENIT EN ESE LUGAR ##############

############# CALCULA LA OBLICUIDAD DE LA ECLIPTICA EN LA EPOCA CORRESPONDIENTE A LA FECHA ACTUAL 
            JDE = self.CALtoJDE(str(global_lugar.date))
            Tcalc = (JDE - 2451545.) / 36525.
            Tcalc2 = Tcalc*Tcalc
            Tcalc3 = Tcalc2*Tcalc
            epsilon_0 = 23.439291111 + (-46.815 *Tcalc - 0.00059 *Tcalc2 + 0.001813 *Tcalc3)/3600.
            # Calcula la correccion (nutacion en oblicuedad) a la oblicuedad media de la ecliptica
            Omega_epsi0 = (125.04452 - 1934.136261*Tcalc + 0.0020708*Tcalc2 + Tcalc3/450000.)*pi/180.
            L_epsi0 = (280.4665 + 36000.7698*Tcalc)*pi/180.
            Lp_epsi0 = (218.3165 + 481267.8813*Tcalc)*pi/180.
            depsilon_0= 9.2*cos(Omega_epsi0)+0.57*cos(2*L_epsi0)+0.1*cos(2*Lp_epsi0)-0.09*cos(2*Omega_epsi0)
            epsilon = epsilon_0 + depsilon_0/3600.

            if float(global_lugar.lat) * 180 / np.pi > epsilon:
                self.v_aviso("The Sun does not pass through the zenith at this latitude","WARNING!")
            else:
                aci = acos(tan(global_lugar.lat))*180/np.pi            

############# EVALUA EL ACIMUT DEL SOL EL SOLSTICIO DE VERANO SITIO DE OBSERVACION (USA LA OBLICUiDAD EN LA ÉPOCA DE LA FECHA) ###############
                min_acimut_solar1 = sin(epsilon_0 * pi / 180.)
                min_acimut_solar2 = cos(global_lugar.lat)
                try:
                   min_acimut_solar = acos(min_acimut_solar1 / min_acimut_solar2) * 180. / pi
                except:
                   min_acimut_solar = 0.
                   self.v_aviso("Minimum solar azimuth could not be computed", "WARNING!")

############# AHORA EVALUA EL ACIMUT DEL SOL EL SOLSTICIO DE INVIERNO EN SITIO DE OBSERVACION (USA LA OBLICUiDAD EN LA EPOCA DE LA FECHA) ########
                max_acimut_solar1 = sin(-epsilon_0 * pi / 180.)
                max_acimut_solar2 = cos(global_lugar.lat)
                try:
                    max_acimut_solar = acos(max_acimut_solar1 / max_acimut_solar2) * 180. / pi
                except:
                    max_acimut_solar = 180.
                    self.v_aviso("Maximum solar azimuth could not be computed", "WARNING!")

############# ENCUENTRA CUAL ES EL ACIMUT DEL SOLSTICIO MAS CERCANO A LA ALINEACION INGRESADA #########################
###### Y EVALUA SI ESTA SE ENCUENTRA DENTRO DEL RANGO DE POSIBLES ALINEACIONES CON EL SOL EN SITIO DE OBSERVACION #####
                if aci > 180.:
                    temporal = min_acimut_solar
                    min_acimut_solar = 360.0 - max_acimut_solar
                    max_acimut_solar = 360.0 - temporal

           #######   ESTO SOLO ES PARA PROPOSITOS DE CONTROL ###################
                if abs(aci-min_acimut_solar) < abs(aci-max_acimut_solar):
                    print(u"Acimut m\u00EDnimo que puede tener el Sol a esa altura=", min_acimut_solar)
                    print(u"Acimut m\u00E1ximo que puede tener el Sol a esa altura=", max_acimut_solar)
            ####################################################################

                if aci < min_acimut_solar or aci > max_acimut_solar:
                    self.v_aviso("The Sun does not pass through the zenith at this latitude","WARNING!")
                    bandera = False

########################################################################################################################
########## CALCULA LA DECLINACION QUE TENDRIA EL SOL SI ESTUVIERA ALINEADO CON LA ESTRUCTURA (EPOCA J2000.0)############
########################################################################################################################
                if bandera:
                    dec_solar = cos(global_lugar.lat) * cos(aci*np.pi/180.)
                    dec_solar = asin(dec_solar) * 180. / np.pi
                    if dec_solar >= 0:
                        signo_dec = "+"
                    else:
                        signo_dec = "-"
                        dec_solar = dec_solar * -1.
                    dec_solarg = int(dec_solar)
                    dec_solarm = int((dec_solar-dec_solarg)*60.)
                    dec_solars = ((dec_solar-dec_solarg)*60.-dec_solarm)*60.
                    dec_solar = str(dec_solarg)+':'+str(dec_solarm)+':'+str(int(dec_solars*10.)/10.)
                    print("Declinación del Sol:", dec_solar)

########### ENCUENTRA LAS FECHAS EN QUE EL SOL ALCANZA EL ACIMUT A EVALUAR, HALLANDO LA DIFERENCIA ENTRE ############
############# ACIMUT EVALUADO Y ACIMUT DEL SOL, CUANDO ESTA DIFERENCIA ES MINIMA, OCURRE COINCIDENCIA ###############

                    s = Sun()
                    o = Observer()
                    o.date = global_lugar.date
                    o.lat = global_lugar.lat
                    o.long = global_lugar.long
                    o.elevation = global_lugar.elevation
                    o.horizon = "0.0"
                    o.date = previous_solstice(o.date)
                    s.compute(o)
                    if aci < 180.:
                        o.date=str(s.rise_time)
                    else:
                        o.date =str(s.set_time)
                    s.compute(o)
    
                    diferencia = abs(float(s.az)*180/np.pi - aci)
                    i = 0
                    # Evalua la fecha de cuando la diferencia encontrada entre el acimut calculado del Sol
                    # y el acimut que tiene el Sol en el día del paso del sol por el cenit
                    while abs(float(s.az)*180/np.pi - aci) <= diferencia and i < 183:
                        diferencia = abs(float(s.az)*180/np.pi - aci)
                        o.date = o.date + (24*hour)
                        s.compute(o)
                        if aci < 180.:
                            o.date=str(s.rise_time)
                        else:
                            o.date = str(s.set_time)
                        s.compute(o)
                        i += 1
                    o.date = o.date - 24*hour  # Primera fecha encontrada en que el Sol pasa por ese acimut
                    d1 = o.date
                    print("Intentos:",i, "; ",o.date)
                    print(" ")

                    o.date = next_solstice(o.date)
                    s.compute(o)
                    if aci < 180.:
                        o.date=str(s.rise_time)
                    else:
                        o.date =str(s.set_time)
                    s.compute(o)
    
                    diferencia = abs(float(s.az)*180/np.pi - aci)
                    i = 0
                    while abs(float(s.az)*180/np.pi - aci) <= diferencia and i < 183:
                        diferencia = abs(float(s.az)*180/np.pi - aci)
                        o.date = o.date + (24*hour)
                        s.compute(o)
                        if aci < 180.:
                            o.date=str(s.rise_time)
                        else:
                            o.date = str(s.set_time)
                        s.compute(o)
                        i += 1
                    o.date = o.date - 24*hour  # Segunda fecha encontrada en que el Sol pasa por ese acimut
                    d2 = o.date
                    print("Intentos:",i, "; ",o.date)
    
                    print(d1, "  ", d2)
    
                    msj0 = "PASSING OF SUN THROUGH ZENITH"
                    m1_1 = str(float(int(aci*1000.))/1000.)
                    msj1 = u"Declination of Sun in the azimuth " + m1_1 + " : " + dec_solar
                    msj2 = "Dates of passing of the Sun through zenith, for latitude "+str(o.lat)
                    msj3 = " "
                    msj4 = d1
                    msj5 = 'or'
                    msj6 = d2
                    self.mensaje(fig2, ax2, canvas2, msj0, msj2, msj3, msj4, msj5, msj6)

#****************************************************************
    def pstz_a(self):
        self.pstz()

#***************************************************************
    def aniodecimal(self,fechat,incldia):      # Transforms from format yyyy/mm/dd to decimal year
                                               # 1=computes to the day of the year, 0=computes to beginning of first day of month
        anio = ""
        mes = ""
        dia = ""
        i = 0
        while fechat[i] != "/":
            anio = anio + fechat[i]
            i += 1
        i += 1
        while fechat[i] != "/":
            mes = mes + fechat[i]
            i += 1
        i += 1
        while fechat[i] != " ":
            dia = dia + fechat[i]
            i += 1
        y = float(anio) + (float(mes) - 1.)/12. + incldia*(float(dia)/365.2422)

        return y

#**************************************************************
    def lunapasanodo(self,k,E): # CALCULA PASOS DE LA LUNA A TRAVES DE LOS NODOS

        T = k / 1342.23
        D = 183.6380 + 331.73735691*k + 0.0015057*T*T + 0.00000209*T*T*T - 0.000000010*T*T*T*T
        M = 17.4006 + 26.82037250*k + 0.0000999*T*T + 0.00000006*T*T*T
        Mp = 38.3776 + 355.52747322*k + 0.0123577*T*T + 0.000014628*T*T*T - 0.000000069*T*T*T*T
        omega = 123.9767 - 1.44098949*k + 0.0020625*T*T + 0.00000214*T*T*T - 0.000000016*T*T*T*T
        V = 299.75 + 132.85*T - 0.009173*T*T
        P = omega + 272.75 - 2.3*T
        D = D*np.pi / 180.
        M = M*np.pi/180.
        Mp = Mp*np.pi/180.
        omega = omega*np.pi/180.
        V = V*np.pi/180.
        P = P*np.pi/180.

        JDEpasanodo = 2451565.1619 + 27.212220817*k + 0.0002572*T*T + 0.000000021*T*T*T
        JDEpasanodo = JDEpasanodo - 0.000000000088*T*T*T*T - 0.4721*sin(Mp) - 0.1649*sin(2.*D)
        JDEpasanodo = JDEpasanodo - 0.0868*sin(2.*D - Mp) + 0.0084*sin(2.*D + Mp)
        JDEpasanodo = JDEpasanodo - 0.0083*E*sin(2.*D - M) - 0.0039*E*sin(2.*D-M-Mp) + 0.0034*sin(2.*Mp)
        JDEpasanodo = JDEpasanodo - 0.0031*sin(2.*D-2.*Mp) + 0.003*E*sin(2.*D+M) + 0.0028*E*sin(M-Mp)
        JDEpasanodo = JDEpasanodo + 0.0026*E*sin(M) + 0.0025*sin(4.*D) + 0.0024*sin(D)
        JDEpasanodo = JDEpasanodo + 0.0022*E*sin(M+Mp) + 0.0017*sin(omega) + 0.0014*sin(4.*D-Mp)
        JDEpasanodo = JDEpasanodo + 0.0005*E*sin(2.*D+M-Mp) + 0.0004*E*sin(2.*D-M+Mp)
        JDEpasanodo = JDEpasanodo - 0.0003*E*(sin(2.*D-2.*M) - sin(4.*D-M)) + 0.0003*(sin(V)+sin(P))

        return [JDEpasanodo, omega]

#******************************************************************
    def dextremasluna(self, k, E): # Calcula fechas de decs max y min, asi como la dec. correspondiente a lunacion k
        T = k / 1336.86
        Dn = (152.2029 + 333.0705546 * k - 0.00004025 * T * T + 0.00000011 * T * T * T) * np.pi / 180.
        Ds = (345.6676 + 333.0705546 * k - 0.00004025 * T * T + 0.00000011 * T * T * T) * np.pi / 180.
        Mn = (14.8591 + 26.9281592 * k -0.0000544 * T * T - 0.00000010 * T * T * T) * np.pi / 180.
        Ms = (1.39510 + 26.9281592 * k -0.0000544 * T * T - 0.00000010 * T * T * T) * np.pi / 180.
        Mpn = (4.6881 + 356.9562795 * k + 0.0103126 * T * T + 0.00001251 * T * T * T) * np.pi / 180.
        Mps = (186.21 + 356.9562795 * k + 0.0103126 * T * T + 0.00001251 * T * T * T) * np.pi / 180.
        Fn = (325.8867 + 1.4467806 * k - 0.0020708 * T * T - 0.00000215 * T * T * T) * np.pi / 180.
        Fs = (145.1633 + 1.4467806 * k - 0.0020708 * T * T - 0.00000215 * T * T * T) * np.pi / 180.

                ############## Calculo de los terminos periodicos de la Tabla 50.A del libro de Meeus
        T50An = 0.8975*cos(Fn) - 0.4726*sin(Mpn) - 0.103*sin(2.*Fn) - 0.0976*sin(2.*Dn-Mpn)
        T50An = T50An - 0.0462*cos(Mpn-Fn) - 0.0461*cos(Mpn+Fn) - 0.0438*sin(2.*Dn) + 0.0162*E*sin(Mn)
        T50An = T50An - 0.0157*cos(3.*Fn) + 0.0145*sin(Mpn+2.*Fn) + 0.0136*cos(2.*Dn-Fn)
        T50An = T50An - 0.0095*cos(2.*Dn-Mpn-Fn) - 0.0091*cos(2.*Dn-Mpn+Fn) - 0.0089*cos(2.*Dn+Fn)
        T50An = T50An + 0.0075*sin(2.*Mpn) - 0.0068*sin(Mpn-2*Fn) + 0.0061*cos(2.*Mpn-Fn)
        T50An = T50An - 0.0047*sin(Mpn+3.*Fn) - 0.0043*E*sin(2.*Dn-Mn-Mpn) - 0.004*cos(Mpn-2.*Fn)
        T50An = T50An - 0.0037*sin(2.*Dn-2*Mpn) + 0.0031*sin(Fn) + 0.003*sin(2.*Dn+Mpn)
        T50An = T50An - 0.0029*cos(Mpn+2.*Fn) - 0.0029*E*sin(2.*Dn-Mn) - 0.0027*sin(Mpn+Fn)
        T50An = T50An + 0.0024*E*sin(Mn-Mpn) - 0.0021*sin(Mpn-3.*Fn) + 0.0019*sin(2.*Mpn+Fn)
        T50An = T50An + 0.0018*(cos(2.*Dn-2.*Mpn-Fn) + sin(3.*Fn)) + 0.0017*(cos(Mpn+3.*Fn) + cos(2.*Mpn))
        T50An = T50An - 0.0014*cos(2.*Dn-Mpn) + 0.0013*(cos(2.*Dn+Mpn+Fn)+cos(Mpn))+0.0012*sin(3.*Mpn+Fn)
        T50An = T50An + 0.0011*(sin(2.*Dn-Mpn+Fn)-cos(2.*Dn-2.*Mpn)) + 0.001*(cos(Dn+Fn)+E*sin(Mn+Mpn))
        T50An = T50An - 0.0009*sin(2.*Dn-2.*Fn) + 0.0007*cos(2.*Mpn+Fn) - 0.0007*cos(3.*Mpn+Fn)

        T50As = -0.8975*cos(Fs) - 0.4726*sin(Mps) - 0.103*sin(2.*Fs) - 0.0976*sin(2.*Ds-Mps)
        T50As = T50As + 0.0541*cos(Mps-Fs) + 0.0516*cos(Mps+Fs) - 0.0438*sin(2.*Ds) + 0.0112*E*sin(Ms)
        T50As = T50As + 0.0157*cos(3.*Fs) + 0.0023*sin(Mps+2.*Fs) - 0.0136*cos(2.*Ds-Fs)
        T50As = T50As + 0.0110*cos(2.*Ds-Mps-Fs) + 0.0091*cos(2.*Ds-Mps+Fs) + 0.0089*cos(2.*Ds+Fs)
        T50As = T50As + 0.0075*sin(2.*Mps) - 0.0030*sin(Mps-2*Fs) - 0.0061*cos(2.*Mps-Fs)
        T50As = T50As - 0.0047*sin(Mps+3.*Fs) - 0.0043*E*sin(2.*Ds-Ms-Mps) + 0.004*cos(Mps-2.*Fs)
        T50As = T50As - 0.0037*sin(2.*Ds-2*Mps) - 0.0031*sin(Fs) + 0.003*sin(2.*Ds+Mpn)
        T50As = T50As + 0.0029*cos(Mps+2.*Fs) - 0.0029*E*sin(2.*Ds-Ms) - 0.0027*sin(Mps+Fs)
        T50As = T50As + 0.0024*E*sin(Ms-Mps) - 0.0021*sin(Mps-3.*Fs) - 0.0019*sin(2.*Mps+Fs)
        T50As = T50As - 0.0006*cos(2.*Ds-2.*Mps-Fs) - 0.0018*sin(3.*Fs)-0.0017*(cos(Mps+3.*Fs)-cos(2.*Mps))
        T50As = T50As + 0.0014*cos(2.*Ds-Mps) - 0.0013*(cos(2.*Ds+Mps+Fs)+cos(Mps))+0.0012*sin(3.*Mps+Fs)
        T50As = T50As + 0.0011*(sin(2.*Ds-Mps+Fs)+cos(2.*Ds-2.*Mps)) + 0.001*(cos(Ds+Fs)+E*sin(Ms+Mps))
        T50As = T50As - 0.0009*sin(2.*Ds-2.*Fs) - 0.0007*cos(2.*Mps+Fs) - 0.0007*cos(3.*Mps+Fs)

        JDEn = 2451562.5897 + 27.321582241*k + 0.000100695*T*T - 0.000000141*T*T*T + T50An
        JDEs = 2451548.9289 + 27.321582241*k + 0.000100695*T*T - 0.000000141*T*T*T + T50As

                ############## Calculo de los terminos periodicos de la Tabla 50.B del libro de Meeus
        T50Bn = 5.1093*sin(Fn) + 0.2658*cos(2*Fn) + 0.1448*sin(2.*Dn-Fn) - 0.0322*sin(3.*Fn)
        T50Bn = T50Bn + 0.0133*cos(2.*Dn-2.*Fn) + 0.0125*cos(2.*Dn) - 0.0124*sin(Mpn-Fn)
        T50Bn = T50Bn - 0.0101*sin(Mpn+2.*Fn) + 0.0097*cos(Fn) - 0.0087*E*sin(2.*Dn+Mn-Fn)
        T50Bn = T50Bn + 0.0074*sin(Mpn+3.*Fn) + 0.0067*sin(Dn+Fn) + 0.0063*sin(Mpn-2.*Fn)
        T50Bn = T50Bn + 0.0060*E*sin(2.*Dn-Mn-Fn) - 0.0057*sin(2.*Dn-Mpn-Fn) - 0.0056*cos(Mpn+Fn)
        T50Bn = T50Bn + 0.0052*cos(Mpn+2.*Fn) + 0.0041*cos(2.*Mpn+Fn) - 0.004*cos(Mpn-3.*Fn)
        T50Bn = T50Bn + 0.0038*cos(2.*Mpn-Fn) - 0.0034*cos(Mpn-2.*Fn) - 0.0029*sin(2.*Mpn)
        T50Bn = T50Bn + 0.0029*sin(3.*Mpn+Fn) - 0.0028*(E*cos(2.*Dn+Mn-Fn) + cos(Mpn-Fn))
        T50Bn = T50Bn - 0.0023*cos(3.*Fn) - 0.0021*sin(2.*Dn+Fn) + 0.0019*cos(Mpn+3.*Fn)
        T50Bn = T50Bn + 0.0018*cos(Dn+Fn) + 0.0017*sin(2.*Mpn-Fn) + 0.0015*cos(3.*Mpn+Fn)
        T50Bn = T50Bn + 0.0014*cos(2.*Dn+2.*Mpn+Fn)-0.0012*(sin(2.*Dn-2.*Mpn-Fn) + cos(2.*Mpn))
        T50Bn = T50Bn - 0.0010*(cos(Mpn) + sin(2.*Fn)) + 0.0006*sin(Mpn+Fn)

        T50Bs = -5.1093*sin(Fs) + 0.2658*cos(2*Fs) - 0.1448*sin(2.*Ds-Fs) + 0.0322*sin(3.*Fs)
        T50Bs = T50Bs + 0.0133*cos(2.*Ds-2.*Fs) + 0.0125*cos(2.*Ds) - 0.0015*sin(Mps-Fs)
        T50Bs = T50Bs + 0.0101*sin(Mps+2.*Fs) - 0.0097*cos(Fs) + 0.0087*E*sin(2.*Ds+Ms-Fs)
        T50Bs = T50Bs + 0.0074*sin(Mps+3.*Fs) + 0.0067*sin(Ds+Fs) - 0.0063*sin(Mps-2.*Fs)
        T50Bs = T50Bs - 0.0060*E*sin(2.*Ds-Ms-Fs) + 0.0057*sin(2.*Ds-Mps-Fs) - 0.0056*cos(Mps+Fs)
        T50Bs = T50Bs - 0.0052*cos(Mps+2.*Fs) - 0.0041*cos(2.*Mps+Fs) - 0.004*cos(Mps-3.*Fs)
        T50Bs = T50Bs - 0.0038*cos(2.*Mps-Fs) + 0.0034*cos(Mps-2.*Fs) - 0.0029*sin(2.*Mps)
        T50Bs = T50Bs + 0.0029*sin(3.*Mps+Fs) + 0.0028*(E*cos(2.*Ds+Ms-Fs) - cos(Mps-Fs))
        T50Bs = T50Bs + 0.0023*cos(3.*Fs) + 0.0021*sin(2.*Ds+Fs) + 0.0019*cos(Mps+3.*Fs)
        T50Bs = T50Bs + 0.0018*cos(Ds+Fs) - 0.0017*sin(2.*Mps-Fs) + 0.0015*cos(3.*Mps+Fs)
        T50Bs = T50Bs + 0.0014*cos(2.*Ds+2.*Mps+Fs) + 0.0012*(sin(2.*Dn-2.*Mps-Fs) - cos(2.*Mps))
        T50Bs = T50Bs + 0.0010*(cos(Mps) - sin(2.*Fs)) + 0.0037*sin(Mps+Fs)

        maxdecn = 23.6961 - 0.013004 * T + T50Bn
        maxdecs = 23.6961 - 0.013004 * T + T50Bs

        return [JDEn, maxdecn, JDEs, maxdecs]

    def decsluna(self,decisn):  # New way to compute declinations of the moon

        fechat = str(global_lugar.date)
        JDE = self.CALtoJDE(fechat)
        Tjde = (JDE - 2451545.)/36525. # Formula 22.1 of AA by Meeus

        # Now, computes the longitude of ascending node (omega) by using equation 47.7 from the
        # second edition of "Astronomical Algorithms" by Meeus, obtained from (Chapront,1998)
        omega = 125.04455479-1934.1362891*Tjde+0.0020754*Tjde*Tjde+Tjde*Tjde*Tjde/467441.-Tjde*Tjde*Tjde*Tjde/60616000.
        omega = (omega/360. - float(int(omega/360.)))*360.

        # Computes the difference between the longitude of asc. node and the longitude of the vernal point (when omega =0)
        # according to when it was closer: the past (359.99>omega>180) or the future (0<omega<180)

        if omega < 0:
            omega = omega + 360.

        if decisn == 0:
            if omega > 180.:
                domega = 360. - omega
            else:
                domega = omega
        else:
            if omega > 180.:
                domega = omega - 180.
            else:
                domega = 180. - omega

        # Computes the absolute speed with which omega is changing, at the time that was input by user
        v = abs(-1934.1362891+0.0020754*Tjde+Tjde*Tjde/467441.-Tjde*Tjde*Tjde/60616000.)

        # if the long. of asc node is closer in the past, then we will move in time (T) negatively
        if decisn == 0:
            if omega > 180.:
                v = -v
        else:
            if omega < 180.:
                v = -v

        Tl = Tjde + domega / v

        # Computes the long of asc node in the time T that was computed and finds the corresponding julian date
        omegan = 125.04455479-1934.1362891*Tl+0.0020754*Tl*Tl+Tl*Tl*Tl/467441.-Tl*Tl*Tl*Tl/60616000.
        omegan = (omegan/360. - float(int(omegan/360.)))*360.
        JDE = Tl*36525. + 2451545.

        # Finds if Moon's longitude is near 90 or 270 degrees and decides whether to compute T closest
        # to when the Moon reaches 90 or 270 degrees, using equation 47.1

        Lp = 218.3164477+481267.88123421*Tl-0.0015786*Tl*Tl+Tl*Tl*Tl/538841.-Tl*Tl*Tl*Tl/65194000.
        Lp = (Lp/360. - float(int(Lp/360.)))*360.
        if Lp < 0.:
            Lpc = Lp + 360.
        else:
            Lpc = Lp
    
        if abs(270.-Lpc) < abs (90.-Lpc):
            dLp = 270. - Lpc
        else:
            dLp = 90 - Lpc

        vL = 481267.88123421-0.0015786*Tl+Tl*Tl/538841.-Tl*Tl*Tl/65194000.

        Tlf = Tl + dLp / vL
        Lpf = 218.3164477+481267.88123421*Tlf-0.0015786*Tlf*Tlf+Tlf*Tlf*Tlf/538841.-Tlf*Tlf*Tlf*Tlf/65194000.
        Lpf = (Lpf/360. - float(int(Lpf/360.)))*360.
        if Lpf < 0.:
            Lpf = Lpf + 360.
        else:
            Lpf = Lpf

        jdef = Tlf*36525. + 2451545.
        fechat = self.JDEtoCAL(jdef,0)

        # After finding the date that the longitude of the ascending node is closer to zero, and the longitude of Moon is 90 or 270
        # takes this date as starting point to compute the date the Moon reaches maximum declinations, as seen from the observer's location
        y = self.aniodecimal(fechat,0) # Third parameter is to determine whether to include
                                       # the days in the computation of decimal year, 1=yes, 0=no
        E = 1 - 0.002516 * Tlf - 0.0000074 * Tlf * Tlf
        k = int(abs(y - 2000.03) * 13.3686)
        if y < 2000.03:
            k = -k
        k = float(k)

        msj1 = " "
###################################################****************************************************************************************
                ### Llama la rutina para determinar las fechas (julianas) de las declinaciones extremas
                ### de la Luna hacia el N y al S, asi como el valor de dichas declinaciones
                ### 0 -> JDEn / 1 -> Maxima decl Norte / 2 -> JDEs / 3 -> Maxima decl Sur
                ### para la lunacion k que hemos encontrado

        i = 0
        maxdecn_ant = 0
        maxdecs_ant = 0
        maxdecn_ant_ant = 0
        maxdecs_ant_ant = 0
        bandera = True
        direccion_k = +1.
        while bandera:
            temporal = self.dextremasluna(k,E)

                # Calcula el valor de la longitud del nodo ascendente de la Luna en las fechas (julianas)
                # en que ocurren las maximas declinaciones de la Luna (segun formula 47.7 de A-A de Meeus), de esta
                # manera, se hace un ajuste (si es necesario) para acercar la fecha de los calculos al
                # momento en que el nodo ascendente de la orbita lunar esta cerca del equinoccio vernal.
            JDEn = temporal[0]
            Tjde = (JDEn - 2451545.) / 36525.
            omegan = 125.0445479-1934.1362891*Tjde+0.0020754*Tjde*Tjde+Tjde*Tjde*Tjde/467441.-Tjde*Tjde*Tjde*Tjde/60616000.
            omegan = ((omegan / 360.) - int(omegan / 360.)) * 360.
            if omegan < 0:
                omegan += 360.

            JDEs = temporal[2]
            Tjde = (JDEs - 2451545.) / 36525.
            omegas = 125.0445479-1934.1362891*Tjde+0.0020754*Tjde*Tjde+Tjde*Tjde*Tjde/467441.-Tjde*Tjde*Tjde*Tjde/60616000.
            omegas = ((omegas / 360.) - int(omegas / 360.)) * 360.
            if omegas < 0:
                omegas += 360.

                # Gets the gregorian dates in which maximum declinations of the Moon happen
            fechan = self.JDEtoCAL(JDEn,0)
            fechas = self.JDEtoCAL(JDEs,0)

            maxdecn = temporal[1]
            maxdecs = temporal[3]

            if i == 1 and abs(maxdecn) < abs(maxdecn_ant):
                direccion_k = direccion_k * (-1)
            else:
                if abs(maxdecn) < abs(maxdecn_ant):
                    bandera = False
                    maxdecn = maxdecn_ant
                    JDEn = JDEn_ant
                    fechan = self.JDEtoCAL(JDEn,0)
                    if abs(maxdecs) < abs(maxdecs_ant):
                        maxdecs = maxdecs_ant
                        JDEs = JDEs_ant
                        fechas = self.JDEtoCAL(JDEs,0)
                else:
                    maxdecn_ant = maxdecn
                    JDEn_ant = JDEn
                    if abs(maxdecs) > abs(maxdecs_ant):
                        maxdecs_ant = maxdecs
                        JDEs_ant = JDEs
            i += 1
            k = k + direccion_k

################################################
                # Aqui se calculan los datos relativos a la Luna para el sitio de observacion: acimut a la salida y la
                # puesta, usando las fechas encontradas de maxima declinacion norte y maxima declinacion Sur
                # mostrando previamente las fechas de "lunasticios" mas cercanos a la fecha ingresada por el usuario

        horizonte = self.horizon(float(global_lugar.lat)*180./np.pi, float(global_lugar.long)*180./np.pi) # Calcula el horizonte local

        if JDEn > 1721423.5:
            if decisn == 0:
                msj2 = "Major Northern declination"
            else:
                msj2 = "Minor Northern declination"
            msj3 = "Julian Day: "+str(int(JDEn*10.)/10.) + ", Gregorian Date: " + fechan
        else:
            if decisn == 0:
                msj5 = "Major Southern declination"
            else:
                msj5 = "Minor Southern declination"
            msj6 = "Julian Day: "+str(int(JDEn*10.)/10.) + ", Gregorian Date: " + fechan

        l = Moon()
        o = Observer()
        o.lat = global_lugar.lat
        o.lon = global_lugar.lon
        o.date = fechan
        o.epoch = o.date
        l.compute(o)
        try:
            o.date = l.rise_time
        except:
            o.date = o.date - 24*hour
            l.compute(o)
            o.date = l.rise_time
        l.compute(o) # Calcula caracteristicas de la Luna en la hora de su salida - horizonte ideal

################# Hace las correcciones necesarias para calcular caracteristicas lunares segun horizonte local a la salida de Luna
        iazluna = l.az * 180/np.pi   # Toma el dato del acimut del orto lunar
        deltaz = horizonte[int(iazluna)]/tan(np.pi/2 - o.lat)
        while deltaz > 0.1:
            if  o.lat >= 0.:
                iazluna2 = iazluna + 0.5*deltaz
            else:
                iazluna2 = iazluna - 0.5*deltaz
            o.horizon = horizonte[int(iazluna2)]*np.pi/180. # Encuentra para ese acimut cuan alto es el horizonte y lo incorpora a los calculos
            l.compute(o) # calcula datos lunares nuevamente a la salida en horizonte nuevo, pero buscando la hora de orto
            try:
                o.date = l.rise_time
            except:
                o.date = o.date - 24*hour
                l.compute(o)
                o.date = l.rise_time
            l.compute(o)
            iazluna = l.az * 180/np.pi
            deltaz = l.az*180/np.pi - iazluna2

        # Crea la linea de salida para el archivo, para la parada Norte
        filelinen = "                " + str(fechan) + "         "+str(int(omegan*10000)/10000.) + "            "
        filelinen = filelinen + str(int(maxdecn*1000)/1000.)+"                  N                  " + str(int(l.az*10*180/np.pi)/10.)
        o.horizon = 0.
        try:
            o.date = l.set_time
        except:
            o.date = o.date + 24*hour
            l.compute(o)
            o.date = l.set_time
        l.compute(o)
################# Hace las correcciones necesarias para calcular caracteristicas lunares segun horizonte local a la puesta de Luna
        iazluna = l.az * 180/np.pi   # Toma el dato del acimut del orto lunar
        deltaz = horizonte[int(iazluna)]/tan(np.pi/2 - o.lat)
        while deltaz > 0.1:
            if  o.lat >= 0.:
                iazluna2 = iazluna - 0.5*deltaz
            else:
                iazluna2 = iazluna + 0.5*deltaz
            o.horizon = horizonte[int(iazluna2)]*np.pi/180. # Encuentra para ese acimut cuan alto es el horizonte y lo incorpora a los calculos
            l.compute(o) # calcula datos lunares nuevamente a la salida en horizonte nuevo, pero buscando la hora de orto
            try:
                o.date = l.set_time
            except:
                o.date = o.date + 24*hour
                l.compute(o)
                o.date = l.set_time
            l.compute(o)
            iazluna = l.az * 180/np.pi
            deltaz = l.az*180/np.pi - iazluna2

        filelinen = filelinen + "                      " + str(int(l.az*10*180/np.pi)/10.)+"\n"
        msj4 = " "
        if JDEn > 1721423.5:
            if decisn == 0:
                msj5 = "Major Southern Declination"
            else:
                msj5 = "Minor Southern Declination"
            msj6 = "Julian Day: " + str(int(JDEs*10.)/10.) + ", Gregorian Date: " + fechas
        else:
            if decisn == 0:
                msj2 = "Major Northern Declination"
            else:
                msj2 = "Minor Northern Declination"
            msj3 = "Julian Day: " + str(int(JDEs*10.)/10.) + ", Gregorian Date: " + fechas

        o.date = fechas
        o.epoch = o.date
        o.horizon = 0.
        l.compute(o)
        try:
            o.date = l.rise_time
        except:
            o.date = o.date - 24*hour
            l.compute(o)
            o.date = l.rise_time
        l.compute(o)
################# Hace las correcciones necesarias para calcular caracteristicas lunares segun horizonte local (orto)
        iazluna = l.az * 180/np.pi   # Toma el dato del acimut del orto lunar
        deltaz = horizonte[int(iazluna)]/tan(np.pi/2 - o.lat)
        while deltaz > 0.1:
            if  o.lat >= 0.:
                iazluna2 = iazluna + 0.5*deltaz
            else:
                iazluna2 = iazluna - 0.5*deltaz
            o.horizon = horizonte[int(iazluna2)]*np.pi/180. # Encuentra para ese acimut cuan alto es el horizonte y lo incorpora a los calculos
            l.compute(o) # calcula datos lunares nuevamente a la salida en horizonte nuevo, pero buscando la hora de orto
            try:
                o.date = l.rise_time
            except:
                o.date = o.date - 24*hour
                l.compute(o)
                o.date = l.rise_time
            l.compute(o)
            iazluna = l.az * 180/np.pi
            deltaz = l.az*180/np.pi - iazluna2

#        print "Moon's declination (eph):", (l.dec + 0.0000001)*180./np.pi
#        print "Azimuth of rising = ", l.az
#        print "Height of eastern horizon= ", o.horizon

        # Crea la linea de salida para el archivo, para la parada Sur
        o.horizon = 0.
        try:
            o.date = l.set_time
        except:
            o.date = o.date + 24*hour
            l.compute(o)
            o.date = l.set_time
        l.compute(o)
################ Hace las correcciones necesarias para calcular caracteristicas lunares segun horizonte local (puesta)
        iazluna = l.az * 180/np.pi   # Toma el dato del acimut del orto lunar
        deltaz = horizonte[int(iazluna)]/tan(np.pi/2 - o.lat)
        while deltaz > 0.1:
            if  o.lat >= 0.:
                iazluna2 = iazluna - 0.5*deltaz
            else:
                iazluna2 = iazluna + 0.5*deltaz
            o.horizon = horizonte[int(iazluna2)]*np.pi/180. # Encuentra para ese acimut cuan alto es el horizonte y lo incorpora a los calculos
            l.compute(o) # calcula datos lunares nuevamente a la salida en horizonte nuevo, pero buscando la hora de puesta
            try:
                o.date = l.set_time
            except:
                o.date = o.date - 24*hour
                l.compute(o)
                o.date = l.set_time
            l.compute(o)
            iazluna = l.az * 180/np.pi
            deltaz = l.az*180/np.pi - iazluna2

#        print "Azimuth of setting = ", l.az
#        print "Height of western horizon= ", o.horizon

        JDEn = temporal[0]
        JDEs = temporal[2]
        maxdecn = temporal[1]
        maxdecs = temporal[3]
        fechan = self.JDEtoCAL(JDEn,0)
        fechas = self.JDEtoCAL(JDEs,0)

        self.mensaje(fig2, ax2, canvas2, msj1, msj2, msj3, msj4, msj5, msj6)

#*****************************************************************************
    def decsvenus(self):

        v = Venus()
        o = Observer()
        o.lat = global_lugar.lat
        o.lon = global_lugar.lon
        o.date = global_lugar.date
        o.epoch = o.date
        maxforton = 0.
        maxfortos = 0.
        maxfocason = 0.
        maxfocasos = 0.
        maxazorton = 90.
        maxazortos = 90.
        maxazocason = 270.
        maxazocasos = 270.
        horizonte = self.horizon(float(global_lugar.lat)*180./np.pi, float(global_lugar.long)*180./np.pi) # Calcula el horizonte local
        i = 1
        while i < 584*5:

            v.compute(o)
            try:
                o.date = v.rise_time
            except:
                o.date = o.date - 24*hour
                v.compute(o)
                o.date = v.rise_time
            v.compute(o)
################# Hace las correcciones necesarias para calcular caracteristicas venusianas segun horizonte local
            iazvenus = v.az * 180/np.pi   # Toma el dato del acimut del orto de Venus
            deltaz = horizonte[int(iazvenus)]/tan(np.pi/2 - o.lat)
            while deltaz > 0.1:
                if  o.lat >= 0.:
                    iazvenus2 = iazvenus + 0.5*deltaz
                else:
                    iazvenus2 = iazvenus - 0.5*deltaz
                o.horizon = horizonte[int(iazvenus2)]*np.pi/180. # Encuentra para ese acimut altura del horizonte e incorpora a calculos
                v.compute(o) # calcula datos venusianos nuevamente a la salida en horizonte nuevo, pero buscando la hora de orto
                try:
                    o.date = v.rise_time
                except:
                    o.date = o.date - 24*hour
                    v.compute(o)
                    o.date = v.rise_time
                v.compute(o)
                iazvenus = v.az * 180/np.pi
                deltaz = v.az*180/np.pi - iazvenus2

            if float(v.az)*180 / np.pi < maxazorton:
                maxazorton = float(v.az)*180 / np.pi
                maxforton = v.rise_time
            if float(v.az)*180 / np.pi > maxazortos:
                maxazortos = float(v.az)*180 / np.pi
                maxfortos = v.rise_time

            try:
                o.date = v.set_time
            except:
                o.date = o.date + 48*hour
                v.compute(o)
                o.date = v.set_time
            v.compute(o)
################# Hace las correcciones necesarias para calcular caracteristicas venusianas segun horizonte local
            iazvenus = v.az * 180/np.pi   # Toma el dato del acimut del orto de Venus
            deltaz = horizonte[int(iazvenus)]/tan(np.pi/2 - o.lat)
            while deltaz > 0.1:
                if  o.lat >= 0.:
                    iazvenus2 = iazvenus - 0.5*deltaz
                else:
                    iazvenus2 = iazvenus + 0.5*deltaz
                o.horizon = horizonte[int(iazvenus2)]*np.pi/180. # Encuentra para ese acimut altura del horizonte e incorpora a calculos
                v.compute(o) # calcula datos venusianos nuevamente a la salida en horizonte nuevo, pero buscando la hora de orto
                try:
                    o.date = v.set_time
                except:
                    o.date = o.date - 24*hour
                    v.compute(o)
                    o.date = v.set_time
                v.compute(o)
                iazvenus = v.az * 180/np.pi
                deltaz = v.az*180/np.pi - iazvenus2

            if float(v.az)*180 / np.pi > maxazocason:
                maxazocason = float(v.az)*180 / np.pi
                maxfocason = v.set_time
            if float(v.az)*180 / np.pi < maxazocasos:
                maxazocasos = float(v.az)*180 / np.pi
                maxfocasos = v.set_time

            o.date = o.date + 48*hour
            i += 2

        msj0 = "           EXTREME DECLINATIONS OF PLANET VENUS"
        msj1 = " "
        msj2 = "   Maximum North rising             Maximum Southern rising"
        msj3 = str(maxforton) + "    " + str(int(maxazorton*10.)/10.) + "       " +str(maxfortos) + "    " + str(int(maxazortos*10.)/10.)
        msj4 = " "
        msj5 = "   Maximum North setting            Maximum Southern setting"
        msj6 =str(maxfocason) + "    " + str(int(maxazocason*10.)/10.) + "       " +str(maxfocasos) + "    " + str(int(maxazocasos*10.)/10.)
        self.mensaje(fig2, ax2, canvas2, msj0, msj1, msj2, msj3, msj4, msj5, msj6)

#**************************************************************************
    def graficar(self, global_n_cuerpoc, fig, ax, canvas, listornot):

        global aci, diagtype, althorg
        diagtype = self.dropVar2.get()

        if listornot == 0:
            self.dropVar.set(global_n_cuerpoc)
        else:
            global_n_cuerpoc = self.dropVar.get()

        print("Cuerpo astronómico a trabajar:", global_n_cuerpoc, "\nTipo de diagrama:", diagtype)
        color_cielo = '#FFFFFF'
        color_tierra = '#BFBFBF'
        color_linea = '#808080'

        ax.clear()

        if diagtype == "Zotti Diagram":

            ax.set_axis_off()

            # Graduacion de alturas entre 0 y 90 grados
            q1=patches.Circle(xy=(0.5,0.5),radius=0.21, color = color_tierra, fill=True, fc = color_tierra)
            q2=patches.Circle(xy=(0.5,0.5),radius=0.252318, color = color_tierra, fill = False) 
            q3=patches.Circle(xy=(0.5,0.5),radius=0.293973, color = color_tierra, fill = False)
            q4=patches.Circle(xy=(0.5,0.5),radius=0.334229, color = color_tierra, fill = False)
            q5=patches.Circle(xy=(0.5,0.5),radius=0.372204, color = color_tierra, fill = False)
            q6=patches.Circle(xy=(0.5,0.5),radius=0.406787, color = color_tierra, fill = False)
            q7=patches.Circle(xy=(0.5,0.5),radius=0.436567, color = color_tierra, fill = False)
            q8=patches.Circle(xy=(0.5,0.5),radius=0.459847, color = color_tierra, fill = False)
            q9=patches.Circle(xy=(0.5,0.5),radius=0.474816, color = color_tierra, fill = False)
            q10=patches.Circle(xy=(0.5,0.5),radius=0.48, color = color_tierra, fill = True, fc = color_cielo)

            # Graduacion de alturas entre 1 y 9 grados
            q13=patches.Circle(xy=(0.5,0.5),radius=0.2142, color = color_tierra, fill = False) 
            q14=patches.Circle(xy=(0.5,0.5),radius=0.2185, color = color_tierra, fill = False)
            q15=patches.Circle(xy=(0.5,0.5),radius=0.2227, color = color_tierra, fill = False) 
            q16=patches.Circle(xy=(0.5,0.5),radius=0.2270, color = color_tierra, fill = False)
            q17=patches.Circle(xy=(0.5,0.5),radius=0.2312, color = color_tierra, fill = False)
            q18=patches.Circle(xy=(0.5,0.5),radius=0.2354, color = color_tierra, fill = False)
            q19=patches.Circle(xy=(0.5,0.5),radius=0.2397, color = color_tierra, fill = False)
            q20=patches.Circle(xy=(0.5,0.5),radius=0.2439, color = color_tierra, fill = False)
            q21=patches.Circle(xy=(0.5,0.5),radius=0.2481, color = color_tierra, fill = False)

            ax.add_patch(q10)
            ax.add_patch(q9)
            ax.add_patch(q8)
            ax.add_patch(q7)
            ax.add_patch(q6)
            ax.add_patch(q5)
            ax.add_patch(q4)
            ax.add_patch(q3)
            ax.add_patch(q2)
            ax.add_patch(q1)

            ax.add_patch(q13)
            ax.add_patch(q14)
            ax.add_patch(q15)
            ax.add_patch(q16)
            ax.add_patch(q17)
            ax.add_patch(q18)
            ax.add_patch(q19)
            ax.add_patch(q20)
            ax.add_patch(q21)

            ax.set_aspect('equal')
            ax.set_title("Zotti Diagram of the Local Horizon", fontsize='large')

                ############# TRAZA LINEAS Y VALORES DE GRADUACION DE ACIMUT EN EL AREA DEL CIELO ##################
            i = 0.0
            alin_hor = ['center','center']
            alin_ver = ['bottom', 'top']
            while i < 180.0:
                xacimutg = [0.0, 0.0]
                yacimutg = [0.0, 0.0]
                if aci < 180.0:
                    acimut2 = float(i) + 180.0
                else:
                    acimut2 = float(i) - 180.0
                xacimutg[0] = 0.5 + (sin(float(i) * np.pi / 180.0)*(0.21+0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                yacimutg[0] = 0.5 + (cos(float(i) * np.pi / 180.0)*(0.21+0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                xacimutg[1] = 0.5 + (sin(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                yacimutg[1] = 0.5 + (cos(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                line, = ax.plot(xacimutg, yacimutg, lw = 1, color = color_tierra , zorder = 1)

                ################ ESCRIBE LA ROTULACION DEL GRAFICO MOSTRADO ####################
                ####################### EMPIEZA CON ACIMUT Y ALTURAS ########################
                if (i / 10.0) % 2 == 0:
                    alin_vert = 0.71 + (0.27 * acos((cos(i * np.pi / 360.))**2) / (np.pi / 2))
                    ax.text(0.5, alin_vert, int(i/2.),
                    horizontalalignment = 'left',
                    verticalalignment = 'center',
                    fontsize = 6, color = color_linea,
                    transform = ax.transAxes)
    
                    alin_vert = 0.29 - (0.27 * acos((cos(i * np.pi / 360.))**2) / (np.pi / 2))
                    ax.text(0.5, alin_vert, int(i/2.),
                    horizontalalignment = 'right',
                    verticalalignment = 'center',
                    fontsize = 6, color = color_linea,
                    transform = ax.transAxes)

                ax.text(xacimutg[0],yacimutg[0], int(i),
                horizontalalignment = alin_hor[0],
                verticalalignment = alin_ver[0],
                fontsize = 8, color = color_linea,
                transform = ax.transAxes)

                ax.text(xacimutg[1],yacimutg[1], int(i+180),
                horizontalalignment = alin_hor[1],
                verticalalignment = alin_ver[1],
                fontsize = 8, color = color_linea,
                transform = ax.transAxes)

                if i == 0.0:
                    alin_hor = ['left', 'right']
                    alin_ver = ['center', 'center']

                i += 10.0

                ################ LABELS CARDINAL POINTS ON GRAPH #######################
            ax.text(0.5,0.71, 'N',
                horizontalalignment='center',
                verticalalignment='top',
                fontsize=12, color='black',
                transform=ax.transAxes)
            ax.text(0.5,0.29, 'S',
                horizontalalignment='center',
                verticalalignment='bottom',
                fontsize=12, color='black',
                transform=ax.transAxes)
            ax.text(0.71,0.48, 'E',
                horizontalalignment='right',
                verticalalignment='bottom',
                fontsize=12, color='black',
                transform=ax.transAxes)
            ax.text(0.29,0.48, 'W',
                horizontalalignment='left',
                verticalalignment='bottom',
                fontsize=12, color='black',
                transform=ax.transAxes)

            line, = ax.plot([0.5], [0.5]) # empty line

        else:

            ax.set_aspect(15-int(althorg*4/9))
            lim_inf_x=0.
            lim_sup_x=360.
            lim_inf_y=0.
            lim_sup_y=althorg
            ax.axis([lim_inf_x, lim_sup_x, lim_inf_y, lim_sup_y])
            ax.minorticks_off()            
            ax.grid(True, which = 'major')
            ax.xaxis.set_major_locator(ticker.FixedLocator([0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360]))
            ax.minorticks_on()
            ax.grid(True, which = 'minor', alpha=0.2)
            ax.set_xlabel("Azimuth (Degrees)")
            ax.set_ylabel("Height above astronomical horizon (Degrees)", fontsize = 'small')
            ax.set_title("Cartesian Diagram of the Local Horizon", fontsize='large')

#####################################################################################################

        horizonte = self.horizon(float(global_lugar.lat)*180./np.pi, float(global_lugar.long)*180./np.pi) # Computes local horizon

        alt_c_aci = 0
        flag = True

        # Calls and assigns the corresponding function for the astronomical body
        if global_n_cuerpoc == "Sun":
            cuerpoc = Sun()

        if global_n_cuerpoc == "Moon":
            cuerpoc = Moon()

        if global_n_cuerpoc == "Venus":
            cuerpoc = Venus()

        if global_n_cuerpoc == "Antares":
            cuerpoc = star('Antares')

        if global_n_cuerpoc == "Aldebaran":
            cuerpoc = star('Aldebaran')

        if global_n_cuerpoc == "Pleyades":
            cuerpoc = star('Alcyone')

        if global_n_cuerpoc == "Capella":
            cuerpoc = star('Capella')

        if global_n_cuerpoc == "Sirius":
            cuerpoc = star('Sirius')

        if global_n_cuerpoc == "Arcturus":
            cuerpoc = star('Arcturus')

        if global_n_cuerpoc == "Fomalhaut":
            cuerpoc = star('Fomalhaut')

        if global_n_cuerpoc == "Jupiter":
            cuerpoc = Jupiter()

        if global_n_cuerpoc == "Mars":
            cuerpoc = Mars()

        try:
            cuerpoc.compute(global_lugar)   # Calcula efemérides del Cuerpo celeste para el lugar
                                            # del observador y fecha/hora/época seleccionadas
        except:
            global_n_cuerpoc = "Sun"
            cuerpoc = Sun()
            cuerpoc.compute(global_lugar)

        a = 0.04                          # Intervalo de tiempo entre puntos a graficar (minutos)
        k_cuerpoc_sale=cuerpoc.rise_time        # Define como inicio de los cálculos para el cuerpo astronomico,
        k_cuerpoc_puesta=cuerpoc.set_time       # la hora de su salida, en la fecha del dí­a seleccionado y asigna
                                                # horas de salida y puesta a constantes

        if not(k_cuerpoc_sale):     # Correcciones para cuando no hay salida de Cuerpo celeste
            vp=global_lugar
            vp.date-=hour*24
            cuerpoc.compute(vp)
            k_cuerpoc_sale=cuerpoc.rise_time
            vp.date+=hour*24

        if not(k_cuerpoc_puesta):  # Correcciones para cuando no hay puesta de Cuerpo celeste
            vp = global_lugar
            vp.date += hour*24
            cuerpoc.compute(vp)
            k_cuerpoc_puesta = cuerpoc.set_time
            vp.date -= hour*24

        if not(k_cuerpoc_sale):
            k_cuerpoc_sale = global_lugar.date
            k_cuerpoc_puesta = global_lugar.date
            print("wrong execution")
        else:
            global_lugar.date = date(k_cuerpoc_sale)

        vp = global_lugar
        k_pi = 3.141592654

        if k_cuerpoc_puesta<k_cuerpoc_sale:  # Corrección para puesta del Cuerpo celeste ANTES de la salida
            vp.date += hour*24
            cuerpoc.compute(vp)
            k_cuerpoc_puesta = cuerpoc.set_time
            vp.date -= hour*24

        lugarc = Observer()
        lugarc.long, lugarc.lat = global_lugar.long, global_lugar.lat
        lugarc.date, lugarc.epoch = k_cuerpoc_sale, global_lugar.epoch
        iteracion = 0

        intervalo_cuerpoc = 1/(1 + (k_cuerpoc_puesta - k_cuerpoc_sale)/(minute*a)) # Quantity of intervals to use

        if k_cuerpoc_sale==k_cuerpoc_puesta:
            print("No trace can be made for ",global_n_cuerpoc)
            print(k_cuerpoc_sale, k_cuerpoc_puesta)

        rotulo_cuerpoc=int((1/intervalo_cuerpoc)*3/4)   # Prepara variables con Numero de elementos del arreglo
                                                        # que se usará para colocar rotulador de cada objeto
        xcuerpoc=np.arange(0,1,intervalo_cuerpoc) # Crea los arreglos donde se guardarán las coordenadas que sigue
        ycuerpoc=np.arange(0,1,intervalo_cuerpoc) # el cuerpo celeste, según la cantidad de intervalos requeridos,

        ################### COMPUTATIONS FOR THE CELESTIAL BODY ####################
        while lugarc.date <= k_cuerpoc_puesta:
            cuerpoc.compute(lugarc)

            if abs((cuerpoc.az*180./np.pi) - aci) <= 0.075 and (cuerpoc.alt*180./np.pi) < 50. and flag:
                #print cuerpoc.az, cuerpoc.alt, aci
                alt_c_aci = cuerpoc.alt*180./np.pi
                flag = False

            if int(cuerpoc.alt*180./np.pi) < horizonte[int(cuerpoc.az*180./np.pi)] and cuerpoc.az < np.pi:
                hora_sale = lugarc.date
                alt_sale = cuerpoc.alt
                az_sale = cuerpoc.az
            elif horizonte[int(cuerpoc.az*180./np.pi)] == 0 and iteracion == 0:
                hora_sale = lugarc.date
                alt_sale = cuerpoc.alt
                az_sale = cuerpoc.az               

            if int(cuerpoc.alt*180./np.pi) > horizonte[int(cuerpoc.az*180./np.pi)] and cuerpoc.az > np.pi:
                hora_puesta = lugarc.date
                alt_puesta = cuerpoc.alt
                az_puesta = cuerpoc.az

            if diagtype == "Zotti Diagram":
                xcuerpoc[iteracion] = 0.5 + (sin(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2)))
                ycuerpoc[iteracion] = 0.5 + (cos(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2)))
            else:
                xcuerpoc[iteracion] = cuerpoc.az * 180 / np.pi
                ycuerpoc[iteracion] = cuerpoc.alt * 180 / np.pi
            lugarc.date += a / (24 * 60)
            iteracion += 1

        try: # Corrección para que el último punto a graficar no salga fuera del Histograma
            if diagtype == "Zotti Diagram":
                xcuerpoc[iteracion] = 0.5 + (sin(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2))) 
                ycuerpoc[iteracion] = 0.5 + (cos(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2)))
            else:
                xcuerpoc[iteracion] = cuerpoc.az
                ycuerpoc[iteracion] = cuerpoc.alt
        except:
            print("No correction could be made for the last point to graph")

        print(" ")
        print("Epoch:", lugarc.epoch)
        print("Rising of "+global_n_cuerpoc)
        print(iteracion, hora_sale, alt_sale, az_sale) # Writes info on rise time)
        print(" ")
        print("Setting of "+global_n_cuerpoc)
        print(iteracion, hora_puesta, alt_puesta, az_puesta) # Writes info on setting time)
        print(" ")

        print(global_n_cuerpoc+" culminates at: "+str(lugarc.previous_transit(cuerpoc))+" (UT)") # Imprime datos en el meridiano
        x_rotulo_cuerpoc = xcuerpoc[rotulo_cuerpoc]
        y_rotulo_cuerpoc = ycuerpoc[rotulo_cuerpoc]
                ####################### END OF CALCULATIONS FOR THE CELESTIAL BODY #########################

                ############### CALCULATIONS FOR THE AZIMUTHAL LINE THAT THE USER DEFINES #################

        acimut2 = 0.0
        xacimut = [0.0, 0.0]
        yacimut = [0.0, 0.0]
        if aci < 180.0:
            acimut2 = float(aci) + 180.0
        else:
            acimut2 = float(aci) - 180.0

        if diagtype == "Zotti Diagram":
            xacimut[0] = 0.5 + (sin(float(aci) * np.pi / 180.0)*(0.21+0.27*acos((cos(0.349066))**2)/(np.pi/2)))
            yacimut[0] = 0.5 + (cos(float(aci) * np.pi / 180.0)*(0.21+0.27*acos((cos(0.349066))**2)/(np.pi/2)))
            xacimut[1] = 0.5 + (sin(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(0.349066))**2)/(np.pi/2)))
            yacimut[1] = 0.5 + (cos(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(0.349066))**2)/(np.pi/2)))

                ##################### ENDS CALCULATIONS FOR THE USER DEFINED AZIMUTH ####################################

        else:
            xacimut[0] = aci
            yacimut[0] = 0
            xacimut[1] = aci
            yacimut[1] = 10

        line, = ax.plot(xacimut, yacimut, lw = 2, color = color_linea, zorder = 3) # Draws azimuthal line on the diagram

        th = 0.
        xhor = []
        yhor = []

        while th < 360.:
            if diagtype == "Zotti Diagram":
                xhor.append(0.5 + sin(th * np.pi / 180.0)*(0.21 + 0.27*acos((cos(horizonte[int(th)] * np.pi / 180.0))**2)/(np.pi/2)))
                yhor.append(0.5 + cos(th * np.pi / 180.0)*(0.21 + 0.27*acos((cos(horizonte[int(th)] * np.pi / 180.0))**2)/(np.pi/2)))
            else:
                xhor.append(th)
                yhor.append(horizonte[int(th)])
            th += 1.
 
        line, = ax.plot(xcuerpoc, ycuerpoc, lw = 1, color = color_linea, zorder = 1) # Draws track of the celestial body on diagram
        line, = ax.plot(xhor, yhor, lw = 1, color = color_linea, zorder = 3) # Draws the local horizon on diagram

                ############ LABELS DATA OF THE OBSERVED CELESTIAL OBJECT #######################

        # Setting coordinates for labels on each diagram type
        if diagtype == "Zotti Diagram":
            name_object_label = [xcuerpoc[rotulo_cuerpoc],ycuerpoc[rotulo_cuerpoc]]
            evaluated_azimuth_label = [-0.2,1.0]
            height_azimuth_label = [-0.2,0.98]
            alt_c_aci_label0 = [-0.2,0.96]
            alt_c_aci_label1 = [-0.2,0.94]
            mer_cross_label = [-0.2, 0.92]
            rise_time_label = [-0.2, 0.90]
            set_time_label = [-0.2, 0.88]
            max_height_ah_label = [-0.2, 0.86]
            coords_label = [-0.2,0.84]
            aci_label = [0.5,0.5]

        else:
            name_object_label = [0.55,0.6]
            evaluated_azimuth_label = [0.,-0.48]
            height_azimuth_label = [0,-0.54]
            max_height_ah_label = [0.,-0.36]
            set_time_label = [0.,-0.42]
            mer_cross_label = [0.,-0.30]
            rise_time_label = [0.,-0.24]
            coords_label = [0.,-0.18]
            aci_label = [aci/360.,0.55]
            alt_c_aci_label0 = [0,-0.6]
            alt_c_aci_label1 = [0,-0.66]

        # Labels that serve as legends to the graph
        ax.text(evaluated_azimuth_label[0],evaluated_azimuth_label[1], 'Evaluated Azimuth:' + str(aci),
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(height_azimuth_label[0],height_azimuth_label[1],"Height of Horizon at azimuth "+str(aci)+" : " + str(int(horizonte[int(aci+0.5)]*1000.)/1000.),
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(max_height_ah_label[0],max_height_ah_label[1], 'Max. height above horizon: '+str(cuerpoc.alt),
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color = 'black',
            transform = ax.transAxes)
        ax.text(set_time_label[0],set_time_label[1], 'Setting at: '+str(hora_puesta)+' (UT)',
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=7.5, color='black',
            transform=ax.transAxes)
        ax.text(coords_label[0],coords_label[1], 'Lat:'+str(global_lugar.lat)+', Lon:'+str(global_lugar.long),
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color = 'black',
            transform = ax.transAxes)
        ax.text(alt_c_aci_label0[0],alt_c_aci_label0[1],"Height of "+global_n_cuerpoc+" at azimuth "+str(aci)+" : " + str(int(alt_c_aci*1000.)/1000.)+"*",
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(alt_c_aci_label1[0],alt_c_aci_label1[1],"* Height shown only when "+global_n_cuerpoc+"\'s altitude lower than 50 degrees",
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)

        # Labels that are inside the graph
        ax.text(name_object_label[0],name_object_label[1], global_n_cuerpoc,
            horizontalalignment='right',
            verticalalignment='bottom',
            fontsize=12, color='black' ,
            transform=ax.transAxes)
        lugarc.date = k_cuerpoc_sale
        ax.text(mer_cross_label[0],mer_cross_label[1], 'Meridian crossing: '+str(lugarc.next_transit(cuerpoc))+"(UT)",
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=7.5, color='black',
            transform=ax.transAxes)
        ax.text(rise_time_label[0],rise_time_label[1], 'Rising at: '+str(hora_sale)+' (UT)',
            horizontalalignment='left',
            verticalalignment='top',
            fontsize=7.5, color='black',
            transform=ax.transAxes)
        ax.text(aci_label[0],aci_label[1], str(aci),
            horizontalalignment = 'center',
            verticalalignment = 'top',
            fontsize = 7.5, color = color_linea,
            transform = ax.transAxes)

        canvas.draw()

#*******************************************-------------------------------------------------------------------------------------------------
    def graficar2(self, global_n_cuerpoc, fig, ax, canvas, listornot):

        global aci, diagtype
        diagtype = self.dropVar2.get()
        print("******************\nAcimut de evaluacion al inicio de grafica", aci)

        if listornot == 0:
            self.dropVar.set(global_n_cuerpoc)
        else:
            global_n_cuerpoc = self.dropVar.get()

        print("Cuerpo astronómico a trabajar:", global_n_cuerpoc, "\nTipo de diagrama:", diagtype)
        color_cielo = '#FFFFFF'
        color_tierra = '#BFBFBF'
        color_linea = '#808080'
        color_linea_WS = '#00008B'
        color_linea_SS = '#8B0000'
        color_linea_eqnx = '#FF8C00'

        ax.clear()

        if diagtype == "Zotti Diagram":

            ax.set_axis_off()

            # Graduacion de alturas entre 0 y 90 grados
            q1=patches.Circle(xy=(0.5,0.5),radius=0.21, color = color_tierra, fill=True, fc = color_tierra)
            q2=patches.Circle(xy=(0.5,0.5),radius=0.252318, color = color_tierra, fill = False) 
            q3=patches.Circle(xy=(0.5,0.5),radius=0.293973, color = color_tierra, fill = False)
            q4=patches.Circle(xy=(0.5,0.5),radius=0.334229, color = color_tierra, fill = False)
            q5=patches.Circle(xy=(0.5,0.5),radius=0.372204, color = color_tierra, fill = False)
            q6=patches.Circle(xy=(0.5,0.5),radius=0.406787, color = color_tierra, fill = False)
            q7=patches.Circle(xy=(0.5,0.5),radius=0.436567, color = color_tierra, fill = False)
            q8=patches.Circle(xy=(0.5,0.5),radius=0.459847, color = color_tierra, fill = False)
            q9=patches.Circle(xy=(0.5,0.5),radius=0.474816, color = color_tierra, fill = False)
            q10=patches.Circle(xy=(0.5,0.5),radius=0.48, color = color_tierra, fill = True, fc = color_cielo)

            # Graduacion de alturas entre 1 y 9 grados
            q13=patches.Circle(xy=(0.5,0.5),radius=0.2142, color = color_tierra, fill = False) 
            q14=patches.Circle(xy=(0.5,0.5),radius=0.2185, color = color_tierra, fill = False)
            q15=patches.Circle(xy=(0.5,0.5),radius=0.2227, color = color_tierra, fill = False) 
            q16=patches.Circle(xy=(0.5,0.5),radius=0.2270, color = color_tierra, fill = False)
            q17=patches.Circle(xy=(0.5,0.5),radius=0.2312, color = color_tierra, fill = False)
            q18=patches.Circle(xy=(0.5,0.5),radius=0.2354, color = color_tierra, fill = False)
            q19=patches.Circle(xy=(0.5,0.5),radius=0.2397, color = color_tierra, fill = False)
            q20=patches.Circle(xy=(0.5,0.5),radius=0.2439, color = color_tierra, fill = False)
            q21=patches.Circle(xy=(0.5,0.5),radius=0.2481, color = color_tierra, fill = False)

            ax.add_patch(q10)
            ax.add_patch(q9)
            ax.add_patch(q8)
            ax.add_patch(q7)
            ax.add_patch(q6)
            ax.add_patch(q5)
            ax.add_patch(q4)
            ax.add_patch(q3)
            ax.add_patch(q2)
            ax.add_patch(q1)

            ax.add_patch(q13)
            ax.add_patch(q14)
            ax.add_patch(q15)
            ax.add_patch(q16)
            ax.add_patch(q17)
            ax.add_patch(q18)
            ax.add_patch(q19)
            ax.add_patch(q20)
            ax.add_patch(q21)

            ax.set_aspect('equal')
            ax.set_title("Zotti Diagram of the Local Horizon", fontsize='large')

                ############# TRAZA LINEAS Y VALORES DE GRADUACION DE ACIMUT EN EL AREA DEL CIELO ##################
            i = 0.0
            alin_hor = ['center','center']
            alin_ver = ['bottom', 'top']
            while i < 180.0:
                xacimutg = [0.0, 0.0]
                yacimutg = [0.0, 0.0]
                if aci < 180.0:
                    acimut2 = float(i) + 180.0
                else:
                    acimut2 = float(i) - 180.0
                xacimutg[0] = 0.5 + (sin(float(i) * np.pi / 180.0)*(0.21+0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                yacimutg[0] = 0.5 + (cos(float(i) * np.pi / 180.0)*(0.21+0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                xacimutg[1] = 0.5 + (sin(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                yacimutg[1] = 0.5 + (cos(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(1.5708))**2)/(np.pi/2)))
                line, = ax.plot(xacimutg, yacimutg, lw = 1, color = color_tierra , zorder = 1)

                ################ ESCRIBE LA ROTULACION DEL GRAFICO MOSTRADO ####################
                ####################### EMPIEZA CON ACIMUT Y ALTURAS ########################
                if (i / 10.0) % 2 == 0:
                    alin_vert = 0.71 + (0.27 * acos((cos(i * np.pi / 360.))**2) / (np.pi / 2))
                    ax.text(0.5, alin_vert, int(i/2.),
                    horizontalalignment = 'left',
                    verticalalignment = 'center',
                    fontsize = 6, color = color_linea,
                    transform = ax.transAxes)
    
                    alin_vert = 0.29 - (0.27 * acos((cos(i * np.pi / 360.))**2) / (np.pi / 2))
                    ax.text(0.5, alin_vert, int(i/2.),
                    horizontalalignment = 'right',
                    verticalalignment = 'center',
                    fontsize = 6, color = color_linea,
                    transform = ax.transAxes)

                ax.text(xacimutg[0],yacimutg[0], int(i),
                horizontalalignment = alin_hor[0],
                verticalalignment = alin_ver[0],
                fontsize = 8, color = color_linea,
                transform = ax.transAxes)

                ax.text(xacimutg[1],yacimutg[1], int(i+180),
                horizontalalignment = alin_hor[1],
                verticalalignment = alin_ver[1],
                fontsize = 8, color = color_linea,
                transform = ax.transAxes)

                if i == 0.0:
                    alin_hor = ['left', 'right']
                    alin_ver = ['center', 'center']

                i += 10.0

                ################ LABELS CARDINAL POINTS ON GRAPH #######################
            ax.text(0.5,0.71, 'N',
                horizontalalignment='center',
                verticalalignment='top',
                fontsize=12, color='black',
                transform=ax.transAxes)
            ax.text(0.5,0.29, 'S',
                horizontalalignment='center',
                verticalalignment='bottom',
                fontsize=12, color='black',
                transform=ax.transAxes)
            ax.text(0.71,0.48, 'E',
                horizontalalignment='right',
                verticalalignment='bottom',
                fontsize=12, color='black',
                transform=ax.transAxes)
            ax.text(0.29,0.48, 'W',
                horizontalalignment='left',
                verticalalignment='bottom',
                fontsize=12, color='black',
                transform=ax.transAxes)

            line, = ax.plot([0.5], [0.5]) # empty line

        else:

            ax.set_aspect(4)
            lim_inf_x=0.
            lim_sup_x=360.
            lim_inf_y=0.
            lim_sup_y=25.0
            ax.axis([lim_inf_x, lim_sup_x, lim_inf_y, lim_sup_y])
            ax.minorticks_off()            
            ax.grid(True, which = 'major', alpha=0.5, ls=":")
            ax.xaxis.set_major_locator(ticker.FixedLocator([0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360]))
            ax.minorticks_on()
            ax.grid(True, which = 'minor', alpha=0.2, ls=":")
            ax.set_xlabel("Azimuth (Degrees)")
            ax.set_ylabel("Height above astronomical horizon (Degrees)", fontsize = 'small')
            ax.set_title("Cartesian Diagram of the Local Horizon", fontsize='large')

#####################################################################################################

        horizonte = self.horizon(float(global_lugar.lat)*180./np.pi, float(global_lugar.long)*180./np.pi) # Computes local horizon

        contadorp = 0
        xcuerpoc = []
        ycuerpoc = []
        x_rotulo_cuerpoc=[]
        y_rotulo_cuerpoc=[]
        alt_c_aci = []
        o = Observer()
        o = global_lugar
        cuerpoc = Sun() # This is the variable that will handle the sun object

        while contadorp < 3:

            flag = True

            if contadorp == 0:
                o.date = previous_solstice(global_lugar.date)
                fechadet = str(o.date)
                i = 0
                Y = ""
                while fechadet[i] != "/":
                    Y = Y + fechadet[i]
                    i += 1
                i += 1
                M = ""
                while fechadet[i] != "/":
                    M = M + fechadet[i]
                    i += 1
                i += 1
                D = ""
                while fechadet[i] != " ":
                    D = D + fechadet[i]
                    i += 1
    
                ys0, ms0, ds0 = int(float(Y)), int(float(M)), int(float(D))

            elif contadorp == 1:
                o.date = next_solstice(global_lugar.date+24.*hour)
                fechadet = str(o.date)
                i = 0
                Y = ""
                while fechadet[i] != "/":
                    Y = Y + fechadet[i]
                    i += 1
                i += 1
                M = ""
                while fechadet[i] != "/":
                    M = M + fechadet[i]
                    i += 1
                i += 1
                D = ""
                while fechadet[i] != " ":
                    D = D + fechadet[i]
                    i += 1
    
                ys1, ms1, ds1 = int(float(Y)), int(float(M)), int(float(D))
                #print ys1, ms1, ds1
                if ms1 == 12 or ms1 == 1 or ms1 == 2:
                    solstice0 = "Summer "
                    solstice1 = "Winter "
                    color_linea_solst0 = color_linea_SS
                    color_linea_solst1 = color_linea_WS
                elif ms1 == 6 or ms1 == 7 or ms1 == 8:
                    solstice0 = "Winter "
                    solstice1 = "Summer "
                    color_linea_solst0 = color_linea_WS
                    color_linea_solst1 = color_linea_SS

            elif contadorp == 2:
                o.date = previous_equinox(global_lugar.date)
                fechadet = str(o.date)
                i = 0
                Y = ""
                while fechadet[i] != "/":
                    Y = Y + fechadet[i]
                    i += 1
                i += 1
                M = ""
                while fechadet[i] != "/":
                    M = M + fechadet[i]
                    i += 1
                i += 1
                D = ""
                while fechadet[i] != " ":
                    D = D + fechadet[i]
                    i += 1
    
                yeq, meq, deq = int(float(Y)), int(float(M)), int(float(D))


            cuerpoc.compute(o)   # Calcula efemérides del Cuerpo celeste para el lugar
                                        
            a = 0.04                          # Intervalo de tiempo entre puntos a graficar (minutos)
            k_cuerpoc_sale=cuerpoc.rise_time        # Define como inicio de los cálculos para el cuerpo astronomico,
            k_cuerpoc_puesta=cuerpoc.set_time       # la hora de su salida, en la fecha del dí­a seleccionado y asigna
                                                # horas de salida y puesta a constantes
            if not(k_cuerpoc_sale):     # Corrections when there is not a rising for the body
                vp=o
                vp.date-=hour*24
                cuerpoc.compute(vp)
                k_cuerpoc_sale=cuerpoc.rise_time
                vp.date+=hour*24

            if not(k_cuerpoc_puesta):  # Corrections when there is not a setting for the body
                vp = o
                vp.date += hour*24
                cuerpoc.compute(vp)
                k_cuerpoc_puesta = cuerpoc.set_time
                vp.date -= hour*24

            if not(k_cuerpoc_sale):
                k_cuerpoc_sale = global_lugar.date
                k_cuerpoc_puesta = global_lugar.date
                print("wrong execution")
            else:
                global_lugar.date = date(k_cuerpoc_sale)

            vp = global_lugar
            k_pi = 3.141592654

            if k_cuerpoc_puesta<k_cuerpoc_sale:  # Correction if body's setting is BEFORE rising
                vp.date += hour*24
                cuerpoc.compute(vp)
                k_cuerpoc_puesta = cuerpoc.set_time
                vp.date -= hour*24

            lugarc = Observer()
            lugarc.long, lugarc.lat = global_lugar.long, global_lugar.lat
            lugarc.date, lugarc.epoch = k_cuerpoc_sale, global_lugar.epoch
            iteracion = 0

            intervalo_cuerpoc = 1/(1 + (k_cuerpoc_puesta - k_cuerpoc_sale)/(minute*a)) # Quantity of intervals to use

            if k_cuerpoc_sale==k_cuerpoc_puesta:
                print("No trace can be made for ",global_n_cuerpoc)
                ( k_cuerpoc_sale, k_cuerpoc_puesta)

            rotulo_cuerpoc=int((1/intervalo_cuerpoc)*3/4)   # Prepara variables con Numero de elementos del arreglo
                                                        # que se usará para colocar rotulador de cada objeto
            xcuerpoc.append(np.arange(0,1,intervalo_cuerpoc)) # Crea los arreglos donde se guardarán las coordenadas que sigue
            ycuerpoc.append(np.arange(0,1,intervalo_cuerpoc)) # el cuerpo celeste, según la cantidad de intervalos requeridos,

        ################### COMPUTATIONS FOR THE CELESTIAL BODY ####################

            while lugarc.date <= k_cuerpoc_puesta:
                cuerpoc.compute(lugarc)
                if abs((cuerpoc.az*180./np.pi) - aci) <= 0.0075 and (cuerpoc.alt*180./np.pi) <= 50. and flag:
                    #print cuerpoc.az, cuerpoc.alt, aci
                    alt_c_aci.append(cuerpoc.alt*180./np.pi)
                    flag = False

                if int(cuerpoc.alt*180./np.pi) < horizonte[int(cuerpoc.az*180/np.pi)] and cuerpoc.az < np.pi:
                    hora_sale = lugarc.date
                    alt_sale = cuerpoc.alt
                    az_sale = cuerpoc.az
                    if contadorp == 0:
                        azrise0 = cuerpoc.az
                    elif contadorp == 1:
                        azrise1 = cuerpoc.az
                    else:
                        azrise2 = cuerpoc.az

                elif horizonte[int(cuerpoc.az*180/np.pi)] == 0 and iteracion == 0:
                    hora_sale = lugarc.date
                    alt_sale = cuerpoc.alt
                    az_sale = cuerpoc.az
                    if contadorp == 0:
                        azrise0 = cuerpoc.az
                    elif contadorp == 1:
                        azrise1 = cuerpoc.az
                    else:
                        azrise2 = cuerpoc.az

                if int(cuerpoc.alt*180./np.pi) > horizonte[int(cuerpoc.az*180/np.pi)] and cuerpoc.az > np.pi:
                    hora_puesta = lugarc.date
                    alt_puesta = cuerpoc.alt
                    az_puesta = cuerpoc.az

                if diagtype == "Zotti Diagram":
                    xcuerpoc[contadorp][iteracion] = 0.5 + (sin(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2)))
                    ycuerpoc[contadorp][iteracion] = 0.5 + (cos(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2)))
                else:
                    xcuerpoc[contadorp][iteracion] = cuerpoc.az * 180 / np.pi
                    ycuerpoc[contadorp][iteracion] = cuerpoc.alt * 180 / np.pi
                lugarc.date += a / (24 * 60)
                iteracion += 1

            if flag:
                alt_c_aci.append(0)
                print("Body's height in Azimuth was adjusted to 0 in position", contadorp)

            try: # Corrección para que el último punto a graficar no salga fuera del Histograma
                if diagtype == "Zotti Diagram":
                    xcuerpoc[contadorp][iteracion] = 0.5 + (sin(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2))) 
                    ycuerpoc[contadorp][iteracion] = 0.5 + (cos(cuerpoc.az)*(0.21+0.27*acos((cos(cuerpoc.alt))**2)/(np.pi/2)))
                else:
                    xcuerpoc[contadorp][iteracion] = cuerpoc.az
                    ycuerpoc[contadorp][iteracion] = cuerpoc.alt
            except:
                print("No correction could be made for the last point to graph")

            contadorp += 1
#                                       =======             =======
#                                     //   ##  \\         //   ##  \\
#                                     ||   ##   ||        ||   ##   ||
#                                     \\       //         \\       //
#                                       =======             =======

                ####################### END OF CALCULATIONS FOR THE CELESTIAL BODY #########################

                ############### CALCULATIONS FOR THE AZIMUTHAL LINE THAT THE USER DEFINES #################

        acimut2 = 0.0
        xacimut = [0.0, 0.0]
        yacimut = [0.0, 0.0]
        if aci < 180.0:
            acimut2 = float(aci) + 180.0
        else:
            acimut2 = float(aci) - 180.0

        if diagtype == "Zotti Diagram":
            xacimut[0] = 0.5 + (sin(float(aci) * np.pi / 180.0)*(0.21+0.27*acos((cos(0.349066))**2)/(np.pi/2)))
            yacimut[0] = 0.5 + (cos(float(aci) * np.pi / 180.0)*(0.21+0.27*acos((cos(0.349066))**2)/(np.pi/2)))
            xacimut[1] = 0.5 + (sin(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(0.349066))**2)/(np.pi/2)))
            yacimut[1] = 0.5 + (cos(acimut2*np.pi/180.0) * (0.21 + 0.27*acos((cos(0.349066))**2)/(np.pi/2)))
        else:
            xacimut[0] = aci
            yacimut[0] = 0
            xacimut[1] = aci
            yacimut[1] = 10

                ##################### ENDS CALCULATIONS FOR THE USER DEFINED AZIMUTH ####################################

        line, = ax.plot(xacimut, yacimut, lw = 1, color = color_linea, zorder = 3) # Draws azimuthal line on the diagram

        th = 0.
        xhor = []
        yhor = []

        while th < 360.:
            if diagtype == "Zotti Diagram":
                xhor.append(0.5 + sin(th * np.pi / 180.0)*(0.21 + 0.27*acos((cos(horizonte[int(th)] * np.pi / 180.0))**2)/(np.pi/2)))
                yhor.append(0.5 + cos(th * np.pi / 180.0)*(0.21 + 0.27*acos((cos(horizonte[int(th)] * np.pi / 180.0))**2)/(np.pi/2)))
            else:
                xhor.append(th)
                yhor.append(horizonte[int(th)])
            th += 1.
 
        line, = ax.plot(xcuerpoc[0], ycuerpoc[0], lw = 1, color = color_linea_solst0, zorder = 2) # Draws track of Sun on last solstice
        line, = ax.plot(xcuerpoc[1], ycuerpoc[1], lw = 1, color = color_linea_solst1, zorder = 2) # Draws track of Sun on next solstice
        line, = ax.plot(xcuerpoc[2], ycuerpoc[2], '--', lw = 1, color = color_linea_eqnx, zorder = 2) # Draws track of Sun on equinox
        line, = ax.plot(xhor, yhor, lw = 1, color = color_linea, zorder = 3) # Draws the local horizon on diagram

                ############ LABELS DATA OF THE OBSERVED CELESTIAL OBJECT #######################


        if diagtype == "Zotti Diagram":
            name_object_label0 = [xcuerpoc[0][rotulo_cuerpoc],ycuerpoc[0][rotulo_cuerpoc]]
            name_object_label1 = [xcuerpoc[1][rotulo_cuerpoc],ycuerpoc[1][rotulo_cuerpoc]]
            name_object_label2 = [xcuerpoc[2][rotulo_cuerpoc],ycuerpoc[2][rotulo_cuerpoc]]
            evaluated_azimuth_label = [-0.2,1.0]
            height_azimuth_label = [-0.2,0.96]
            alt_c_aci_label0 = [-0.2,0.94]
            alt_c_aci_label1 = [-0.2,0.92]
            alt_c_aci_label2 = [-0.2,0.90]
            alt_c_aci_label3 = [-0.2,0.88]
            coords_label = [-0.2,0.86]
            aci_label = [0.5,0.5]
        else:
            name_object_label0 = [azrise0/(2*np.pi),0.7]
            name_object_label1 = [azrise1/(2*np.pi),0.5]
            name_object_label2 = [azrise2/(2*np.pi),0.6]
            evaluated_azimuth_label = [0.,-0.18]
            height_azimuth_label = [0,-0.54]
            coords_label = [0.,-0.26]
            aci_label = [aci/360.,0.45]
            alt_c_aci_label0 = [0,-0.60]
            alt_c_aci_label1 = [0,-0.66]
            alt_c_aci_label2 = [0,-0.72]
            alt_c_aci_label3 = [0,-0.78]

        # Setting coordinates for labels on each diagram type
        # Labels inside the graph
        ax.text(name_object_label0[0],name_object_label0[1], solstice0+"Solstice",
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=9, color='black' ,
            transform=ax.transAxes)
        ax.text(name_object_label1[0],name_object_label1[1], solstice1+"Solstice",
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=9, color='black' ,
            transform=ax.transAxes)
        ax.text(name_object_label2[0],name_object_label2[1], "Equinoxes",
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=9, color='black' ,
            transform=ax.transAxes)
        ax.text(aci_label[0],aci_label[1], str(aci),
            horizontalalignment = 'center',
            verticalalignment = 'top',
            fontsize = 7.5, color = color_linea,
            transform = ax.transAxes)

        # Labels that serve as legends to the graph
        ax.text(evaluated_azimuth_label[0],evaluated_azimuth_label[1], 'Solar Phenomena: Equinoxes and Solstices',
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 10, color='black',
            transform = ax.transAxes)

        ax.text(coords_label[0],coords_label[1], 'Lat:'+str(global_lugar.lat)+', Lon:'+str(global_lugar.long),
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 8, color = 'black',
            transform = ax.transAxes)
        ax.text(height_azimuth_label[0],height_azimuth_label[1],"Height of Horizon at azimuth "+str(aci)+" : " + str(int(horizonte[int(aci+0.5)]*1000.)/1000.),
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(alt_c_aci_label0[0],alt_c_aci_label0[1],"Height of "+solstice0+"Sun at azimuth "+str(aci)+" : " + str(int(alt_c_aci[0]*1000.)/1000.)+"*",
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(alt_c_aci_label1[0],alt_c_aci_label1[1],"Height of "+solstice1+"Sun at azimuth "+str(aci)+" : " + str(int(alt_c_aci[1]*1000.)/1000.)+"*",
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(alt_c_aci_label2[0],alt_c_aci_label2[1],"Height of equinox Sun at azimuth "+str(aci)+" : " + str(int(alt_c_aci[2]*1000.)/1000.)+"*",
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)
        ax.text(alt_c_aci_label3[0],alt_c_aci_label3[1],"* Height shown only when Sun's altitude lower than 50 degrees",
            horizontalalignment = 'left',
            verticalalignment = 'top',
            fontsize = 7.5, color='black',
            transform = ax.transAxes)

        if diagtype != "Zotti Diagram":
            ax.text(0,-0.33, solstice0+'Solstice: '+str(ys0)+"/"+str(ms0)+"/"+str(ds0),
                horizontalalignment = 'left',
                verticalalignment = 'top',
                fontsize = 8, color='black',
                transform = ax.transAxes)

            ax.text(0,-0.40, 'Intermediate Equinox: '+str(yeq)+"/"+str(meq)+"/"+str(deq),
                horizontalalignment = 'left',
                verticalalignment = 'top',
                fontsize = 8, color='black',
                transform = ax.transAxes)

            ax.text(0,-0.47, solstice1+'Solstice: '+str(ys1)+"/"+str(ms1)+"/"+str(ds1),
                horizontalalignment = 'left',
                verticalalignment = 'top',
                fontsize = 8, color='black',
                transform = ax.transAxes)
        canvas.draw()
#******************************************************************---------------------------------------------------------------------------

    def graficar_a(self, event, global_n_cuerpoc, fig, ax, canvas):
        self.graficar(global_n_cuerpoc, fig, ax, canvas) 

    def readDEM(self, X1, Y1, X2, Y2, nomfile):

        resultado = []
        try:
            nfile = open(nomfile)
        except:
            i = 0
            while i < Y2-Y1+1:
                j = 0
                resultado.append([])
                while j < X2-X1+1:
                    resultado[i].append(0)
                    j += 1
                i += 1
            return resultado

        contl = 0
        for line in nfile:
            if contl >= Y1 and contl <= Y2:
                contc = 0
                valor = ""
                fila = []
                for char in line:
                    if char == "\n" or char == ",":
                        if contc >= X1 and contc <= X2:
                            fila.append(int(float(valor)))
                        valor = ""
                        contc += 1
                        continue
                    valor = valor + char
                resultado.append(fila)
            contl += 1
        nfile.close()
        return resultado

    def horizon(self,la,lo):

        # Builds the name of the corresponding file, according to the entered coordinates

        la2 = str(la)
        lo2 = str(lo)
        if la2[0] == "N" or la2[0] == "n":
            la2 = la2[1:]
        elif la2[0] == "S" or la2[0] == "s" or la2[0] == "-":
            la2 = "-" + la2[1:]

        if lo2[0] == "E" or lo2[0] == "e":
            lo2 = lo2[1:]
        elif lo2[0] == "W" or lo2[0] == "w" or lo2[0] == "-":
            lo2 = "-" + lo2[1:]

        la2 = float(la2)
        lo2 = float(lo2)

        dla = abs(float(la2) - int(float(la2)))
        dlo = abs(float(lo2) - int(float(lo2)))
        if la2 > 0.:
            letrala="N"
            fila_la = int((1 - dla) * 3600)
        else:
            letrala="S"
            la2 = abs(la2)+1.
            fila_la = int(dla * 3600)

        if lo2 < 0.:
            letralon="W"
            lo2 = abs(lo2)+1.
            col_lo = int((1 - dlo) * 3600)
        else:
            letralon="E"
            col_lo = int(dlo * 3600)

        cla = str(int(la2))
        clo = str(int(lo2))

        if abs(lo2) < 100.:
            clo = "0" + clo
            if abs(lo2) < 10.:
                clo = "0" + clo

        if abs(la2) < 10.:
            cla = "0" + cla

        nomarch = letrala+cla+letralon+clo+"p.asc"
        print("Archivo de la base de datos: ",nomarch)

        try:
            fhand = open (nomarch)
            fhand.close()
            limites = int(3600)
        except:
            try:
                nomarch = letrala+cla+letralon+clo+"c.asc"
                print("No se encontró base de datos de alta precisión, intentando con baja precisión....")
                fhand = open(nomarch)
                fhand.close()
                limites = int(1200)

                # Makes correction for a lower number of rows and columns in the database raster
                fila_la = int(fila_la / 3)
                col_lo = int(col_lo / 3)

            except:
                self.v_aviso("Coordinates are not in the database\nAstronomical horizon will be used","WARNING!")
                i = 0
                hor = []
                while i <= 360:
                    hor.append(0)
                    i += 1
                return hor
        print ("Tamaño de array:",limites)
        x = []   # This array variable contains the DEM to be used to draw the local horizon

                # Defines distance to the astronomical horizon
        dhor_pix = int(limites/2 -1)  # Horizon adjusted to 54 kms

        # Defines the astronomical horizon at a distance of dhor_pix squares (that is, dhor/1000 kms of distance)
        fila_0 = fila_la - dhor_pix
        fila_f = fila_la + dhor_pix
        col_0 = col_lo - dhor_pix
        col_f = col_lo + dhor_pix

        esqsupder = 45
        esqinfder = 45
        esqinfizq = 45
        esqsupizq = 45

########### Here, it determines which databases to read ##################

        if col_0 < 0:

            if fila_0 < 0:                                            # CASO A
                lev = int(0 - col_0)
                up = int(0 - fila_0)
                print (limites-lev, limites-up, limites)

                if letrala == "N" or letrala == "N0":
                    cla1 = str(int(cla) + 1)
                else:
                    cla1 = str(int(cla) - 1)
                if letralon == "E" or letralon == "E0":
                    clo1 = str(int(clo) - 1)
                else:
                    clo1 = str(int(clo) + 1)

                if int(cla1) < 10.:
                    cla1 = "0" + cla1

                if int(clo1) < 100.:
                    clo1 = "0" + clo1

        # Loads upper left matrix
                if limites == 3600:
                    nom_matriz1 = letrala+cla1+letralon+clo1+"p.asc"   # High precision Upper left matrix
                    nom_matriz2 = letrala+cla+letralon+clo1+"p.asc"   # High precision Lower left matrix
                    nom_matriz4 = letrala+cla1+letralon+clo+"p.asc"   # High precision Upper right matrix
                else:
                    nom_matriz1 = letrala+cla1+letralon+clo1+"c.asc"   # Low precision Upper left matrix
                    nom_matriz2 = letrala+cla+letralon+clo1+"c.asc"   # Low precision Lower left matrix
                    nom_matriz4 = letrala+cla1+letralon+clo+"c.asc"   # Low precision Upper right matrix

                matriz1 = []
                matriz1 = self.readDEM(limites-lev,limites-up,limites,limites,nom_matriz1)
                matriz2 = []
                matriz2 = self.readDEM(limites-lev,0,limites,fila_f,nom_matriz2)
                matriz4 = []
                matriz4 = self.readDEM(0,limites-up,col_f,limites,nom_matriz4)

        ### Building final matrix in order to find local horizon (Case A)
                x0 = self.readDEM(0,0,col_f,fila_f,nomarch)        # Carga datos de raster dentro del horizonte,
                                                                  # a partir del DEM original.
                i = 0
                x = []
        # Crea una matriz de ceros para rellenarse con los datos de los raster
                while i < limites:
                    fila_vacia = [0] * limites
                    x.append(fila_vacia)
                    i += 1
        # Incorpora la matriz 1
                i = 0
                while i < lev:
                    j = 0
                    while j < up:
                        x[j][i] = matriz1[j][i] # Corregir: No pueden tener la misma numeracion ambas matrices
                        j += 1
                    i+= 1
        # Incorpora la matriz 2
                i = 0
                while i < lev:
                    j = 0
                    while j < fila_f:
                        x[j+up][i] = matriz2[j][i]
                        j += 1
                    i += 1
        # Incorpora la matriz 4
                i = 0
                while i < col_f:
                    j = 0
                    while j < up:
                        x[j][i+lev] = matriz4[j][i]
                        j += 1
                    i += 1
        #Incorpora matriz 0
                i = 0
                while i < col_f:
                    j = 0
                    while j < fila_f:
                        x[j+up][i+lev] = x0[j][i]
                        j += 1
                    i += 1

            elif fila_f > limites:                                         # Caso C
                lev = 0 - col_0
                down = fila_f - limites

                if letrala == "N":
                    cla3 = str(int(cla) - 1)
                else:
                    cla3 = str(int(cla) + 1)
                if letralon == "E":
                    clo3 = str(int(clo) - 1)
                else:
                    clo3 = str(int(clo) + 1)

                if int(cla3) < 10.:
                    cla3 = "0" + cla3

                if int(clo3) < 100.:
                    clo3 = "0" + clo3

        # Encontrando la matriz superior izquierda
                if limites == 3600:
                    nom_matriz2 = letrala+cla+letralon+clo3+"p.asc"   # High precision Upper left matrix
                    nom_matriz3 = letrala+cla3+letralon+clo3+"p.asc"   # High precision lower left matrix
                    nom_matriz5 = letrala+cla3+letralon+clo+"p.asc"   # High precision lower left matrix
                else:
                    nom_matriz2 = letrala+cla+letralon+clo3+"c.asc"   # Low precision Upper left matrix
                    nom_matriz3 = letrala+cla3+letralon+clo3+"c.asc"   # Low precision lower left matrix
                    nom_matriz5 = letrala+cla3+letralon+clo+"c.asc"   # Low precision lower left matrix
                matriz2 = []
                matriz2 = self.readDEM(limites-lev,fila_0,limites,limites,nom_matriz2)

                matriz3 = []
                matriz3 = self.readDEM(limites-lev,0,limites,down,nom_matriz3)

                matriz5 = []
                matriz5 = self.readDEM(0,0,col_f,down,nom_matriz5)

        ### Here we build the final matrix that is used to make the local horizon (CASE C)
                x0 = self.readDEM(0,fila_0,col_f,limites,nomarch)    # Loads raster data into the horizon
                                                                     # from the original DEM
                i = 0
                x = []
        # Crea una matriz de ceros para rellenarse con los datos de los raster
                while i < limites:
                    fila_vacia = [0] * limites
                    x.append(fila_vacia)
                    i += 1
        # Incorpora la matriz 2
                i = 0
                while i < lev:
                    j = 0
                    while j < limites-fila_0:
                        x[j][i] = matriz2[j][i]
                        j += 1
                    i+= 1
        # Incorpora la matriz 3
                i = 0
                while i < lev:
                    j = 0
                    while j < down:
                        x[j+limites-fila_0][i] = matriz2[j][i]
                        j += 1
                    i += 1
        # Incorpora la matriz 5
                i = 0
                while i < col_f:
                    j = 0
                    while j < down:
                        x[j+limites-fila_0][i+lev] = matriz5[j][i]
                        j += 1
                    i += 1
        #Incorpora matriz 0
                i = 0
                while i < col_f:
                    j = 0
                    while j < limites-fila_0:
                        x[j][i+lev] = x0[j][i]
                        j += 1
                    i += 1

            else:                                                   # Caso 2

                lev = 0 - col_0
                if letralon == "E":
                    clo2 = str(int(clo) - 1)
                else:
                    clo2 = str(int(clo) + 1)
                if int(clo2) < 100.:
                    clo2 = "0" + clo2

        # Finding the left matrix
                if limites == 3600:
                    nom_matriz2 = letrala+cla+letralon+clo2+"p.asc"    # High precision left matrix
                else:
                    nom_matriz2 = letrala+cla+letralon+clo2+"c.asc"    # Low precision left matrix
                matriz2 = []
                matriz2 = self.readDEM(limites-lev,0,limites,limites,nom_matriz2)

        # Loading matrix 0
                x0 = self.readDEM(0,0,col_f,limites,nomarch)     # Loads data from the raster within the horizon,
                                                                 # from the original DEM.
                i = 0
                x = []
        # Creates a zero-filled matrix in order to be filled in with the data from all the matrixes
                while i < limites:
                    fila_vacia = [0] * limites
                    x.append(fila_vacia)
                    i += 1
        # Adds matrix 2
                i = 0
                while i < lev:
                    j = 0
                    while j < limites:
                        x[j][i] = matriz2[j][i]
                        j += 1
                    i+= 1

        # Adds matrix 0
                i = 0
                while i < col_f:
                    j = 0
                    while j < limites:
                        x[j][i+lev] = x0[j][i]
                        j += 1
                    i += 1

        elif col_f > limites:

            if fila_0 < 0:                                            # CASE B
                dex = col_f - limites
                up = int(0 - fila_0)

                if letrala == "N":
                    cla6 = str(int(cla) + 1)
                else:
                    cla6 = str(int(cla) - 1)
                if letralon == "E":
                    clo6 = str(int(clo) + 1)
                else:
                    clo6 = str(int(clo) - 1)

                if int(cla6) < 10.:
                    cla6 = "0" + cla6

                if int(clo6) < 100.:
                    clo6 = "0" + clo6

        # Finding upper-left matrix
                if limites == 3600:
                    nom_matriz4 = letrala+cla6+letralon+clo+"p.asc"  # High precision Upper left matrix
                    nom_matriz7 = letrala+cla+letralon+clo6+"p.asc"   # High precision lower-right matrix
                    nom_matriz6 = letrala+cla6+letralon+clo6+"p.asc"   # High precision upper-right matrix
                else:
                    nom_matriz4 = letrala+cla6+letralon+clo+"c.asc"  # Low precision Upper left matrix
                    nom_matriz7 = letrala+cla+letralon+clo6+"c.asc"  # Low precision lower-right matrix
                    nom_matriz6 = letrala+cla6+letralon+clo6+"c.asc" # Low precision upper-right matrix

                matriz4 = []
                matriz4 = self.readDEM(col_0,limites-up,limites,limites,nom_matriz4)

                matriz7 = []
                matriz7 = self.readDEM(0,0,dex,fila_f,nom_matriz7)

                matriz6 = []
                matriz6 = self.readDEM(0,limites-up,dex,limites,nom_matriz6)

        ### Building the final matrix from which the local horizon will be built (CASE B)
                x0 = self.readDEM(col_0,0,limites,fila_f,nomarch)        # Loads data from the raster within the horizon,
                                                              # from the original DEM.
                i = 0
                x = []
        # Creates a zero-filled matrix in order to be filled in with the data from all the matrixes
                while i < limites:
                    fila_vacia = [0] * limites
                    x.append(fila_vacia)
                    i += 1
        # Incorpora la matriz 4
                i = 0
                while i < limites-col_0:
                    j = 0
                    while j < up:
                        x[j][i] = matriz4[j][i]
                        j += 1
                    i+= 1
        # Incorpora la matriz 6
                i = 0
                while i < dex:
                    j = 0
                    while j < up:
#                        print (j, i, i+limites-col_0)
                        x[j][int(i+limites-col_0)] = matriz6[j][i]
                        j += 1
                    i += 1
        # Incorpora la matriz 7
                i = 0
                while i < dex:
                    j = 0
                    while j < fila_f:
                        x[j+up][int(i+limites-col_0)] = matriz7[j][i]
                        j += 1
                    i += 1
        #Incorpora matriz 0
                i = 0
                while i < limites-col_0:
                    j = 0
                    while j < fila_f:
                        x[j+up][i] = x0[j][i]
                        j += 1
                    i += 1

            elif fila_f > limites:                                         # Caso D
                dex = col_f - limites
                down = fila_f - limites

                if letrala == "N":
                    cla8 = str(int(cla) - 1)
                else:
                    cla8 = str(int(cla) + 1)
                if letralon == "E":
                    clo8 = str(int(clo) + 1)
                else:
                    clo8 = str(int(clo) - 1)

                if int(cla8) < 10.:
                    cla8 = "0" + cla8

                if int(clo8) < 100.:
                    clo8 = "0" + clo8

        # Finding the upper-right matrix
                if limites == 3600:
                    nom_matriz7 = letrala+cla+letralon+clo8+"p.asc"   # High precision upper-right matrix
                    nom_matriz8 = letrala+cla8+letralon+clo8+"p.asc"  # High precision lower-right matrix
                    nom_matriz5 = letrala+cla8+letralon+clo+"p.asc"   # High precision lower left matrix
                else:
                    nom_matriz7 = letrala+cla+letralon+clo8+"c.asc"   # Low precision upper-right matrix
                    nom_matriz8 = letrala+cla8+letralon+clo8+"c.asc"  # Low precision lower-right matrix
                    nom_matriz5 = letrala+cla8+letralon+clo+"c.asc"   # Low precision lower left matrix

                matriz7 = []
                matriz7 = self.readDEM(0,fila_0,dex,limites,nom_matriz7)

                matriz8 = []
                matriz8 = self.readDEM(0,0,dex,down,nom_matriz8)

                matriz5 = []
                matriz5 = self.readDEM(col_0,0,limites,down,nom_matriz5)

        ### Building the final matrix from which the local horizon will be built (CASE D)
                x0 = self.readDEM(col_0,fila_0,limites,limites,nomarch)   # Loads data from the raster within the horizon,
                                                                          # from the original DEM.
                i = 0
                x = []
        # Creates a zero-filled matrix in order to be filled in with the data from all the matrixes
                while i < limites:
                    fila_vacia = [0] * limites
                    x.append(fila_vacia)
                    i += 1
        # Incorpora la matriz 7
                i = 0
                while i < dex:
                    j = 0
                    while j < limites-fila_0:
                        x[j][int(i+limites-col_0)] = matriz7[j][i]
                        j += 1
                    i+= 1
        # Incorpora la matriz 8
                i = 0
                while i < dex:
                    j = 0
                    while j < down:
                        x[int(j+limites-fila_0)][int(i+limites-col_0)] = matriz8[j][i]
                        j += 1
                    i += 1
        # Incorpora la matriz 5
                i = 0
                while i < limites-col_0:
                    j = 0
                    while j < down:
                        x[int(j+limites-fila_0)][i] = matriz5[j][i]
                        j += 1
                    i += 1
        #Incorpora matriz 0
                i = 0
                while i < limites-col_0:
                    j = 0
                    while j < limites-fila_0:
                        x[j][i] = x0[j][i]
                        j += 1
                    i += 1

            else:                                                   # Caso 7

                dex = col_f-limites
                if letralon == "E":
                    clo7 = str(int(clo) + 1)
                else:
                    clo7 = str(int(clo) - 1)
                if int(clo7) < 100.:
                    clo7 = "0" + clo7

        # Finding right matrix
                if limites == 3600:
                    nom_matriz7 = letrala+cla+letralon+clo7+"p.asc" # High precision right matrix
                else:
                    nom_matriz7 = letrala+cla+letralon+clo7+"c.asc" # Low precision right matrix

                matriz7 = []
                matriz7 = self.readDEM(0,0,dex,limites,nom_matriz7)

        # Loading matrix 0
                x0 = self.readDEM(col_0,0,limites,limites,nomarch)        # Loads data from the raster within the horizon,
                                                              # from the original DEM.
                i = 0
                x = []
        # Creates a zero-filled matrix in order to be filled in with the data from all the matrixes
                while i < limites:
                    fila_vacia = [0] * limites
                    x.append(fila_vacia)
                    i += 1
        # Incorpora la matriz 7
                i = 0
                while i < dex:
                    j = 0
                    while j < limites:
                        x[j][i+limites-col_0] = matriz7[j][i]
                        j += 1
                    i+= 1

        #Incorpora matriz 0
                i = 0
                while i < limites-col_0:
                    j = 0
                    while j < limites:
                        x[j][i] = x0[j][i]
                        j += 1
                    i += 1

        elif fila_0 < 0:

            up = 0 - fila_0

            if letrala == "N":
                cla4 = str(int(cla) + 1)
            else:
                cla4 = str(int(cla) - 1)

            if int(cla4) < 10.:
                cla4 = "0" + cla4

    # Encontrando la matriz superior
            if limites == 3600:
                nom_matriz4 = letrala+cla4+letralon+clo+"p.asc"  # High precision upper matrix
            else:
                nom_matriz4 = letrala+cla4+letralon+clo+"c.asc"  # Low precision upper matrix

            matriz4 = []
            matriz4 = self.readDEM(0,limites-up,limites,limites,nom_matriz4)

    ### Aqui va la construcción de la matriz final para elaborar el horizonte (CASO 4)
            x0 = self.readDEM(0,0,limites,fila_f,nomarch)        # Loads data from the raster within the horizon,
                                                          # from the original DEM.
            i = 0
            x = []
    # Crea una matriz de ceros para rellenarse con los datos de los raster
            while i < limites:
                fila_vacia = [0] * limites
                x.append(fila_vacia)
                i += 1
    # Incorpora la matriz 4
            i = 0
            while i < limites:
                j = 0
                while j < up:
                    x[j][i] = matriz4[j][i]
                    j += 1
                i += 1
    #Incorpora matriz 0
            i = 0
            while i < limites:
                j = 0
                while j < fila_f:
                    x[j+up][i] = x0[j][i]
                    j += 1
                i += 1

        else:

            down = 0 - fila_f

            if letrala == "N":
                cla5 = str(int(cla) + 1)
            else:
                cla5 = str(int(cla) - 1)

            if int(cla5) < 10.:
                cla5 = "0" + cla5

    # Encontrando la matriz inferior
            if limites == 3600:
                nom_matriz5 = letrala+cla5+letralon+clo+"p.asc"   # High precision lower matrix
            else:
                nom_matriz5 = letrala+cla5+letralon+clo+"p.asc"   # Low precision lower matrix

            matriz5 = []
            matriz5 = self.readDEM(0,0,limites,down,nom_matriz5)

    ### Aqui va la construcción de la matriz final para elaborar el horizonte (CASO 5)
            x0 = self.readDEM(0,fila_0,limites,limites,nomarch)        # Carga datos de raster dentro del horizonte,
                                                          # a partir del DEM original.
            i = 0
            x = []
    # Crea una matriz de ceros para rellenarse con los datos de los raster
            while i < limites:
                fila_vacia = [0] * limites
                x.append(fila_vacia)
                i += 1
    # Incorpora la matriz 5
            i = 0
            while i < limites:
                j = 0
                while j < down:
                    x[j+limites-fila_0][i] = matriz5[j][i]
                    j += 1
                i += 1
    #Incorpora matriz 0
            i = 0
            while i < limites:
                j = 0
                while j < limites-fila_0:
                    x[j][i] = x0[j][i]
                    j += 1
                i += 1
        #print(x)
        th = 0
        hor = []
        print ("Elevación sobre nivel del mar del punto de observación:", x[int(limites/2)][int(limites/2)], "msnm")

        # Starts evaluating height for each tile in each line of azimuth,
        # from the point of view of the tile where the observer is located
        if limites == 3600:
            factorah = 30.
        else:
            factorah = 90.
        while th <= 360:

            th += 1  # Line of azimuth
            amax = 0 
            althor = 0. # temporary value of the horizon height
            # Multiplying factor according to the sector where the
            # line of azimuth that is being evaluated is pointing to.
            if th > 0 and th <= 90:
                factorx = 1
                factory = 1
            elif th > 90 and th <= 180:
                factorx = 1
                factory = -1
            elif th > 180 and th <= 270:
                factorx = -1
                factory = -1
            elif th > 270 and th <= 360:
                factorx = -1
                factory = 1

            if limites == 3600:
                maxtop = 1799
                maxbott = 1799
                maxizq = 1799
                maxder = 1799
                deltac0 = 1799
                deltaf0 = 1799
                deltaff = 1799
                deltacf = 1799
            else:
                maxtop = 599
                maxbott = 599
                maxizq = 599
                maxder = 599
                deltac0 = 599
                deltaf0 = 599
                deltaff = 599
                deltacf = 599

            # Determination of the coordinates of the last tile being used for
            # computing the height along a line of azimuth, inside the square
            # that contains the tiles within the horizon.
            if th > 0 and th <= esqsupder:  # I
                ycmax = maxtop * factory
                xcmax = int(maxtop*abs(tan(th*pi/180.))) * factorx
            if th > esqsupder and th <= 90: # II
                xcmax = maxder * factorx
                ycmax = int(maxder*abs(tan((90.-th)*pi/180.))) * factory
            elif th > 90 and th < esqinfder:  # III
                xcmax = maxder * factorx
                ycmax = int(maxder*abs(tan((th-90.)*pi/180.))) * factory
            elif th >= esqinfder and th <=180:  # IV
                xcmax = int(maxbott*abs(tan((180.-th)*pi/180.))) * factorx
                ycmax = maxbott * factory
            elif th > 180 and th <= esqinfizq:   # V
                xcmax = int(maxbott*abs(tan((th-180.)*pi/180.))) * factorx
                ycmax = maxbott * factory
            elif th > esqinfizq and th <= 270:  # VI
                xcmax = maxizq * factorx
                ycmax = int(maxizq*abs(tan((270.-th)*pi/180.))) * factory
            elif th > 270 and th < esqsupizq:
                xcmax = maxizq * factorx
                ycmax = int(maxizq*abs(tan((th-270.)*pi/180.))) * factory
            elif th >= esqsupizq:                # VIII
                xcmax = int(maxtop*abs(tan((360.-th)*pi/180.))) * factorx
                ycmax = maxtop * factory

            xc = 0
            while xc <= abs(xcmax):
                xc += 1
                y0 = int((xc-1)/(abs(tan(th*pi/180)))) * factory
                ym = int((xc-0.5)/(abs(tan(th*pi/180)))) * factory
                y1 = int(xc/(abs(tan(th*pi/180)))) * factory
                if abs(ym) > abs(ycmax):
                    ym = abs(ycmax) * factory
                if abs(y1) > abs(ycmax):
                    y1 = abs(ycmax) * factory
                i = 0
                while abs(y0+i) <= abs(ym):
                    coordx = (xc-1)*factorx + deltac0
                    coordy = deltaf0-(y0+i)
                    if coordx > maxder+maxizq or coordx < 0:
                        i += factory
                        continue
                    if coordy > maxtop+maxbott or coordy < 0:
                        i += factory
                        continue
                    althor = factorah*sqrt(((xc-1)*factorx)*((xc-1)*factorx)+(-(y0+i))*(-(y0+i)))
                    try:
                        if althor != 0:
                            althor = atan((float(x[coordy][coordx])-float(x[deltaf0][deltac0]))/althor)*180/pi
                    except:
                        i += 1*factory
                        break
                    if amax < althor:
                        amax = althor
                    i += 1*factory
                while abs(y0+i) <= abs(y1):
                    coordx = xc*factorx + deltac0
                    if coordx > maxder+maxizq or coordx < 0:
                        i += factory
                        continue
                    if coordy > maxtop+maxbott or coordy < 0:
                        i += factory
                        continue

                    althor = factorah*sqrt((xc*factorx)*((xc-1)*factorx)+(-(y0+i))*(-(y0+i))) # This is the distance from the evaluated
                    try:                                                                 # tile to the observer's tile in meters
                        if althor != 0:
                            althor = atan((float(x[coordy][xc*factorx + deltac0])-float(x[deltaf0][deltac0]))/althor)*180/pi
                    except:
                        i += 1*factory
                        break
                    if amax < althor:
                        amax = althor
                    i += 1*factory
            hor.append(amax)
        return hor

root = Tk()

screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
print(screen_width, screen_height)
root_xpos=int((screen_width-ancho_centro)/2-90)
root_ypos=int((screen_height-alt_centro)/2-120)
root.title("Chan U'Bih v4.2 High/Low Res Py3.8")
rootWindowPosition="+" + str(root_xpos) + "+" + str(root_ypos)
root.geometry(rootWindowPosition)

myapp = Chanubih(root,screen_width,screen_height)
root.mainloop()

# Improvements in this version over 4.1:
# 1) Adjusts the height of the Cartesian diagram to that which the user defines.
