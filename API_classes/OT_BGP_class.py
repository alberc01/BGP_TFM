from copy import copy
from API_classes.BGP_class import BGP
import re


class OT_BGP(BGP):
    def __init__(self, country_data, country_iso2, raw_data, ot_data, o_date, r_date):
        super().__init__(country_data, country_iso2, raw_data, ot_data, o_date, r_date)
        self.selected_list = []
        self.sortedmainlist = sorted(self.country_data)
        
        aux = []
        another = copy(self.sortedmainlist)
        for i in self.sortedmainlist:
            if self.hasnum(i):
                aux.append(i)
                another.remove(i)
        self.sortedmainlist = sorted(another)
        self.mainlist =  self.sortedmainlist  + aux

    def hasnum(self, elem):
        return bool(re.search(r'\d', elem))

    def add_to_selected_list(self, v):
        if (v != "") and (v not in self.selected_list):
            self.selected_list.append(v)

    def set_selected_list(self,list):
        self.selected_list = list.copy()

    def remove_from_selected_list(self, v):
        if v in self.selected_list:
            self.selected_list.remove(v)
    
    def clear_selected_list(self):
        self.selected_list = []

    def get_selected_list(self):
        return self.selected_list
