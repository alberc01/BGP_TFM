import json
import datetime


def write_dict_to_file(name, dict):
        with open(name, "a") as outfile:
                    json.dump(dict, outfile,indent=4)

def string_to_datetime(string_date):
    return datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S%z')
    
# Funcion para leer el archivo Json que contiene la informacion con las incidencias BGP
def readJson(filename):
    # Apertura y lectura del archivo Json correspondiente y almacenado localmente
    with open(filename)as json_file:
        raw_data  = json.load(json_file)
    
    # Inicializacion de listas que seleccionaran la informacion que sera tratada en la aplicacion
    country = []
    ot_data = []
    country_iso2 = []

    # Obtencion de las fechas mas reciente y mas antigua para limitar el calendario de la aplicacion
    recent_date= string_to_datetime(raw_data['most_recent_date'])
    oldest_date= string_to_datetime(raw_data['oldest_date'])

    # Poblado de datos con la informacion del Json, para que sea mas facil de tratar
    for k in raw_data.keys():
        if k not in ["oldest_date", "most_recent_date"]:
            country.append(raw_data[k]['ctry_fullname'])
            country_iso2.append(k)
            ot_data.append(raw_data[k]['OT_count'])

    return country, country_iso2, raw_data, ot_data, oldest_date, recent_date