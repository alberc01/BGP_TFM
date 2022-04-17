from tkinter import *
import tkinter as tk
from tkcalendar import Calendar, DateEntry

from tkinter import ttk


class BGP:
    def __init__(self, country_data, country_iso2, raw_data, ot_data, o_date, r_date):
        self.country_data = country_data
        self.country_iso2 = country_iso2
        self.raw_data = raw_data
        self.ot_data = ot_data
        self.o_date = o_date
        self.r_date = r_date


    