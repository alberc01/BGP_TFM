
import tkinter
from turtle import color, width
from HJ_BGP_class import HJ_BGP
from OT_BGP_class import OT_BGP
from matplotlib import style
import numpy as np
import matplotlib.pyplot as plt
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from ttkwidgets.autocomplete import AutocompleteEntryListbox
from uritemplate import expand
from tkcalendar import Calendar, DateEntry
import datetime
import pytz

class Graphics(tk.Tk):
    # Constructrora para inicializar la interfaz grafica de la aplicacion
    def __init__(self):
        # Inizializamos tkinter de manera que sea padre de la aplicacion
        super().__init__()
        # Asignamos un estilo para las pestañas de la aplicaicon
        s = ttk.Style()        
        s.configure('TNotebook.Tab', padding=[100, 10], font = ('Times', '21', 'bold'))
        # Obtenemos los datos filtrados almacenados de manera local
        self.country_data, self.country_iso2, self.raw_data, self.ot_data, self.o_date, self.r_date = self.readJson()

        # Inicializacion de los objetos principales que se mostraran en la aplicacion
        self.OT_bgp = OT_BGP()
        self.HJ_bgp = HJ_BGP()
        
        # inicializacion del panel principal de la aplicacion
        self.mainframe = Frame(self)
        self.mainframe.pack()

        # Variable no utilizada #TODO
        self.country_entry = None

        # Construccion de las difrentes pestañas que compondran la aplicacion
        tab_widget = ttk.Notebook(self.mainframe)
        self.Ot_tab = Frame(tab_widget)
        self.HJ_tab = Frame(tab_widget)
        self.BGP_nt_r = Frame(tab_widget)
        
        # Adicion de las diferentes pestañas al panel principal de la aplicacion
        tab_widget.add(self.Ot_tab, text ='Outage Stats')
        tab_widget.add(self.HJ_tab, text ='Hijack Stats')
        tab_widget.add(self.BGP_nt_r, text ='BGP Net Policy Recommend')
        tab_widget.pack(expand = 1, fill ="both")

        # Llamada a la construccion interna de los componentes de cada pestaña
        self.GUI_main_frame()

    # Funcion para pasar un string de fecha al formato datetime
    def string_to_datetime(self,string_date):
        # obtencion de datetime con horario utc
        return datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S%z')

    # Funcion para leer el archivo Json que contiene la informacion con las incidencias BGP
    def readJson(self):
        # Apertura y lectura del archivo Json correspondiente y almacenado localmente
        with open('dict_by_country.json')as json_file:
            raw_data  = json.load(json_file)
        
        # Inicializacion de listas que seleccionaran la informacion que sera tratada en la aplicacion
        country = []
        ot_data = []
        country_iso2 = []

        # Obtencion de las fechas mas reciente y mas antigua para limitar el calendario de la aplicacion
        recent_date= self.string_to_datetime(raw_data['most_recent_date'])
        oldest_date= self.string_to_datetime(raw_data['oldest_date'])

        # Poblado de datos con la informacion del Json, para que sea mas facil de tratar
        for k in raw_data.keys():
            if k not in ["oldest_date", "most_recent_date"]:
                country.append(raw_data[k]['ctry_fullname'])
                country_iso2.append(k)
                ot_data.append(raw_data[k]['OT_count'])

        return country, country_iso2, raw_data, ot_data, oldest_date, recent_date

    # Funcion que permite construir un widget de autocompletado para seleccionar los paises sobre los que el usuario quiere la informacion
    def autocomplete_country_combo_widget(self, tabname, bgp_object):
        ## Creacion y emplazamiento del frame de los paises seleccionables ##
        autocomp_country_frame = Frame(tabname, bg='steel blue')
        autocomp_country_frame.grid(row=0, column=0, sticky= tk.NS)
        # Creacion y emplazamiento de Label para diferenciar los paises que se pueden seleccionar
        Label(
            autocomp_country_frame, 
            bg='steel blue',
            font = ('Times',21),
            text='Countries to select',
            ).grid(row=0, column=0, sticky= tk.NS)
        # Creacion del widget de autocompletado para seleccionar los paises a añadir
        auto_in = AutocompleteEntryListbox(
            autocomp_country_frame, 
            width=40, 
            font=('Times', 18),
            completevalues=self.country_data
            )
        # Emplazamiento del widget de autocompletado para seleccionar los paises a añadir
        auto_in.grid(row=1, column=0, sticky= tk.NS)

        ## Creacion y emplazamiento del frame de los paises seleccionados ##
        country_list_frame  = Frame(tabname, bg='steel blue')
        country_list_frame.grid(row=0, column=1, sticky= tk.NS)
        # Creacion y emplazamiento de Label para diferenciar los paises que se pueden eliminar de los seleccionados
        Label(
                country_list_frame,
                bg='steel blue',
                font = ('Times',21),
                text='Countries selected',
        ).grid(row=0, column=0)
        # Creacion del widget de autocompletado para seleccionar los paises a eliminar
        auto_out= AutocompleteEntryListbox(
                country_list_frame, 
                width=40, 
                font=('Times', 18),
                completevalues=bgp_object.get_country_list()
                )
        # Emplazamiento del widget de autocompletado para seleccionar los paises a eliminar
        auto_out.grid(row=1, column=0, sticky= tk.NS)

        ## Creacion del frame que contendra la botonera con las opciones de adicion sobre la lista ##
        add_butt_frame = Frame(tabname, bg='steel blue')
        # Creacion y emplazamiento del boton para añadir un pais a la lista de seleccionados
        add_but = Button(
            add_butt_frame, 
            width=18,
            font=('Times', 18),
            text = "Add to list",
            command= lambda: [bgp_object.add_to_country_list(auto_in.get()),self.update_ot_list_info(bgp_object,auto_out)],
            bg='steel blue',
            ).grid(row=0, column=0)
        # Creacion y emplazamiento del boton para añadir todos los elementos a la lista de seleccionados
        add_all_but = Button(
            add_butt_frame, 
            width=18,
            font=('Times', 18),
            text = "Add All",
            command= lambda: [bgp_object.set_country_list(self.country_data),self.update_ot_list_info(bgp_object,auto_out)],
            bg='steel blue',
            ).grid(row=0, column=1)
        # Emplazamiento de la botonera de adicion
        add_butt_frame.grid(row=2, column=0)
        
        ## Creacion del frame que contendra la botonera con las opciones de eliminacion sobre la lista ##
        del_butt_frame = Frame(tabname, bg='steel blue')
        # Creacion y emplazamiento del boton para eliminar un pais de la lista de seleccionados
        remove_but = Button(
            del_butt_frame, 
            width=18,
            font=('Times', 18),
            text = "Delete from list",
            command= lambda: [bgp_object.remove_from_country_list(auto_out.get()),self.update_ot_list_info(bgp_object, auto_out)],
            bg='steel blue',
            ).grid(row=0, column=0)
        # Creacion y emplazamiento del boton para eliminar todos los elementos de la lista de seleccionados
        remove_all_but = Button(
            del_butt_frame, 
            width=18,
            font=('Times', 18),
            text = "Clear List",
            command= lambda: [bgp_object.clear_country_list(),self.update_ot_list_info(bgp_object, auto_out)],
            bg='steel blue',
            ).grid(row=0, column=1)
        # Emplazamiento de la botonera de eliminacion
        del_butt_frame.grid(row=2, column=1)

    # Funcion para actualizar la lista de valores seleccionados cuando se pulse el boton correspondiente
    def update_ot_list_info(self, bgp_object, auto_out):
        auto_out.configure(completevalues = bgp_object.get_country_list())
    
    # Funcion que permite construir el widget para mostrar la infromacion en forma de graficos
    def plot_widget(self, tab_frame, plot_main_func ,from_cl, to_cl):

        # Creacion de un frame auxiliar para facilitar el emplazamiento de elementos
        aux_frame = Frame(tab_frame)
        # Creacion de la figura donde se renderizara el grafico
        figure = Figure(figsize = (10,5), dpi = 150)
        # Creacion de la figura canvas con posibilidad de scroll
        canvas_figure = self.addScrollingFigure(figure, aux_frame)

        # Creacion y emplazamiento del boton para construir el grtafico
        Button(
            tab_frame, 
            width=30,
            font=('Times', 18),
            text = "Get outtage bar diagram",
            command= lambda: plot_main_func(canvas_figure, figure, from_cl, to_cl),
            bg='steel blue',
            pady= 2
        ).grid(row=0, column=2, columnspan= 1)
    
    def addScrollingFigure(self, figure, frame):
        aux_frame = Frame(frame)
        aux_frame.pack(pady= 10)
        # set up a canvas with scrollbars
        canvas = Canvas(aux_frame,width= 1000, height=500)
        canvas.grid(row=0, column=0, sticky=tk.NSEW)

        xScrollbar = Scrollbar(aux_frame, orient=tk.HORIZONTAL)
        yScrollbar = Scrollbar(aux_frame)

        xScrollbar.grid(row=1, column=0, sticky=tk.EW)
        yScrollbar.grid(row=0, column=1, sticky=tk.NS)
        xScrollbar.config(command=canvas.xview)
        yScrollbar.config(command=canvas.yview)

        canvas.config(xscrollcommand=xScrollbar.set)
        canvas.config(yscrollcommand=yScrollbar.set)
        
        figAgg = FigureCanvasTkAgg(figure, canvas)
        figAgg.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
        NavigationToolbar2Tk(figAgg, frame)
        mplCanvas = figAgg.get_tk_widget()
        mplCanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
        
        # and connect figure with scrolling region
        canvas.create_window(0, 0,width=1000, height=500, window=mplCanvas)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
        
    
        frame.grid(row=3, column=0, columnspan= 4, sticky= tk.NS)
        
        return figAgg
    
    def date_selectors_widget(self, tabname):
        # def from_date_selector_widget(self):
        date_frame  = Frame(tabname)
        

        l1 = Label(
                date_frame,
                bg='steel blue',
                font = ('Times',21),
                text='From date',
        )
        
        from_cal = DateEntry(master = date_frame ,
                    font="Times 18",
                    selectmode='day',
                    year=self.o_date.year,
                    month=self.o_date.month,
                    day=self.o_date.day,
                    mindate = self.o_date,
                    maxdate = self.r_date
                    )
        
        # def to_date_selector_widget(self):        
        l2 = Label(
                date_frame,
                bg='steel blue',
                font = ('Times',21),
                text='To date',
        )
        
        to_cal = DateEntry(master = date_frame,
                    font="Times 18",
                    selectmode='day',
                    year=self.r_date.year,
                    month=self.r_date.month,
                    day=self.r_date.day,
                    mindate = self.o_date,
                    maxdate = self.r_date)

        l1.grid(row=0, column=0, sticky= tk.N)
        l2.grid(row=0, column=2, sticky= tk.N)
        
        from_cal.grid(row=1, column=0, sticky= tk.N)           
        to_cal.grid(row=1, column=2, sticky= tk.N)

        date_frame.grid(row=0, column=2, sticky= tk.N)

        return from_cal, to_cal

    def show_plot(self,canvas, figure, dataX, dataY1, dataY2=None):
        try:
            self.axes.remove()
            self.axes2.remove()
        except:
            pass

        
        if not dataY2: 
            self.axes = figure.add_subplot()
            self.axes.bar(dataX, dataY1)
            self.axes.set_ylabel("Number of Outages")
        else:
            self.axes = figure.add_subplot(1,1,1)
            r = np.arange(len(dataX))
            w = 0.2

            self.axes.bar(r - w/2, dataY1, width = w, color='g')
            self.axes.set_ylabel('Injured')
            
            self.axes2 = self.axes.twinx()
            self.axes2.bar(r + w/2, dataY2, width = w, color='r')
            self.axes2.set_ylabel('Causer')
            
            self.axes.set_xticks(r,dataX, minor=False)

        canvas.draw()

    # Funcion no utilizada de momento #TODO
    def search_items(self):
        search_value = self.country_entry.get()
        if search_value == "" or search_value == " ":
            self.combo['values'] = self.country_data
        else:
            value_to_display = []
            for v in self.country_data:
                if search_value.lower() in v.lower():
                    value_to_display.append(v)
            
            self.combo['values'] = value_to_display
    
    def Ot_bar_plot(self, canvas_figure, figure, from_cl, to_cl):
        ot_bar_diag = {'X': [], 'Y':[]}
        for item in self.OT_bgp.get_country_list():
            iso2Ctry =self.country_iso2[self.country_data.index(item)]
            ot_bar_diag['X'].append(iso2Ctry)
            ot_count = self.obtain_conutry_ot_between_dates(iso2Ctry, from_cl.get_date(), to_cl.get_date())
            ot_bar_diag['Y'].append(ot_count)
        
        self.show_plot(canvas_figure, figure, ot_bar_diag['X'], ot_bar_diag['Y'])

    def obtain_conutry_ot_between_dates(self, countryISO2, from_date, to_date):
        ot_counter = 0
        from_date = datetime.datetime.combine(from_date, datetime.datetime.min.time()).replace(tzinfo=datetime.timezone.utc)
        to_date = datetime.datetime.combine(to_date, datetime.datetime.min.time()).replace(tzinfo=datetime.timezone.utc)
        for k,v in self.raw_data[countryISO2]['OT_by_date'].items():
            date_of_issue = self.string_to_datetime(k)
            if  from_date < date_of_issue < to_date:
                ot_counter += v
        return ot_counter

    def Hj_bar_plot(self,canvas_figure, figure, from_cl, to_cl):
        hj_bar_diag = {'X': [],'Y1':[], 'Y2':[]}
        for item in self.HJ_bgp.get_country_list():
            iso2Ctry =self.country_iso2[self.country_data.index(item)]
            hj_bar_diag['X'].append(iso2Ctry)
            causer_counter ,injured_counter = self.obtain_conutry_hj_between_dates(iso2Ctry, from_cl.get_date(), to_cl.get_date())
            hj_bar_diag['Y1'].append(injured_counter)
            hj_bar_diag['Y2'].append(causer_counter)
        
        self.show_plot(canvas_figure, figure, hj_bar_diag['X'], hj_bar_diag['Y1'], hj_bar_diag['Y2'])

    def obtain_conutry_hj_between_dates(self, countryISO2, from_date, to_date):
        causer_counter = 0
        injured_counter = 0
        from_date = datetime.datetime.combine(from_date, datetime.datetime.min.time()).replace(tzinfo=datetime.timezone.utc)
        to_date = datetime.datetime.combine(to_date, datetime.datetime.min.time()).replace(tzinfo=datetime.timezone.utc)

        for k,v in self.raw_data[countryISO2]['HJ_by_date']['causer'].items():
            date_of_issue = self.string_to_datetime(k)
            if  from_date < date_of_issue < to_date:
                causer_counter += v

        for k,v in self.raw_data[countryISO2]['HJ_by_date']['injured'].items():
            date_of_issue = self.string_to_datetime(k)
            if  from_date < date_of_issue < to_date:
                injured_counter += v

        return causer_counter, injured_counter

    def construct_ot_tab(self):
        from_cl, to_cl = self.date_selectors_widget(self.Ot_tab)
        self.autocomplete_country_combo_widget(self.Ot_tab, self.OT_bgp)
        self.plot_widget(self.Ot_tab, self.Ot_bar_plot, from_cl, to_cl)  

    def construct_hj_tab(self):
        from_cl, to_cl = self.date_selectors_widget(self.HJ_tab)
        self.autocomplete_country_combo_widget(self.HJ_tab, self.HJ_bgp)
        self.plot_widget(self.HJ_tab, self.Hj_bar_plot, from_cl, to_cl) 

    # Funcion par costruir las diferentes pestañas de manera modular 
    def GUI_main_frame(self):
        # Creamos y establecemos el tamaño de la ventana de la aplicacion
        self.geometry("1900x1060")
        # Asignamos un titulo al frontal de la aplicacion
        self.title("Sistema de recomendacion de politicas de trafico BGP")

        # Contruimos la pestaña que mostrara la informacion con las caidas en BGP
        self.construct_ot_tab()
        # Construimos las pestaña que mostrara la informacion con las suplantaciones de BGP
        self.construct_hj_tab()
        
Graphics().mainloop()