from calendar import c
from unicodedata import name
import pandas as pd
from ipwhois import IPWhois
import subprocess
import re
from collections import Counter
import time
import pycountry as pycty
import sys
from geopy.geocoders import Nominatim
import geocoder
from munch import DefaultMunch

class Country:
    # def __init__(self):
        # inicializamos la lectura del pandas dataframe
        # self.country_dataframe = self.read_country_diminutives()
        # nm = Nominatim(user_agent="BGP_RECOM")
        # country = geocoder.google('Mountain View, CA')
        # print(country.raw)
        
    #     for country in pycty.countries: 
    #         print(country)
        
    # def read_country_diminutives(self):
    #     # dfs = pd.read_excel("/home/alber/TFM-LINUX/BGP_TFM/country_info/country.xlsx", sheet_name= None)
    #     # # Conseguimos los codigos de los paises
    #     # partial_dfs = dfs['Codes']
    #     # # Construimos un pandas con la informacion que es relevante
    #     # final_df = pd.DataFrame(partial_dfs, columns=['ISO2', 'ISO3', 'CATEGORY', 'LIST NAME'])
        
    #     # Leemos el archivo CSV con pandas
    #     df = pd.read_csv('/home/alber/TFM-LINUX/BGP_TFM/country_info/country_codes.csv', keep_default_na=False)

    #     return df

    def get_asn_from_string(self, frame):
        as_name = frame.split(' ') 
        regex = re.compile(r'^AS') 
        filtered = [i for i in as_name if regex.match(i)]
        return filtered
    
    def get_country_from_whois_data(self, frame):
        # filtramos la informacion obtenida con el comando whois
        server_data = str(frame).split('\n')
        regex = re.compile(r'^organisation',re.IGNORECASE)
        regex_to_sub = re.compile(r'^organisation:',re.IGNORECASE)
        
        # obtenemos los campos con clave Country 
        ret = [regex_to_sub.sub("",i.replace(" ", '')) for i in server_data if regex.match(i)]
        if len(ret) > 0:
            try:
                country_text = subprocess.check_output(['whois',ret[0]]).decode(sys.stdout.encoding).strip()
                ret = self.find_country_in_text(country_text)
            except :
                print("Whois problem!")
                ret = self.find_country_in_text(str(frame))
        else:
            ret = self.find_country_in_text(str(frame))

        return ret

    def find_country_in_text(self,text):
        ret = []
        # filtramos la informacion obtenida con el comando whois
        server_data = text.split('\n')
        regex = re.compile(r'^Country:',re.IGNORECASE)
        regex_to_sub = re.compile(r'^Country:',re.IGNORECASE)
        
        # obtenemos los campos con clave Country 
        ret = [regex_to_sub.sub("",i.replace(" ", '')) for i in server_data if regex.match(i)]
        if len(ret) < 1:
            countries = sorted([country for country in pycty.countries] , key=lambda x: -len(x.name))
            alpha_list = []
            for country in countries:
                alpha_list.append(country.alpha_2)
                if country.name.lower() in text.lower():
                    # ret.extend(list(self.country_dataframe[self.country_dataframe['Name'] == country]['Code'].values))
                    ret.append(country.alpha_2)
                    
            if len(ret) < 1:
                filter = re.sub('\r?\n%*', ' ', text)
                # for code in self.country_dataframe['Code'].values:
                for code in alpha_list :
                    if (' ' + code + ' ') in (' ' + filter + ' '):
                        ret.append(code)
        
        # if len(ret) < 1:
        #     regex = re.compile(r'^address:',re.IGNORECASE)
        #     regex_to_sub = re.compile(r'^address:',re.IGNORECASE)
        
        #      # obtenemos los campos con clave Country 
        #     addrs = [regex_to_sub.sub("",i) for i in server_data if regex.match(i)]
        #     if len(addrs)>0: 
        #         nm = Nominatim(user_agent="BGP_RECOM")
        #         country = nm.geocode(addrs[0])
        #         print(country.raw)
        
        return ret

    def is_iso2_fromat(self, frame):
        return  frame != 'ZZ' and len(frame.split(' ')) < 2 and frame != '' and frame.isnumeric()


    def check_country_in_tweet(self, id, country_indic):
            # comprobamos si el id esta en fromato ISO2
                # data = self.country_dataframe.loc[self.country_dataframe['Code']==id]
            data = pycty.countries.get(alpha_2=id)
            if data:
                return data
            else:
                # comprobamos si el country esta en el tweet publicado en ISO2
                    # is_iso2 = self.country_dataframe.loc[self.country_dataframe['Code']==country_indic]
                is_iso2 = pycty.countries.get(alpha_2=country_indic)
                # comprobamos si el country esta en el tweet publicado en forma de nombre completo
                    # is_full_name = self.country_dataframe.loc[self.country_dataframe['Name']==country_indic]
                is_full_name = pycty.countries.get(name=country_indic)
                if is_iso2:
                    return is_iso2
                elif is_full_name:
                    return is_full_name
            return data

    def get_as_country_by_whois(self, as_name):
        try :
            # hay alguna cadena ASN entre los prametros de entrada
            # obtenemos la infomacion con el comando whois
            server_data = subprocess.check_output(['whois',as_name]).decode(sys.stdout.encoding).strip()
        except:
            # si no se puede obtener informacion devolvemos el id del ASN
            id_retrieve = as_name.replace('AS','')
            data = {
            'alpha_2' : id_retrieve, 
            'name' : id_retrieve, 
            'flag' : id_retrieve
            }
            # data = pd.DataFrame.from_dict(data)
            data = DefaultMunch.fromDict(data)
            return data

        # filtramos la informacion obtenida con el comando whois
        # obtenemos los campos con clave Country 
        filtered = self.get_country_from_whois_data(server_data)
                        
        if len(filtered) > 0:
            # si hemos conseguido algun country del comando whois obtenemos el que mas se repita y lo devolvemos
            dict_country_rept = Counter(filtered)
            dict_country_rept['ZZ'] = 0
            country_code = max(dict_country_rept, key = dict_country_rept.get)
            # data = self.country_dataframe.loc[self.country_dataframe['Code']==country_code]
            data = pycty.countries.get(alpha_2=country_code)
        else:
            # si no hay ningun country con fromato ISO2 devolvemos el id del ASN
            # id_retrieve = as_name.replace('AS','')
            # data = {'Code':[id_retrieve],'Name': [id_retrieve]}
            # data = pd.DataFrame.from_dict(data)
            id_retrieve = as_name.replace('AS','')
            data = {
            'alpha_2' : id_retrieve, 
            'name' : id_retrieve, 
            'flag' : id_retrieve
            }
            data = DefaultMunch.fromDict(data)

        return data


    def find_country_info_V2(self, id, country_indic):
            
            data = self.check_country_in_tweet(id, country_indic)

            if not data:
                # comprobamos que el id no es desconocido 
                # o si la cadena id que se pasa por parametro puede llegar a ser un ASN
                if self.is_iso2_fromat(id):
                    as_name  = 'AS'+ id # Si es un ASN concatenamos para utilizar el comando whois
                else:
                    # comprobamos si la cadena id recibida contiene algun ASN
                    filtered = self.get_asn_from_string(id)
                    if len(filtered) > 0:
                        # si hay algun ASN nos quedamos con el primero de la lista
                        as_name = filtered[0] 
                    else:
                        # si la cadena ID no contiene ningun ASN comprobamos la cadena country_indic
                        # data = self.country_dataframe.loc[self.country_dataframe['Code']==country_indic]
                        data = pycty.countries.get(alpha_2=country_indic)
                        # if data.empty:
                        if not data:
                            # si no contiene formato ISO2 comprobamos si existe la cadena ASN
                            if self.is_iso2_fromat(country_indic):
                                as_name  = 'AS'+ id # Si es un ASN concatenamos para utilizar el comando whois
                            else:
                                # comprobamos si la cadena country_indic recibida contiene algun ASN
                                filtered = self.get_asn_from_string(country_indic)
                                if len(filtered) > 0:
                                    # si hay algun ASN nos quedamos con el primero de la lista
                                    as_name = filtered[0] 
                                else:
                                    # si no esta en fromato ISO2 devolvemos country desconocido
                                    # data = {'Code':['ZZ'],'Name': ['UNKNOWN']}
                                    # data = pd.DataFrame.from_dict(data)
                                   
                                    data = {
                                    'alpha_2' : 'ZZ', 
                                    'name' : 'UNKNOWN', 
                                    'flag' : 'UNKNOWN'
                                    }
                                    data = DefaultMunch.fromDict(data)
                                    return data
                        else:
                            return data
                try :
                    # hay alguna cadena ASN entre los prametros de entrada
                    # obtenemos la infomacion con el comando whois
                    # time.sleep(5) # Esperamos 5 segundos para evitar el bloqueo de ip por multiples solicitudes en poco tiempo
                    server_data = subprocess.check_output(['whois',as_name]).decode(sys.stdout.encoding).strip()
                except:
                    print("Problem with AS: " + as_name)
                    # si el comando whois no puede encontrar la informacion comprobamos si en country_indic esta el ISO2
                    # data = self.country_dataframe.loc[self.country_dataframe['Code']==country_indic]
                    data = pycty.countries.get(alpha_2=country_indic)
                    
                    # if data.empty:
                    if not data:
                        # si no se corresponde con ningun ISO2 devolvemos el id del ASN
                        # id_retrieve = as_name.replace('AS','')
                        # data = {'Code':[id_retrieve],'Name': [id_retrieve]}
                        # data = pd.DataFrame.from_dict(data)
                        id_retrieve = as_name.replace('AS','')
                        data = {
                        'alpha_2' : id_retrieve, 
                        'name' : id_retrieve, 
                        'flag' : id_retrieve
                        }
                        data = DefaultMunch.fromDict(data)
                    return data

                # filtramos la informacion obtenida con el comando whois
                # obtenemos los campos con clave Country 
                filtered = self.get_country_from_whois_data(server_data)
                                
                if len(filtered) > 0:
                    # si hemos conseguido algun country del comando whois obtenemos el que mas se repita y lo devolvemos
                    dict_country_rept = Counter(filtered)
                    dict_country_rept['ZZ'] = 0
                    country_code = max(dict_country_rept, key = dict_country_rept.get)
                    # data = self.country_dataframe.loc[self.country_dataframe['Code']==country_code]
                    data = pycty.countries.get(alpha_2=country_code)
                else:
                    # si no hemos conseguido ningun country con el comando whois comproabmos la cadena country_indic
                    # data = self.country_dataframe.loc[self.country_dataframe['Code']==country_indic]
                    data = pycty.countries.get(alpha_2=country_indic)
                    # if not data.empty:
                    if data:
                        # si los hay algun country con formato ISO2 lo retornamos 
                        return data 
                    # si no hay ningun country con fromato ISO2 devolvemos el id del ASN
                    # id_retrieve = as_name.replace('AS','')
                    # data = {'Code':[id_retrieve],'Name': [id_retrieve]}
                    # data = pd.DataFrame.from_dict(data)
                    id_retrieve = as_name.replace('AS','')
                    data = {
                    'alpha_2' : id_retrieve, 
                    'name' : id_retrieve, 
                    'flag' : id_retrieve
                    }
                    data = DefaultMunch.fromDict(data)

            return data