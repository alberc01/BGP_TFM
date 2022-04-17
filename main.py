from cmath import sin
from importlib import import_module
from ntpath import join
from API_classes.twitter_class import TwitterScrap
from API_classes.gDrive_class import GoogleDriveApi
import API_classes.utils as ut
from API_classes.parser_class import Parser
from API_classes.country_class import Country
from API_classes.GUI_class import Graphics
import string

import os
import json
import datetime
from collections import Counter

class Main():
    # Constructora e la clase, inicializa apis y archivos para la obtencion de informacion
    def __init__(self):
        # Inicializacion de cada uno de los objetos para realizar el scrapping de informacion
        self.scrapp = TwitterScrap()
        self.parser = Parser()
        self.gdrive = GoogleDriveApi()
        self.country_info = Country()
      
        # Obtenemos los datos ya guardados en la carpeta de google drive
        self.bgp_info, self.from_available_date, self.to_available_date  = self.get_BGP_data()

    # Funcion para obtener los datos disponibles en google drive
    def get_BGP_data(self):
        # Seleccionamos la carpeta de google drive con la informacion
        file, content = self.gdrive.download_file('1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        # Cargamos el contenido en forma de diccionario
        bgp_info = json.loads(content)
        # Obtenemos el nombre ya que este contiene la fecha mas antigua de los datos que se poseen
        from_ava_date = file['originalFilename'].replace(".json", "")
        # Obtenemos la fecha mas reciente para la cual se poseen datos
        to_ava_date = bgp_info['recent_date']
        return bgp_info, from_ava_date, to_ava_date

    # Funcion para inicializar el archivo que mas tarde sera actualizado cada cierto tiempo
    def store_inital_data(self):
        dic_info = {}
        # Obtenemos todos los datos posibles con la api de Twitter del usuario @bgpstream
        user_tweets = self.scrapp.scrap_info_by_user("bgpstream")
        # Realizamos el prmer filtrado de datos para poder diferenciar los tipos de tramas bgp publicados
        dic_info, last_date = self.parser.get_bgp_info_of_tweets(dic_info, user_tweets)

        # Construimos el nombre del archivo que sera guardado en google drive y lo escribimos (como medio de seguirdad)
        f_name = str(last_date)+".json"
        ut.write_dict_to_file(f_name, dic_info)

        # Guardamos el fichero en google drive
        list_of_files = [f_name]
        self.gdrive.upload_files(list_of_files,'1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        print("------------------------------Data saved------------------------------")

        # eliminamos el fichero escrito en local ya que este se encuentra en google drive
        os.remove(f_name)
    
    # Funcion utilizada para actualizar las fechas mas reciente y mas antigua por si estas tienen algun tipo de error
    def fix_dictionary_date(self):
        file, content = self.gdrive.download_file('1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        dict_data = json.loads(content)
        firstIter = True
        mindate = 0
        res = 0
        for k,v in dict_data.items():
            if k not in ['recent_date', 'last_date', 'max_id']:
                for item in v:
                    date_in_dict = datetime.datetime.strptime(item['raw']['date'], '%Y-%m-%d %H:%M:%S%z')
                    if firstIter:
                        firstIter = False
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']
                    elif date_in_dict > res:
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']

        dict_data["recent_date"] = str(res).lstrip(' ')
        dict_data["max_id"] = max_id
        self.gdrive.update_gdrive_file(file, json.dumps(dict_data,indent=4))
        print("------------------------------Data updated------------------------------")

    # Funcion par actualizar la fecha mas antigua y mas recinte de los datos obtenidos en el timeline de Twitter
    def update_dictionary_dates(self, dict_info):
        firstIter = True
        mindate = 0
        res = 0
        # Recorremos el diccionario en busqueda de las fechas mas reciente y mas antigua
        for k,v in dict_info.items():
            if k not in ['recent_date', 'last_date', 'max_id']:
                for item in v:
                    date_in_dict = datetime.datetime.strptime(item['raw']['date'], '%Y-%m-%d %H:%M:%S%z')
                    if firstIter:
                        firstIter = False
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']
                    elif date_in_dict > res:
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']
        
        # Fijamos el resultado en el diccionario
        dict_info["recent_date"] = str(res).lstrip(' ')
        dict_info["max_id"] = max_id

        return dict_info

    # Funcion para actualizar los datos nuevos publicados en Twitter, almacenando dicha informacion en google drive
    def update_data(self):
        
        file, content = self.gdrive.download_file('1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        dict_data = json.loads(content)
        since_id = int(dict_data['max_id'])

        user_tweets =  self.scrapp.scrap_info_by_user_between_dates(username="bgpstream",since_id=since_id)

        dic_info, last_date = self.parser.get_bgp_info_of_tweets(dict_data, user_tweets)
        
        dic_info = self.update_dictionary_dates(dic_info)

        self.gdrive.update_gdrive_file(file, json.dumps(dic_info,indent=4))
        print("------------------------------Data updated------------------------------")
        self.save_BGP_issues_by_country("dict_by_country_v3.json")
              
        return dict_data

    # Funcion para poblar el diccionario formateado de la informacion de caidas de servicio
    def populate_OT_info(self, OT_dict, out_dict):
        # Poblar el diccionario con la informacion de caidas
        for item in OT_dict:            
            # Llamada para averiguar el pais del asn correspondiente
            ctry= self.country_info.find_country_info_V2(item['id'], item['country'])
            # Obtencion del nombre del pais en funcion del codigo en formato ISO2
            ctry_key = ctry['Code'].values[0]
            # Obtencion de la fecha del problema
            date = item['raw']['date']

            # Si el pais se encontraba en el diccionario
            if ctry_key in out_dict:
                # Creamos la informacion del problema para asignarlo segun la fecha
                date_inf_ot = {
                                'ctry':ctry_key,
                                'ASN': 'AS' + item['id']
                }

                # Si ya existia algun problema en esa fecha concatenamos la nueva
                if date in out_dict[ctry_key]['OT_by_date']:
                    out_dict[ctry_key]['OT_by_date'][date].append(date_inf_ot)
                # Si la fecha no existe creamos el array correspondiente con la informacion pertinente
                else :
                    out_dict[ctry_key]['OT_by_date'][date] = [date_inf_ot]

                # Aumentamos el numero de incidencias de OT del pais
                out_dict[ctry_key]['OT_count'] += 1

                # Mantenemos un backlog de OT por lo que pueda pasar
                issue_inf = {
                        'text':item['raw']['text'],
                        'issue_date': date
                    }
                # Concatenamos al backlog OT el problema 
                out_dict[ctry_key]['issue_ot'].append(issue_inf)

             # Si el pais no se encontraba en el diccionario  
            else:
                # Creamos la informacion relevante por fecha
                date_inf_ot = {
                                'ctry':ctry_key,
                                'ASN': 'AS' + item['id']
                               }

                # Poblamos la informacion incial que almacenaremos de cada pais
                out_dict[ctry_key] = {
                    'ctry_fullname': ctry['Name'].values[0],
                    'OT_by_date': {date : [date_inf_ot]},
                    'OT_count': 1,
                    'HJ_by_date': {'injured': {}, 'causer': {}},
                    'HJ_count': {'injured_count': 0, 'causer_count':0},
                    'HJ_autosabotage': {},
                    'issue_ot':[{
                        'text':item['raw']['text'],
                        'issue_date':date
                    }],
                    'issue_hj':{
                            'inju': [],
                            'causer': []
                            }
                }

        return out_dict

    # Funcion para obtener las partes correspondientes de causante y perjudicado en un incidente de tipo secuestro
    def get_hj_asns_from_string(self, text):
        # Separamos por comas el contenido del tweet
        raw_tex = text.split(',')
        # Obtenemos el separador principal que es el guion
        index_of = raw_tex.index('-')

        # Volvemos a juntar el resultado
        inju_string = "".join(raw_tex[0:index_of])
        caus_string = "".join(raw_tex[index_of:])

        # Obtenemos el ASN del perjudicado y limpiamos la cadena AS del resultado
        asn_i = self.country_info.get_asn_from_string(inju_string)
        for index, value in enumerate(asn_i):
            asn_i[index] = value.replace('\u2026','')

        # Obtenemos el ASN del causante y limpiamos la cadena AS del resultado
        asn_c = self.country_info.get_asn_from_string(caus_string)
        for index, value in enumerate(asn_c):
            asn_c[index] = value.replace('\u2026','')

        # Retornamos el array correspondiente del resultado obtenido
        return asn_i, asn_c

    # Funcion para poblar el diccionario formateado de la informacion de secuestros
    def populate_HJ_info(self, HJ_dict, out_dict):

        # Poblar el diccionario de salida con la informacion de secuestros
        for item in HJ_dict:
            # Obtenemos la fecha del problema BGP
            date = item['raw']['date']
            
            # Obtenemos el pais perjudicado
            injured = item['injured']
            inj_ctry = self.country_info.find_country_info_V2(injured['issue'],injured['country'])
            inj_ctry_key = inj_ctry['Code'].values[0]

            # Obtenemos el pais causante
            causer = item['causer']
            cau_ctry = self.country_info.find_country_info_V2(causer['company'],causer['country'])
            cau_ctry_key = cau_ctry['Code'].values[0]

            # Obtenemos el asn del pais perjudicado y causante
            inj_asn, cau_asn =self.get_hj_asns_from_string(item['raw']['text'])

            # inj_asn = self.country_info.get_asn_from_string(injured['issue'])
            # cau_asn = self.country_info.get_asn_from_string(causer['company'],causer['country'])
            if cau_asn == [] or inj_asn == []:
                print('aio')

            # Creamos la informacion relevante del problema que sera almacenado por fecha
            date_inf_hj = {
                'ctry_inj': inj_ctry_key,
                'ctry_cau': cau_ctry_key,
                'ASN_cau': cau_asn,
                'ASN_inj': inj_asn
            }
            # Si el pais causante es disntinto del pais perjudicado
            if inj_ctry_key != cau_ctry_key:

                ## POBLAMOS LA INFORMACION DEL PERJUDICADO ##
                # Si el pais se encuntra en el diccionario
                if inj_ctry_key in out_dict:

                    # Si ya existia algun problema con la misma fecha lo concatenamos a la lista 
                    if date in out_dict[inj_ctry_key]['HJ_by_date']['injured']:
                        out_dict[inj_ctry_key]['HJ_by_date']['injured'][date].append(date_inf_hj)
                    # Si no existia ningun problema con esa fecha inicializamos el diccionario con la informacion correspondiente
                    else :
                        out_dict[inj_ctry_key]['HJ_by_date']['injured'][date] = [date_inf_hj]

                    # Aumentamos el numero de problemas de ese pais como perjudicado
                    out_dict[inj_ctry_key]['HJ_count']['injured_count'] += 1
                    
                    # Mantenemos un backlog de HJ con el problema por lo que pueda pasar
                    issue_inf = {
                            'text':item['raw']['text'],
                            'issue_date': date
                        }
                    # Concatenamos el problema al backlog de HJ
                    out_dict[inj_ctry_key]['issue_hj']['inju'].append(issue_inf)
                # Si el pais no se encuntra en el diccionario
                else:
                    # Poblamos la informacion incial que almacenaremos de cada pais
                    out_dict[inj_ctry_key] = {
                        'ctry_fullname': inj_ctry['Name'].values[0],
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured': {date: [date_inf_hj]},
                                       'causer': {}},
                        'HJ_count': {'injured_count': 1, 'causer_count':0} ,
                        'HJ_autosabotage': {},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [{'text':item['raw']['text'],'issue_date': date}],
                            'causer': []
                        }
                    }

                ## POBLAMOS LA INFORMACION DEL CAUSANTE ##
                # Si el pais se encuntra en el diccionario
                if cau_ctry_key in out_dict:
                    # Si ya existia algun problema con la misma fecha lo concatenamos a la lista       
                    if date in out_dict[cau_ctry_key]['HJ_by_date']['causer']:
                        out_dict[cau_ctry_key]['HJ_by_date']['causer'][date].append(date_inf_hj)
                    # Si no existia ningun problema con esa fecha inicializamos el diccionario con la informacion correspondiente
                    else :
                        out_dict[cau_ctry_key]['HJ_by_date']['causer'][date] = [date_inf_hj]
                    # Aumentamos el contador del pais como causante de secuestros
                    out_dict[cau_ctry_key]['HJ_count']['causer_count'] += 1

                    # Mantenemos un backlog por lo que pueda pasar
                    issue_inf = {
                            'text':item['raw']['text'],
                            'issue_date':item['raw']['date']
                        }
                    # Concatemos el problema al backlog correspondiente
                    out_dict[cau_ctry_key]['issue_hj']['causer'].append(issue_inf)
                # Si el pais no se encuentra en el diccionario
                else:
                    # Poblamos la informacion incial que almacenaremos de cada pais
                    out_dict[cau_ctry_key] = {
                        'ctry_fullname': cau_ctry['Name'].values[0],
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{},
                                       'causer': {date: [date_inf_hj]}},
                        'HJ_count': {'injured_count': 0, 'causer_count':1} ,
                        'HJ_autosabotage': {},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [],
                            'causer': [{'text':item['raw']['text'],'issue_date': date}]
                        }
                    }
            
            # Si el causante y el perjudicado son los mismos se califica como autosabotaje
            else:
                # Si el pais ya se encontraba en el diccionario
                if cau_ctry_key in out_dict:
                    # Si ya habia algun problema en esa fecha concatenamos la nueva
                    if date in out_dict[inj_ctry_key]['HJ_autosabotage']:
                        out_dict[inj_ctry_key]['HJ_autosabotage'][date].append(date_inf_hj)
                    # Si no habia ningun problema todavia, inicializamos el array con la informacion correspondiente
                    else:
                        out_dict[inj_ctry_key]['HJ_autosabotage'][date] = [date_inf_hj]
                # Si el pais no se encontraba en el diccionario todavia
                else:
                    # Poblamos la informacion incial que almacenaremos de cada pais
                    out_dict[inj_ctry_key] = {
                        'ctry_fullname': inj_ctry['Name'].values[0],
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{}, 'causer': {}},
                        'HJ_count': {'injured_count': 0, 'causer_count':0} ,
                        'HJ_autosabotage': {date : [date_inf_hj]},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [],
                            'causer': []
                        }
                    }
        return out_dict
    
    # Funcion para poblar el diccionario formateado para la aplicacion
    def save_BGP_issues_by_country(self, filename):
        # Diccionario con la informacion de cortes de servicio
        OT_dict = self.bgp_info['OT']
        # Diccionario con la informacion de secuestros
        HJ_dict = self.bgp_info['HJ']
        
        # Diccionario auxiliar donde guardaremos la informacion
        dict_by_country = {}

        # Poblar el diccionario con la informacion de caidas
        dict_by_country = self.populate_OT_info(OT_dict, dict_by_country)

        # Poblar el diccionario con la informacion de secuestros
        dict_by_country = self.populate_HJ_info(HJ_dict, dict_by_country)
        
        # Escritura en el diccionario de las fechas reciente y antigua
        dict_by_country['oldest_date'] = self.from_available_date
        dict_by_country['most_recent_date'] = self.to_available_date

        # Escritura del diccionario en un archivo de backup
        ut.write_dict_to_file(filename, dict_by_country)

        return dict_by_country
    
    # Funcion para inciar el modo GUI de la aplicacion
    def init_GUI(self):
        self.gui = Graphics()
        
    
# Main().fix_dictionary_date()
# Main().store_inital_data()
# Main().update_data()
Main().init_GUI()
