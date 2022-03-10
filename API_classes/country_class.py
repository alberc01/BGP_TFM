from calendar import c
import pandas as pd
from ipwhois import IPWhois
import subprocess
import re
from collections import Counter

class Country:
    def __init__(self):
        self.country_dataframe = self.read_country_diminutives()
        
    def read_country_diminutives(self):
        dfs = pd.read_excel("/home/alber/TFM-LINUX/BGP_TFM/country_info/country.xlsx", sheet_name= None)
        partial_dfs = dfs['Codes']
        final_df = pd.DataFrame(partial_dfs, columns=['ISO2', 'ISO3', 'CATEGORY', 'LIST NAME'])
        return final_df

    def find_country_info(self, country_code, id):
        data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_code]
        if len(data.values) < 1:
            data = self.country_dataframe.loc[self.country_dataframe['ISO3']==country_code]
            if len(data.values) < 1:
                data = self.country_dataframe.loc[self.country_dataframe['LIST NAME']==country_code]
                if len(data.values) < 1:
                    data = self.country_dataframe.loc[self.country_dataframe['ISO2']==id]
                    if len(data.values) < 1:
                        data = self.country_dataframe.loc[self.country_dataframe['ISO3']==id]
                        if len(data.values) < 1:
                            data = self.country_dataframe.loc[self.country_dataframe['LIST NAME']==id]
                            if len(data.values) < 1 :
                                # try to get ASN country by whois
                                if id != 'ZZ':
                                    as_name  = 'AS'+ id
                                else:
                                    as_name = country_code.split(' ')
                                    regex = re.compile(r'^AS')
                                    filtered = [i for i in as_name if regex.match(i)]
                                    if len(filtered) > 0:
                                        as_name = filtered[0]
                                    else:
                                        data = {'ISO2':[id],'ISO3':[country_code],'CATEGORY':'UNKNOWN', 'LIST NAME': [country_code]}
                                        data = pd.DataFrame.from_dict(data)
                                        return data
                                try :
                                    server_data = subprocess.check_output(['whois',as_name])
                                    
                                    server_data = str(server_data).split('\\n')
                                    
                                    regex = re.compile(r'^country')
                                    filtered = [i.replace(" ", '').replace("country:", '') for i in server_data if regex.match(i)]
                                
                                    
                                    if len(filtered) > 0:
                                        dict_country_rept = Counter(filtered)
                                        dict_country_rept['ZZ'] = 0
                                        country_code = max(dict_country_rept, key = dict_country_rept.get)
                                        
                                        data = self.country_dataframe.loc[self.country_dataframe['ISO2']==country_code]
                                    else:
                                        data = {'ISO2':[id],'ISO3':[country_code],'CATEGORY':'UNKNOWN', 'LIST NAME': [country_code]}
                                        data = pd.DataFrame.from_dict(data)
                                except:
                                    data = {'ISO2':[id],'ISO3':[country_code],'CATEGORY':'UNKNOWN', 'LIST NAME': [country_code]}
                                    data = pd.DataFrame.from_dict(data)

        return data