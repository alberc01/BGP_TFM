from cmath import sin
from importlib import import_module
from API_classes.twitter_class import TwitterScrap
from API_classes.gDrive_class import GoogleDriveApi
from API_classes.writer_class import Writer
from API_classes.parser_class import Parser
from API_classes.country_class import Country

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
        self.writer = Writer()
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
        self.writer.write_dict_to_file(f_name, dic_info)

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

    # Funcion no utilizada #TODO
    def update_dictionary_dates(self, dict_info):
        firstIter = True
        mindate = 0
        res = 0
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
              
        return dict_data

    def country_BGP_issues(self):
        OT_dict = self.bgp_info['OT']
        HJ_dict = self.bgp_info['HJ']

        dict_by_country = {}

        for item in OT_dict:

            # ctry= self.country_info.find_country_info(item['country'], item['id']).
            ctry= self.country_info.find_country_info_V2(item['id'], item['country'])
            ctry_key = ctry['ISO2'].values[0]
            date = item['raw']['date']
            if str(date) == '2022-01-27 00:07:16+00:00':
                print('aqui')

            if ctry_key == '' or ctry_key == ' ':
                print('aqui') 

            if ctry_key in dict_by_country:

                if date in dict_by_country[ctry_key]['OT_by_date']:
                    dict_by_country[ctry_key]['OT_by_date'][date] += 1
                else :
                    dict_by_country[ctry_key]['OT_by_date'][date] = 1

                dict_by_country[ctry_key]['OT_count'] += 1
                issue_inf = {
                        'text':item['raw']['text'],
                        'issue_date': date
                    }
                dict_by_country[ctry_key]['issue'].append(issue_inf)
                
            else:
                dict_by_country[ctry_key] = {
                    'ctry_fullname': ctry['LIST NAME'].values[0],
                    'OT_by_date': {date: 1},
                    'OT_count': 1,
                    'HJ_by_date': {'injured': {}, 'causer': {}},
                    'HJ_count': {'injured_count': 0, 'causer_count':0},
                    'HJ_autosabotage': {},
                    'issue':[{
                        'text':item['raw']['text'],
                        'issue_date':date
                    }]
                }

        for item in HJ_dict:
            date = item['raw']['date']
            if str(date) == '2022-01-27 00:07:16+00:00':
                print('aqui')

            injured = item['injured']
            inj_ctry = self.country_info.find_country_info_V2(injured['issue'],injured['country'])
            inj_ctry_key = inj_ctry['ISO2'].values[0]

            causer = item['causer']
            cau_ctry = self.country_info.find_country_info_V2(causer['company'],causer['country'])
            cau_ctry_key = cau_ctry['ISO2'].values[0]

            if cau_ctry_key == '' or inj_ctry_key == '':
                print('aqui')

            if inj_ctry_key != cau_ctry_key:
                if inj_ctry_key in dict_by_country:
                    
                    if date in dict_by_country[inj_ctry_key]['HJ_by_date']['injured']:
                        dict_by_country[inj_ctry_key]['HJ_by_date']['injured'][date].append([1,cau_ctry_key])
                    else :
                        dict_by_country[inj_ctry_key]['HJ_by_date']['injured'][date] = [[1,cau_ctry_key]]

                    dict_by_country[inj_ctry_key]['HJ_count']['injured_count'] += 1

                    issue_inf = {
                            'text':item['raw']['text'],
                            'issue_date': date
                        }
                    dict_by_country[inj_ctry_key]['issue'].append(issue_inf)

                else:
                    dict_by_country[inj_ctry_key] = {
                        'ctry_fullname': inj_ctry['LIST NAME'].values[0],
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured': {date: [[1,cau_ctry_key]]}, 'causer': {}},
                        'HJ_count': {'injured_count': 1, 'causer_count':0} ,
                        'HJ_autosabotage': {},
                        'issue':[{
                            'text':item['raw']['text'],
                            'issue_date': date
                        }]
                    }

                if cau_ctry_key in dict_by_country:

                    if date in dict_by_country[cau_ctry_key]['HJ_by_date']['causer']:
                        dict_by_country[cau_ctry_key]['HJ_by_date']['causer'][date].append([1,inj_ctry_key])
                    else :
                        dict_by_country[cau_ctry_key]['HJ_by_date']['causer'][date] = [[1,inj_ctry_key]]

                    dict_by_country[cau_ctry_key]['HJ_count']['causer_count'] += 1
                    issue_inf = {
                            'text':item['raw']['text'],
                            'issue_date':item['raw']['date']
                        }

                    dict_by_country[cau_ctry_key]['issue'].append(issue_inf)

                else:
                    dict_by_country[cau_ctry_key] = {
                        'ctry_fullname': cau_ctry['LIST NAME'].values[0],
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{}, 'causer': {date: [[1,inj_ctry_key]]}},
                        'HJ_count': {'injured_count': 0, 'causer_count':1} ,
                        'HJ_autosabotage': {},
                        'issue':[{
                            'text':item['raw']['text'],
                            'issue_date':item['raw']['date']
                        }]
                    }
            else:
                if cau_ctry_key in dict_by_country:
                    if date in dict_by_country[inj_ctry_key]['HJ_autosabotage']:
                        dict_by_country[inj_ctry_key]['HJ_autosabotage'][date] += 1
                    else:
                        dict_by_country[inj_ctry_key]['HJ_autosabotage'][date] = 1
                else:
                    dict_by_country[cau_ctry_key] = {
                        'ctry_fullname': cau_ctry['LIST NAME'].values[0],
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{}, 'causer': {}},
                        'HJ_count': {'injured_count': 0, 'causer_count':0} ,
                        'HJ_autosabotage': {date: 1},
                        'issue':[{
                            'text':item['raw']['text'],
                            'issue_date':item['raw']['date']
                        }]
                    }
                

        dict_by_country['oldest_date'] = self.from_available_date
        dict_by_country['most_recent_date'] = self.to_available_date
        self.writer.write_dict_to_file("dict_by_country_v2.json", dict_by_country)
        return dict_by_country
    
# Main().fix_dictionary_date()
# Main().store_inital_data()
# Main().update_data()
Main().country_BGP_issues()
