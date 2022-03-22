from tkinter import *
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import json
import datetime
from tkinter import ttk


class BGP():
    def __init__(self):
        self.country_data, self.country_iso2, self.raw_data, self.ot_data, self.o_date, self.r_date = self.readJson()

    def readJson(self):
        with open('dict_by_country.json')as json_file:
            raw_data  = json.load(json_file)
        
        country = []
        ot_data = []
        country_iso2 = []

        recent_date= self.string_to_datetime(raw_data['most_recent_date'])
        oldest_date= self.string_to_datetime(raw_data['oldest_date'])

        for k in raw_data.keys():
            if k not in ["oldest_date", "most_recent_date"]:
                country.append(raw_data[k]['ctry_fullname'])
                country_iso2.append(k)
                ot_data.append(raw_data[k]['OT_count'])

        return country, country_iso2, raw_data, ot_data, oldest_date, recent_date

    def string_to_datetime(self,string_date):
        return datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S%z')

    