from sys import maxsize
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

class Graphics(tk.Tk):
    def __init__(self):
        super().__init__()
        self.country_data, self.ot_data = self.readJson()
        self.mainframe = Frame(self)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=3)


        country = []
        ot_data = []
        self.mainframe.pack()
        self.country_list = []
        self.country_entry = None
        self.figure = None
        
        self.autocomplete_country_combo()

    #     self.nrows = 2
    #     self.ncols = 2
    #     for i in range(self.nrows):
    #         self.grid_rowconfigure(i, weight=1)
    #         self.grid_columnconfigure(i, weight=1)
    #     # self.resizable(0,0)
    # #     self.fig = plt.figure()
    
    def readJson(self):
        with open('dict_by_country.json')as json_file:
            data  = json.load(json_file)
        
        country = []
        ot_data = []

        for k in data.keys():
            country.append(data[k]['ctry_fullname'])
            ot_data.append(data[k]['OT_count'])

        return country, ot_data


    def autocomplete_country_combo(self):

        self.geometry("1920x700")
        self.title("Sistema de recomendacion de politicas de trafico BGP")


        self.frame = Frame(self.mainframe, bg='#f25252')
        self.frame.grid(row=0, column=0, sticky= tk.NS)

        Label(
            self.frame, 
            bg='#f25252',
            font = ('Times',21),
            text='Countries to select',
            ).grid(row=0, column=0, sticky= tk.NS)

        self.autocomplete_entry = AutocompleteEntryListbox(
            self.frame, 
            width=40, 
            font=('Times', 18),
            completevalues=self.country_data
            )
        self.autocomplete_entry.grid(row=1, column=0, sticky= tk.NS)


        self.country_list_frame  = Frame(self.mainframe, bg='#f25252')
        self.country_list_frame.grid(row=0, column=1, sticky= tk.NS)
        

        Label(
                self.country_list_frame,
                bg='#f25252',
                font = ('Times',21),
                text='Countries selected',
        ).grid(row=0, column=0)

        self.autocomplete_out = AutocompleteEntryListbox(
                self.country_list_frame, 
                width=40, 
                font=('Times', 18),
                completevalues=self.country_list
                )
        self.autocomplete_out.grid(row=1, column=0, sticky= tk.NS)


        Button(
            self.mainframe, 
            width=30,
            font=('Times', 18),
            text = "Add to Country List",
            command= self.add_to_country_list,
            bg='#f25252',
            ).grid(row=1, column=0)
        
        Button(
            self.mainframe, 
            width=30,
            font=('Times', 18),
            text = "Delete from Country List",
            command= self.remove_from_country_list,
            bg='#f25252',
            ).grid(row=1, column=1)

        self.from_date_selector()
        self.to_date_selector()      

        self.figure = Figure(figsize = (6,4), dpi = 100)
        canvas_figure = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(canvas_figure, self)
        canvas_figure.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        Button(
            self.mainframe, 
            width=30,
            font=('Times', 18),
            text = "Show plot",
            command= lambda: self.show_plot(canvas_figure),
            bg='#f25252',
            pady= 2
        ).grid(row=1, column=2, columnspan= 2, sticky= tk.NS)


    def from_date_selector(self):
        self.date_from_frame  = Frame(self.mainframe)
        self.date_from_frame.grid(row=0, column=2, sticky= tk.NS)
        Label(
                self.date_from_frame,
                bg='#f25252',
                font = ('Times',21),
                text='From date',
        ).pack()
        cal = DateEntry(self.date_from_frame ,
                    font="Times 18", selectmode='day',
                    cursor="hand1", year=2018, month=2, day=5)
        cal.pack()
        
    def to_date_selector(self):

        self.date_to_frame  = Frame(self.mainframe)
        self.date_to_frame.grid(row=0, column=3, sticky= tk.NS)
        Label(
                self.date_to_frame,
                bg='#f25252',
                font = ('Times',21),
                text='To date',
        ).pack()
        cal2 = DateEntry(self.date_to_frame ,
                    font="Times 18", selectmode='day',
                    cursor="hand1", year=2018, month=2, day=5)
        cal2.pack()



    
    def add_to_country_list(self):
        v = self.autocomplete_entry.get()

        if v not in self.country_list:
            self.country_list.append(v)

            self.autocomplete_out.configure(completevalues = self.country_list)

    def remove_from_country_list(self):
        v = self.autocomplete_out.get()

        if v in self.country_list:
            self.country_list.remove(v)

            self.autocomplete_out.configure(completevalues = self.country_list)

        # y_pos = np.arange(len(country))
        # plt.bar(y_pos, ot_data)
        # plt.xticks(y_pos, country )
        # plt.show()
        # plt.savefig('prueba.png')
    def show_plot(self,canvas):
        dataX = self.country_list

        dataY = []
        for i in dataX:
            c_idx = self.country_data.index(i)
            dataY.append(self.ot_data[c_idx])
            

        try:
            self.axes.remove()
        except:
            pass
        self.axes = self.figure.add_subplot()
        self.axes.bar(dataX, dataY)
        self.axes.set_ylabel("Number of Outages")
        canvas.draw()

        

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

    
Graphics().mainloop()