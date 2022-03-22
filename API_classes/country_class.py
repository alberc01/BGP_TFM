from calendar import c
import pandas as pd
from ipwhois import IPWhois
import subprocess
import re
from collections import Counter

class Country:
    def __init__(self):
        # inicializamos la lectura del pandas dataframe
        self.country_dataframe = self.read_country_diminutives()
        
    def read_country_diminutives(self):
        # Leemos el archivo xlsx con pandas
        dfs = pd.read_excel("/home/alber/TFM-LINUX/BGP_TFM/country_info/country.xlsx", sheet_name= None)
        # Conseguimos los codigos de los paises
        partial_dfs = dfs['Codes']
        # Construimos un pandas con la informacion que es relevante
        final_df = pd.DataFrame(partial_dfs, columns=['ISO2', 'ISO3', 'CATEGORY', 'LIST NAME'])
        return final_df

    # def find_country_info(self, country_code, id):
    #     data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_code]
    #     if len(data.values) < 1:
    #         data = self.country_dataframe.loc[self.country_dataframe['ISO3']==country_code]
    #         if len(data.values) < 1:
    #             data = self.country_dataframe.loc[self.country_dataframe['LIST NAME']==country_code]
    #             if len(data.values) < 1:
    #                 data = self.country_dataframe.loc[self.country_dataframe['ISO2']==id]
    #                 if len(data.values) < 1:
    #                     data = self.country_dataframe.loc[self.country_dataframe['ISO3']==id]
    #                     if len(data.values) < 1:
    #                         data = self.country_dataframe.loc[self.country_dataframe['LIST NAME']==id]
    #                         if len(data.values) < 1 :
    #                             # try to get ASN country by whois
    #                             if id != 'ZZ':
    #                                 as_name  = 'AS'+ id
    #                             else:
    #                                 as_name = country_code.split(' ')
    #                                 regex = re.compile(r'^AS')
    #                                 filtered = [i for i in as_name if regex.match(i)]
    #                                 if len(filtered) > 0:
    #                                     as_name = filtered[0]
    #                                 else:
    #                                     data = {'ISO2':[id],'ISO3':[country_code],'CATEGORY':'UNKNOWN', 'LIST NAME': [country_code]}
    #                                     data = pd.DataFrame.from_dict(data)
    #                                     return data
    #                             try :
    #                                 server_data = subprocess.check_output(['whois',as_name])
                                    
    #                                 server_data = str(server_data).split('\\n')
                                    
    #                                 regex = re.compile(r'^country')
    #                                 filtered = [i.replace(" ", '').replace("country:", '') for i in server_data if regex.match(i)]
                                
                                    
    #                                 if len(filtered) > 0:
    #                                     dict_country_rept = Counter(filtered)
    #                                     dict_country_rept['ZZ'] = 0
    #                                     country_code = max(dict_country_rept, key = dict_country_rept.get)
                                        
    #                                     data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_code]
    #                                 else:
    #                                     data = {'ISO2':[id],'ISO3':[country_code],'CATEGORY':'UNKNOWN', 'LIST NAME': [country_code]}
    #                                     data = pd.DataFrame.from_dict(data)
    #                             except:
    #                                 data = {'ISO2':[id],'ISO3':[country_code],'CATEGORY':'UNKNOWN', 'LIST NAME': [country_code]}
    #                                 data = pd.DataFrame.from_dict(data)

    #     return data

    def get_asn_from_string(self, frame):
        as_name = frame.split(' ') 
        regex = re.compile(r'^AS') 
        filtered = [i for i in as_name if regex.match(i)]
        return filtered
    
    def get_country_from_whois_data(self, frame):
        # filtramos la informacion obtenida con el comando whois
        server_data = str(frame).split('\\n')
        regex = re.compile(r'^country',re.IGNORECASE)
        regex_to_sub = re.compile(r'^country:',re.IGNORECASE)
        # obtenemos los campos con clave Country 
        filtered = [regex_to_sub.sub("",i.replace(" ", '')) for i in server_data if regex.match(i)]
        return filtered

    def is_iso2_fromat(self, frame):
        return  frame != 'ZZ' and len(frame.split(' ')) < 2 and frame != '' and frame.isnumeric()

    def find_country_info_V2(self, id, country_indic):
            data = self.country_dataframe.loc[self.country_dataframe['ISO2']==id]
            # comprobamos si el id esta en fromato ISO2
            if len(data.values) < 1:
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
                        data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_indic]
                        if data.empty:
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
                                    data = {'ISO2':['ZZ'],'ISO3':['UNKNOWN'],'CATEGORY':'UNKNOWN', 'LIST NAME': ['UNKNOWN']}
                                    data = pd.DataFrame.from_dict(data)
                                    return data
                        else:
                            return data
                try :
                    # hay alguna cadena ASN entre los prametros de entrada
                    # obtenemos la infomacion con el comando whois
                    server_data = subprocess.check_output(['whois',as_name])
                except:
                    # si el comando whois no puede encontrar la informacion comprobamos si en country_indic esta el ISO2
                    data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_indic]
                    if data.empty:
                        # si no se corresponde con ningun ISO2 devolvemos el id del ASN
                        id_retrieve = as_name.replace('AS','')
                        data = {'ISO2':[id_retrieve],'ISO3':[id_retrieve],'CATEGORY':'UNKNOWN', 'LIST NAME': [id_retrieve]}
                        data = pd.DataFrame.from_dict(data)
                    return data

                # filtramos la informacion obtenida con el comando whois
                # obtenemos los campos con clave Country 
                filtered = self.get_country_from_whois_data(server_data)
                                
                if len(filtered) > 0:
                    # si hemos conseguido algun country del comando whois obtenemos el que mas se repita y lo devolvemos
                    dict_country_rept = Counter(filtered)
                    dict_country_rept['ZZ'] = 0
                    country_code = max(dict_country_rept, key = dict_country_rept.get)
                    data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_code]
                else:
                    # si no hemos conseguido ningun country con el comando whois comproabmos la cadena country_indic
                    data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_indic]
                    if not data.empty:
                        # si los hay algun country con formato ISO2 lo retornamos 
                        return data 
                    # si no hay ningun country con fromato ISO2 devolvemos el id del ASN
                    id_retrieve = as_name.replace('AS','')
                    data = {'ISO2':[id_retrieve],'ISO3':[id_retrieve],'CATEGORY':'UNKNOWN', 'LIST NAME': [id_retrieve]}
                    data = pd.DataFrame.from_dict(data)

            return data