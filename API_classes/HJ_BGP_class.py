from BGP_class import BGP


class HJ_BGP(BGP):
    def __init__(self):
        super().__init__()
        self.country_list = []

    def add_to_country_list(self, v):
        if (v != "") and (v not in self.country_list):
            self.country_list.append(v)

    def set_country_list(self,list):
        self.country_list = list.copy()

    def remove_from_country_list(self, v):
        if v in self.country_list:
            self.country_list.remove(v)

    def clear_country_list(self):
        self.country_list = []

    def get_country_list(self):
        return self.country_list


    
