from API_classes.twitter_class import TwitterScrap
from API_classes.gDrive_class import GoogleDriveApi
import API_classes.utils as ut
from API_classes.parser_class import Parser
from API_classes.country_class import Country
import os
import json
import datetime
import pycountry

Classified_By_BgpRS = "Folder_id_Classified_By_BgpRS"
Posible_Extended_Data = "Folder_id_Posible_Extended_Data"    
Scrapped_From_Twitter = "Folder_id_Scrapped_From_Twitter"

class Data_clasffier():
    # Constructora e la clase, inicializa apis y archivos para la obtencion de informacion
    def __init__(self):
        # Inicializacion de cada uno de los objetos para realizar el scrapping de informacion
        self.scrapp = TwitterScrap()
        self.parser = Parser()
        self.gdrive = GoogleDriveApi()
        self.country_info = Country()
      
        # Obtenemos los datos ya guardados en la carpeta de google drive
        self.bgp_info, self.from_available_date, self.to_available_date  = self.get_BGP_data()
    
    # Funcion para cargar inicialmente la apliacion
    def get_content_file_to_make_work_BgpRS(self):
        file, file_content = self.gdrive.download_file(Posible_Extended_Data)
        if file and file_content:
            content = json.loads(file_content)
        else:
            file, file_content = self.gdrive.download_file(Classified_By_BgpRS)
            if file and file_content:
                content = json.loads(file_content)

        return content

    # Funcion para recargar los datos despues de obtener informacion de Twitter
    def reload_info(self):
        self.bgp_info, self.from_available_date, self.to_available_date  = self.get_BGP_data()

    # Funcion para obtener los datos disponibles en google drive
    def get_BGP_data(self):
        # Seleccionamos la carpeta de google drive con la informacion
        file, content = self.gdrive.download_file(Scrapped_From_Twitter)
        # Cargamos el contenido en forma de diccionario
        bgp_info = json.loads(content)
        # Obtenemos el nombre ya que este contiene la fecha mas antigua de los datos que se poseen
        from_ava_date = file['originalFilename'].replace(".json", "")
        # Obtenemos la fecha mas reciente para la cual se poseen datos
        to_ava_date = bgp_info['recent_date']
        return bgp_info, from_ava_date, to_ava_date

    # Funcion para inicializar el archivo que mas tarde sera actualizado cada cierto tiempo
    def store_inital_data(self,drive_folder):
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
        self.gdrive.upload_files(list_of_files, drive_folder)
        print("------------------------------Data saved------------------------------")

        # eliminamos el fichero escrito en local ya que este se encuentra en google drive
        os.remove(f_name)
    
    # Funcion utilizada para actualizar las fechas mas reciente y mas antigua por si estas tienen algun tipo de error
    def fix_dictionary_date(self):
        file, content = self.gdrive.download_file(Scrapped_From_Twitter)
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

    # Funcion para poblar el diccionario formateado de la informacion de caidas de servicio
    def populate_OT_info(self, OT_dict, out_dict):
        # Poblar el diccionario con la informacion de caidas
        for item in OT_dict:            
            # Llamada para averiguar el pais del asn correspondiente
            ctry= self.country_info.find_country_info_V2(item['id'], item['country'])
            # Obtencion del nombre del pais en funcion del codigo en formato ISO2
            # ctry_key = ctry['Code'].values[0]
            ctry_key = ctry.alpha_2
            # Obtencion de la fecha del problema
            date = item['raw']['date']

            # Si el pais se encontraba en el diccionario
            if ctry_key in out_dict:
                issue_url = item['raw']['text']
                issue_url = issue_url.split(',')[-1].split('\u2026')[-1].strip()

                # Creamos la informacion del problema para asignarlo segun la fecha
                date_inf_ot = {
                                'ctry':ctry_key,
                                'ASN': 'AS' + item['id'],
                                'url': issue_url,
                                'scrapped_from_url': ut.get_ot_characteristics(issue_url),
                                'text':item['raw']['text']
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
                issue_url = item['raw']['text']
                issue_url = issue_url.split(',')[-1].split('\u2026')[-1].strip()
                
                # Creamos la informacion relevante por fecha
                date_inf_ot = {
                                'ctry':ctry_key,
                                'ASN': 'AS' + item['id'],
                                'url': issue_url,
                                'scrapped_from_url': ut.get_ot_characteristics(issue_url),
                                'text':item['raw']['text']
                }

                # Poblamos la informacion incial que almacenaremos de cada pais
                out_dict[ctry_key] = {
                    # 'ctry_fullname': ctry['Name'].values[0],
                    'ctry_fullname': ctry.name,
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

    # Funcion para poblar el diccionario formateado de la informacion de secuestros
    def populate_HJ_info(self, HJ_dict, out_dict):

        # Poblar el diccionario de salida con la informacion de secuestros
        for item in HJ_dict:
            # Obtenemos la fecha del problema BGP
            date = item['raw']['date']
            
            # Obtenemos el pais perjudicado
            injured = item['injured']
            inj_ctry = self.country_info.find_country_info_V2(injured['issue'],injured['country'])
            # inj_ctry_key = inj_ctry['Code'].values[0]
            inj_ctry_key = inj_ctry.alpha_2

            # Obtenemos el pais causante
            causer = item['causer']
            cau_ctry = self.country_info.find_country_info_V2(causer['company'],causer['country'])
            # cau_ctry_key = cau_ctry['Code'].values[0]
            cau_ctry_key = cau_ctry.alpha_2

            # Obtenemos el asn del pais perjudicado y causante
            inj_asn, cau_asn =self.get_hj_asns_from_string(item['raw']['text'])

            issue_url = item['raw']['text']
            issue_url = issue_url.split(',')[-1].split('\u2026')[-1].strip()

            # Creamos la informacion relevante del problema que sera almacenado por fecha
            date_inf_hj = {
                'ctry_inj': inj_ctry_key,
                'ctry_cau': cau_ctry_key,
                'ASN_cau': cau_asn,
                'ASN_inj': inj_asn,
                'url': issue_url,
                'scrapped_from_url': ut.get_hj_characteristics(issue_url),
                'text':item['raw']['text'],
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
                        # 'ctry_fullname': inj_ctry['Name'].values[0],
                        'ctry_fullname': inj_ctry.name,
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
                        # 'ctry_fullname': cau_ctry['Name'].values[0],
                        'ctry_fullname': cau_ctry.name,
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
                        # 'ctry_fullname': inj_ctry['Name'].values[0],
                        'ctry_fullname': inj_ctry.name,
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

        print("SAVING OT DATA")
        # Poblar el diccionario con la informacion de caidas
        dict_by_country = self.populate_OT_info(OT_dict, dict_by_country)

        print("SAVING HJ DATA")
        # Poblar el diccionario con la informacion de secuestros
        dict_by_country = self.populate_HJ_info(HJ_dict, dict_by_country)


        print("UPDATING DATES")
        # Escritura en el diccionario de las fechas reciente y antigua
        dict_by_country['oldest_date'] = self.from_available_date
        dict_by_country['most_recent_date'] = self.to_available_date

        print("WRITING FILE")
        # Escritura del diccionario en un archivo de backup
        ut.write_dict_to_file(filename, dict_by_country)
        list_of_files = [filename]

        print("UPLOADING DATA TO GDRIVE")
        files = self.gdrive.get_files_at_directory(Classified_By_BgpRS)
        if len(files) < 1:
            self.gdrive.upload_files(list_of_files, Classified_By_BgpRS)
        else:
            file, content = self.gdrive.download_file(Classified_By_BgpRS)
            self.gdrive.update_gdrive_file(file, json.dumps(dict_by_country,indent=4))
            
        os.remove(filename)

        return dict_by_country
    
    #TODO FUNCION PARA GENERAR DATOS SITNTETICOS
    def generate_synthetic_BGP_issues(self, number=100, filename="Output.json"):
        i=0
        while i<1000:
            print(str(i)+"\n")
            i+=1
        return True
    
    # Funcion para añadir eventos de un archivo al conjunto de datos leidos por la aplicacion
    def load_bgp_issues_from_file(self, source_file, dest_file, start=None, end= None):
        if not start:
            start = 0
        
        src_content = open(source_file)
        src_data = json.load(src_content)

        file, intermediate_content = self.gdrive.download_file(Posible_Extended_Data)
        if file and intermediate_content:
            mid_data = json.loads(intermediate_content)
        else:
            file, intermediate_content = self.gdrive.download_file(Classified_By_BgpRS)
            if file and intermediate_content:
                mid_data = json.loads(intermediate_content)
            else:
                mid_data = {
                    "oldest_date":ut.get_current_date_string(),
                    "most_recent_date":ut.get_current_date_string(),
                }

        if not end:
            end = len(src_data)

        item_count = 0
        for item in src_data[start:end]:
            item_count+=1
            if item['event_type'] == 'Outage':
                mid_data = self.classify_OT_into_app(item, mid_data)
            elif item['event_type'] == 'Possible Hijack':
                mid_data = self.classify_HJ_into_app(item, mid_data)
            # elif item['event_type'] == 'BGP Leak':
            #     mid_data = self.classify_LK_into_app(item, mid_data)

            if item_count % 100 ==0:
                print("Se han añadido "+ str(item_count) + " elementos por el momento. Por favor, siga esperando.")
                
        ut.write_dict_to_file(dest_file, mid_data)
        print("UPLOADING STATIC DATA TO GDRIVE")
        list_of_files = [dest_file]
        files = self.gdrive.get_files_at_directory(Posible_Extended_Data)
        if len(files) < 1:
            self.gdrive.upload_files(list_of_files, Posible_Extended_Data)
        else:
            file, content = self.gdrive.download_file(Posible_Extended_Data)
            self.gdrive.update_gdrive_file(file, json.dumps(mid_data,indent=4))
            
        os.remove(dest_file)

        return True

    def classify_OT_into_app(self,elem,ret_data):
        
            # "starttime_day": 19, 
            # "affected_prefixes": 18, 
            # "endtime_time": null, 
            # "event_type": "Outage", 
            # "starttime_year": 2018, 
            # "outage asn": 197293, 
            # "moredetail": "https://bgpstream.com/event/143159", 
            # "endtime_year": null, 
            # "endtime_month": null, 
            # "starttime_month": 7, 
            # "country": null, 
            # "endtime_day": null, 
            # "starttime_time": "18:12:00"

        if not elem['country']:
            try:
                country = self.country_info.get_as_country_by_whois("AS" + str(elem['outage asn'])).alpha_2
            except:
                country = str(elem['outage asn'])
        else:
            country = elem['country']

        date_string = str(elem['starttime_year']) 
        date_string += '-' + str(elem['starttime_month'])
        date_string += '-' + str(elem['starttime_day'])
        date_string += ' '+ str(elem['starttime_time']) + '+00:00'
        new_date_key = ut.string_to_datetime(date_string)

        oldest_date = ut.string_to_datetime(ret_data["oldest_date"])
        if  oldest_date > new_date_key:
            ret_data["oldest_date"] = str(new_date_key)
        recent_date = ut.string_to_datetime(ret_data["most_recent_date"]) 
        if recent_date < new_date_key:
            ret_data["most_recent_date"] = str(new_date_key)

        new_text = 'BGP,OT,'+ 'AS'+str(elem['outage asn'])+','+ country + ',-,' + 'Outage affected '+ str(elem['affected_prefixes'])+ ' prefixes,'+ elem['moredetail']
        custom_ot_dict ={
                'ctry': country,
                'ASN': 'AS'+str(elem['outage asn']),
                'url': elem['moredetail'],
                'scrapped_from_url':[ut.get_ot_characteristics(elem['moredetail'])],
                'text': "Static data charged on main dict" + new_text

            }
        if country in ret_data.keys():
            otdates = ret_data[country]['OT_by_date']# Dict{fecha: dict{List [ dict{ctry:, ASN:, rul:, scrapped_from_url:, text:}]}
            ot_cont = ret_data[country]['OT_count'] # numero += 1
            issueot = ret_data[country]['issue_ot'] # List[dict{text:, issue_date:}]
        
            if str(new_date_key) in otdates.keys():
                otdates[str(new_date_key) ].append(custom_ot_dict)
            else:
                otdates[str(new_date_key) ] = [custom_ot_dict]

            ret_data[country]['OT_by_date'] = otdates

            issueot_dict = {'text': new_text,'issue_date':str(new_date_key) }
            issueot.append(issueot_dict)
            ret_data[country]['issue_ot'] = issueot
            
            ot_cont+=1
            ret_data[country]['OT_count'] = ot_cont
        else:
            full_name = pycountry.countries.get(alpha_2=country)
            if full_name:
                full_name = full_name.name
            else:
                full_name = country
            dict_in_country ={
                    'ctry_fullname': full_name,
                    'OT_by_date': {str(new_date_key)  : [custom_ot_dict]},
                    'OT_count': 1,
                    'HJ_by_date': {'injured': {}, 'causer': {}},
                    'HJ_count': {'injured_count': 0, 'causer_count':0},
                    'HJ_autosabotage': {},
                    'issue_ot':[{
                        'text': new_text,
                        'issue_date':str(new_date_key)
                    }],
                    'issue_hj':{
                            'inju': [],
                            'causer': []
                            }
                }
            
            ret_data[country] = dict_in_country


        return ret_data

    def classify_HJ_into_app(self,elem,ret_data):
            # "starttime_day": 19, 
            # "expected asn": 39948, 
            # "endtime_time": null, 
            # "event_type": "Possible Hijack", 
            # "detected_aspath": [
            #     27553, 
            #     3356, 
            #     3549, 
            #     7049, 
            #     7049, 
            #     264859
            # ], 
            # "country": null, 
            # "moredetail": "https://bgpstream.com/event/143165", 
            # "starttime_year": 2018, 
            # "endtime_year": null, 
            # "peers": 173, 
            # "endtime_month": null, 
            # "starttime_month": 7, 
            # "detected_prefix": "192.169.12.0/24", 
            # "expected_prefix": "192.169.12.0/22", 
            # "endtime_day": null, 
            # "detected asn": 264859, 
            # "starttime_time": "21:20:00"
        if not elem['country']:
            try:
                country_inj = self.country_info.get_as_country_by_whois("AS" + str(elem['expected asn'])).alpha_2
            except:
                country_inj = str(elem['expected asn'])
        else:
            country_inj = elem['country']
        
        try:
            country_cau = self.country_info.get_as_country_by_whois("AS" + str(elem['detected asn'])).alpha_2
        except:
            country_cau = str(elem['detected asn'])

        date_string = str(elem['starttime_year']) 
        date_string += '-' + str(elem['starttime_month'])
        date_string += '-' + str(elem['starttime_day'])
        date_string += ' '+ str(elem['starttime_time']) + '+00:00'
        new_date_key = ut.string_to_datetime(date_string)

        oldest_date = ut.string_to_datetime(ret_data["oldest_date"])
        if  oldest_date > new_date_key:
            ret_data["oldest_date"] = str(new_date_key)
        recent_date = ut.string_to_datetime(ret_data["most_recent_date"]) 
        if recent_date < new_date_key:
            ret_data["most_recent_date"] = str(new_date_key)
        
        new_text = "BGP,HJ,hijacked prefix " + 'AS'+str(elem['expected asn']) + " " + elem['expected_prefix'] + ", , "+ country_inj+',-,'+ 'By  AS' + str(elem['detected asn']) + ', ' +country_cau,', '+ elem['moredetail']
        new_dict = {
            "ctry_inj": country_inj,
            "ctry_cau": country_cau,
            "ASN_cau": ["AS" + str(elem['detected asn'])],
            "ASN_inj": ["AS" + str(elem['expected asn'])],
            "url": elem['moredetail'],
            "scrapped_from_url": [
                        [str(i) for i in elem['detected_aspath']],
                        ['PEERS AFFECTED '+ str(elem['peers'])] 
            ],
            "text": new_text
        }
        
        if country_inj == country_cau:
            if country_cau in ret_data.keys():
                HJ_autosab = ret_data[country_inj]['HJ_autosabotage'] # Dic{fecha: Lis[dic{'ctry_inj": ,ctry_cau:, ASN_cau:[] , ASN_inj:[], url,scrapped_from_url : [ASNs], text:}
                
                if str(new_date_key) in HJ_autosab.keys():
                    HJ_autosab[str(new_date_key)].append(new_dict)
                else:
                    HJ_autosab[str(new_date_key)] = [new_dict]

                ret_data[country_inj]['HJ_autosabotage'] = HJ_autosab
            else:
                full_name = pycountry.countries.get(alpha_2=country_inj)
                if full_name:
                    full_name = full_name.name
                else:
                    full_name = country_inj
                dict_autosab = {
                        # 'ctry_fullname': inj_ctry['Name'].values[0],
                        'ctry_fullname': full_name,
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{}, 'causer': {}},
                        'HJ_count': {'injured_count': 0, 'causer_count':0} ,
                        'HJ_autosabotage': {str(new_date_key) : [new_dict]},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [],
                            'causer': []
                        }
                    }
                ret_data[country_inj] = dict_autosab
        else:
            if country_inj in ret_data.keys():
                HJ_INJ_dates = ret_data[country_inj]['HJ_by_date']['injured']# Dict{fecha: dict{List [ dict{ctry:, ASN:, rul:, scrapped_from_url:, text:}]}
                HJ_INJ_cont = ret_data[country_inj]['HJ_count']['injured_count']  # numero += 1
                issue_HJ_INJ = ret_data[country_inj]['issue_hj']['inju'] # List[dict{text:, issue_date:}]


                if str(new_date_key) in HJ_INJ_dates.keys():
                    HJ_INJ_dates[str(new_date_key)].append(new_dict)
                else:
                    HJ_INJ_dates[str(new_date_key)] = [new_dict]

                ret_data[country_inj]['HJ_by_date']['injured'] = HJ_INJ_dates

                HJ_INJ_cont+=1
                ret_data[country_inj]['HJ_count']['injured_count'] = HJ_INJ_cont

                issue_hj_inj_dict = {'text': new_text,'issue_date':str(new_date_key)}
                issue_HJ_INJ.append(issue_hj_inj_dict)
                ret_data[country_inj]['issue_hj']['inju'] = issue_HJ_INJ
            else:
                full_name = pycountry.countries.get(alpha_2=country_inj)
                if full_name:
                    full_name = full_name.name
                else:
                    full_name = country_inj
                inju_dict= {
                        # 'ctry_fullname': inj_ctry['Name'].values[0],
                        'ctry_fullname': full_name,
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured': {str(new_date_key): [new_dict]},
                                       'causer': {}},
                        'HJ_count': {'injured_count': 1, 'causer_count':0} ,
                        'HJ_autosabotage': {},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [{'text':new_text,'issue_date': str(new_date_key)}],
                            'causer': []
                        }
                    }

                ret_data[country_inj] = inju_dict

            if country_cau in ret_data.keys():
                HJ_CAU_dates = ret_data[country_cau]['HJ_by_date']['causer']# Dict{fecha: dict{List [ dict{ctry:, ASN:, rul:, scrapped_from_url:, text:}]}
                HJ_CAU_cont = ret_data[country_cau]['HJ_count']['causer_count'] # numero += 1
                issue_HJ_CAU = ret_data[country_cau]['issue_hj']['causer'] # List[dict{text:, issue_date:}]

                if str(new_date_key) in HJ_CAU_dates.keys():
                    HJ_CAU_dates[str(new_date_key)].append(new_dict)
                else:
                    HJ_CAU_dates[str(new_date_key)] = [new_dict]

                ret_data[country_cau]['HJ_by_date']['causer'] = HJ_CAU_dates

                HJ_CAU_cont+=1
                ret_data[country_cau]['HJ_count']['causer_count'] = HJ_CAU_cont

                issue_hj_cau_dict = {'text': new_text,'issue_date':str(new_date_key)}
                issue_HJ_CAU.append(issue_hj_cau_dict)
                ret_data[country_cau]['issue_hj']['causer']  = issue_HJ_CAU
            else:
                full_name = pycountry.countries.get(alpha_2=country_cau)
                if full_name:
                    full_name = full_name.name
                else:
                    full_name = country_cau
                cau_dict = {
                        # 'ctry_fullname': cau_ctry['Name'].values[0],
                        'ctry_fullname': full_name,
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{},
                                       'causer': {str(new_date_key): [new_dict]}},
                        'HJ_count': {'injured_count': 0, 'causer_count':1} ,
                        'HJ_autosabotage': {},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [],
                            'causer': [{'text':new_text,'issue_date': str(new_date_key)}]
                        }
                    }
                ret_data[country_cau] = cau_dict

        return ret_data

    def classify_LK_into_app(self,elem,ret_data):
            # "starttime_day": 18, 
            # "expected asn": 3549, 
            # "leaked_to": 2828, 
            # "endtime_time": "23:11:12", 
            # "event_type": "BGP Leak", 
            # "detected_aspath": [
            #     63774, 
            #     9607, 
            #     2516, 
            #     2828, 
            #     22625, 
            #     3356, 
            #     3549
            # ], 
            # "country": null, 
            # "moredetail": "https://bgpstream.com/event/142914", 
            # "starttime_year": 2018, 
            # "endtime_year": 2018, 
            # "peers": 7, 
            # "endtime_month": 7, 
            # "starttime_month": 7, 
            # "endtime_day": 18, 
            # "detected asn": 22625, 
            # "leaked_prefix": "68.66.40.0/24", 
            # "starttime_time": "14:14:16"
        if not elem['country']:
            try:
                country_inj = self.country_info.get_as_country_by_whois("AS" + str(elem['leaked_to'])).alpha_2
            except:
                country_inj = str(elem['leaked_to'])
        else:
            country_inj = elem['country']
        
        try:
            country_cau = self.country_info.get_as_country_by_whois("AS" + str(elem['detected asn'])).alpha_2
        except:
            country_cau = str(elem['detected asn'])

        date_string = str(elem['starttime_year']) 
        date_string += '-' + str(elem['starttime_month'])
        date_string += '-' + str(elem['starttime_day'])
        date_string += ' '+ str(elem['starttime_time']) + '+00:00'
        new_date_key = ut.string_to_datetime(date_string)

        oldest_date = ut.string_to_datetime(ret_data["oldest_date"])
        if  oldest_date > new_date_key:
            ret_data["oldest_date"] = str(new_date_key)
        recent_date = ut.string_to_datetime(ret_data["most_recent_date"]) 
        if recent_date < new_date_key:
            ret_data["most_recent_date"] = str(new_date_key)
        
        new_text = "BGP,HJ,LEAKED prefix " + 'AS'+str(elem['leaked_to']) + " " + elem['leaked_prefix'] + ' Usually anounced by '+ str(elem['expected asn'])+", , "+ country_inj+',-,'+ 'Leaked by  AS' + str(elem['detected asn']) + ', ' +country_cau,', '+ elem['moredetail']
        new_dict = {
            "ctry_inj": country_inj,
            "ctry_cau": country_cau,
            "ASN_cau": ["AS" + str(elem['detected asn'])],
            "ASN_inj": ["AS" + str(elem['leaked_to'])],
            "url": elem['moredetail'],
            "scrapped_from_url": [
                        [str(i) for i in elem['detected_aspath']],
                        ['PEERS AFFECTED '+ str(elem['peers'])] 
            ],
            "text": new_text
        }

        if country_inj == country_cau:
            
            if country_inj in ret_data.keys():
                HJ_autosab = ret_data[country_inj]['HJ_autosabotage'] # Dic{fecha: Lis[dic{'ctry_inj": ,ctry_cau:, ASN_cau:[] , ASN_inj:[], url,scrapped_from_url : [ASNs], text:}
                if str(new_date_key) in HJ_autosab.keys():
                    HJ_autosab[str(new_date_key)].append(new_dict)
                else:
                    HJ_autosab[str(new_date_key)] = [new_dict]

                ret_data[country_inj]['HJ_autosabotage'] = HJ_autosab
            else:
                full_name = pycountry.countries.get(alpha_2=country_inj)
                if full_name:
                    full_name = full_name.name
                else:
                    full_name = country_inj
                dict_autosab = {
                        # 'ctry_fullname': inj_ctry['Name'].values[0],
                        'ctry_fullname': full_name,
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{}, 'causer': {}},
                        'HJ_count': {'injured_count': 0, 'causer_count':0} ,
                        'HJ_autosabotage': {str(new_date_key) : [new_dict]},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [],
                            'causer': []
                        }
                    }
                ret_data[country_inj] = dict_autosab
        else:
            if country_inj in ret_data.keys():
                HJ_INJ_dates = ret_data[country_inj]['HJ_by_date']['injured']# Dict{fecha: dict{List [ dict{ctry:, ASN:, rul:, scrapped_from_url:, text:}]}
                HJ_INJ_cont = ret_data[country_inj]['HJ_count']['injured_count']  # numero += 1
                issue_HJ_INJ = ret_data[country_inj]['issue_hj']['inju'] # List[dict{text:, issue_date:}]


                if str(new_date_key) in HJ_INJ_dates.keys():
                    HJ_INJ_dates[str(new_date_key)].append(new_dict)
                else:
                    HJ_INJ_dates[str(new_date_key)] = [new_dict]

                ret_data[country_inj]['HJ_by_date']['injured'] = HJ_INJ_dates

                HJ_INJ_cont+=1
                ret_data[country_inj]['HJ_count']['injured_count'] = HJ_INJ_cont

                issue_hj_inj_dict = {'text': new_text,'issue_date':str(new_date_key)}
                issue_HJ_INJ.append(issue_hj_inj_dict)
                ret_data[country_inj]['issue_hj']['inju'] = issue_HJ_INJ
            else:
                full_name = pycountry.countries.get(alpha_2=country_inj)
                if full_name:
                    full_name = full_name.name
                else:
                    full_name = country_inj
                inju_dict= {
                        # 'ctry_fullname': inj_ctry['Name'].values[0],
                        'ctry_fullname': full_name,
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured': {str(new_date_key): [new_dict]},
                                       'causer': {}},
                        'HJ_count': {'injured_count': 1, 'causer_count':0} ,
                        'HJ_autosabotage': {},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [{'text':new_text,'issue_date': str(new_date_key)}],
                            'causer': []
                        }
                    }

                ret_data[country_inj] = inju_dict

            if country_cau in ret_data.keys():
                HJ_CAU_dates = ret_data[country_cau]['HJ_by_date']['causer']# Dict{fecha: dict{List [ dict{ctry:, ASN:, rul:, scrapped_from_url:, text:}]}
                HJ_CAU_cont = ret_data[country_cau]['HJ_count']['causer_count'] # numero += 1
                issue_HJ_CAU = ret_data[country_cau]['issue_hj']['causer'] # List[dict{text:, issue_date:}]

                if str(new_date_key) in HJ_CAU_dates.keys():
                    HJ_CAU_dates[str(new_date_key)].append(new_dict)
                else:
                    HJ_CAU_dates[str(new_date_key)] = [new_dict]

                ret_data[country_cau]['HJ_by_date']['causer'] = HJ_CAU_dates

                HJ_CAU_cont+=1
                ret_data[country_cau]['HJ_count']['causer_count'] = HJ_CAU_cont

                issue_hj_cau_dict = {'text': new_text,'issue_date':str(new_date_key)}
                issue_HJ_CAU.append(issue_hj_cau_dict)
                ret_data[country_cau]['issue_hj']['causer']  = issue_HJ_CAU
            else:
                full_name = pycountry.countries.get(alpha_2=country_cau)
                if full_name:
                    full_name = full_name.name
                else:
                    full_name = country_cau
                cau_dict = {
                        # 'ctry_fullname': cau_ctry['Name'].values[0],
                        'ctry_fullname': full_name,
                        'OT_by_date': {},
                        'OT_count': 0 ,
                        'HJ_by_date': {'injured':{},
                                       'causer': {str(new_date_key): [new_dict]}},
                        'HJ_count': {'injured_count': 0, 'causer_count':1} ,
                        'HJ_autosabotage': {},
                        'issue_ot':[],
                        'issue_hj':{
                            'inju': [],
                            'causer': [{'text':new_text,'issue_date': str(new_date_key)}]
                        }
                    }
                ret_data[country_cau] = cau_dict

        return ret_data
    
    # Funcion para actualizar los datos nuevos publicados en Twitter, almacenando dicha informacion en google drive
    def update_data(self, filename):
        file, content = self.gdrive.download_file(Scrapped_From_Twitter)
        if not file or not content:
            self.store_inital_data(Scrapped_From_Twitter)
            file, content = self.gdrive.download_file(Scrapped_From_Twitter)

        dict_data = json.loads(content)
        since_id = int(dict_data['max_id'])

        user_tweets =  self.scrapp.scrap_info_by_user_between_dates(username="bgpstream",since_id=since_id)

        dic_info, last_date = self.parser.get_bgp_info_of_tweets(dict_data, user_tweets)
        
        dic_info = self.update_dictionary_dates(dic_info)

        self.gdrive.update_gdrive_file(file, json.dumps(dic_info,indent=4))
        print("------------------------------Twitter Data updated and saved in Google Drive------------------------------")
        self.reload_info()
        self.save_BGP_issues_by_country(filename)
        

              
        return dict_data

# Main().update_data("final_dict_by_country.json")
# Main().load_bgp_issues_from_file("BGP_TFM/dataset/record.json","final_dict_by_country_maximi_v3.json",start=16001,end= 19900)

